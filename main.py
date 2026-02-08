import dlib
import cv2
import os
import utils
from tqdm import tqdm
import matplotlib.pyplot as plt
import csv
import argparse

# -----------------------
# Argument parser
# -----------------------
parser = argparse.ArgumentParser(description="Eye Blink Detection using OpenCV and dlib")
parser.add_argument('--video', type=str, required=True, help='Path to video file.')
parser.add_argument('--dat', type=str, default="shape_predictor_68_face_landmarks.dat",
                    help='Path to dlib shape predictor .dat file.')
parser.add_argument('--scale', type=float, default=1.0, help='Video resize scale (0.1-1.0) for faster video processing. scale: 0.5 -> resizes video to 50%% of the original size.')
parser.add_argument('--th_b', type=float, default=0.28, help='Threshold for detecting eye blink. This is the threshold value for detecting blinks. If the average eye aspect ratio (EAR) is less than or equal to th_b, then the system thinks that the eyes are closed. ‘analyze_ear.py’ can be used to decide this threshold value.')
parser.add_argument('--visualize', type=int, default=1, help='Visualize output: 1 = Yes, 0 = No.')
parser.add_argument('--save', type=int, default=1, help='Save output: 1 = Yes, 0 = No.')
parser.add_argument('--pos', type=int, default=0, help='Starting frame position.')
args = parser.parse_args()

# -----------------------
# Video setup
# -----------------------
cap = cv2.VideoCapture(args.video)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
FPS = cap.get(cv2.CAP_PROP_FPS)
cap.set(cv2.CAP_PROP_POS_FRAMES, args.pos)

# Optional: handle rotation if video has orientation metadata
rot_count = utils.check_video_orientation(args.video)

# -----------------------
# Dlib setup
# -----------------------
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args.dat)

# -----------------------
# Output folder setup
# -----------------------
filename = os.path.splitext(os.path.basename(args.video))[0]
output_dir = f'results_{filename}'  # same folder as video
os.makedirs(output_dir, exist_ok=True)  # create folder if it doesn't exist

if args.save:
    csv_file_ear = open(os.path.join(output_dir, filename + '_ear.csv'), 'w', newline='')
    csv_file_info = open(os.path.join(output_dir, filename + '_info.csv'), 'w', newline='')
    out = cv2.VideoWriter(os.path.join(output_dir, filename + '_output.mov'),
                          cv2.VideoWriter_fourcc(*'mp4v'),
                          FPS, (int(w*args.scale), int(h*args.scale)))

# -----------------------
# Counters and lists
# -----------------------
c_lr = 0
t_lr = 0
ind_list = []
earr_list = []

pbar = tqdm(total=frame_count, ncols=100, desc='Processing')

# -----------------------
# Main loop
# -----------------------
while True:
    success, image = cap.read()
    if not success:
        break

    # Fix orientation and resize
    image = utils.fix_orientation(image, rot_count)
    image = cv2.resize(image, (0, 0), fx=args.scale, fy=args.scale)

    # Get landmarks
    image, left_eye_marks, right_eye_marks = utils.get_landmarks(image, detector, predictor)

    if left_eye_marks.size > 0 or right_eye_marks.size > 0:
        leftEAR = utils.eye_aspect_ratio(left_eye_marks)
        rightEAR = utils.eye_aspect_ratio(right_eye_marks)

        ear, t_lr, ind_list = utils.detect_blink(leftEAR, rightEAR, t_lr, args.th_b, ind_list)

        utils.draw(image, leftEAR, rightEAR, ear, t_lr)

        earr_list.append(ear)

    if args.visualize:
        cv2.namedWindow("Visual Video Output", cv2.WINDOW_NORMAL)
        cv2.imshow("Visual Video Output", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if args.save:
        out.write(image)

    pbar.update(1)

pbar.close()

# -----------------------
# Save results
# -----------------------
if args.save:
    # Plot EAR graph
    plt.figure('Eye Aspect Ratio Graph')
    plt.plot(earr_list, 'r', linestyle='-', linewidth=0.2)
    plt.xlabel('Frame Number')
    plt.ylabel('Eye Aspect Ratio')
    plt.savefig(os.path.join(output_dir, filename + '_Graph.png'), dpi=1200)

    # Save EAR CSV
    writer = csv.writer(csv_file_ear)
    for ear in earr_list:
        writer.writerow([ear])
    csv_file_ear.close()

    # Save info CSV
    video_dur = (frame_count / FPS) / 60
    freq = t_lr / video_dur
    writer = csv.writer(csv_file_info)
    writer.writerow(["Filename", "Blink Count", "Frequency (Blinks/min)"])
    writer.writerow([filename, str(t_lr), str(freq)])
    csv_file_info.close()

cv2.destroyAllWindows()
cap.release()
if args.save:
    out.release()

print(f'Finished. All outputs saved to folder: {output_dir}')
