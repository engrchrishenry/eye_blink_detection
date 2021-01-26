# Import all the necessary libraries
import dlib
import cv2
import os
import utils
from tqdm import tqdm
import matplotlib.pyplot as plt
import csv

vid_path = 'Videos/WIN_20210126_21_39_50_Pro.mp4' # Path to video file.
dat_file_path = "shape_predictor_68_face_landmarks.dat" # Path to .dat file.
scale = 0.5 # Video resize value (0.1-1.0). 1.0 means no resizing while 0.2 means resize video to 20% of the orginal video's resolution.
th_b = 0.28 # Threshold for detecting eye blink
visualize = 0 # Visualize = 0 for not visualizing and visualize = 1 for visualizing the output video.
save_output = 1 # save_output = 0 for not saving and save_output = 1 for saving the output files.
pos = 0

rot_count = utils.check_video_orientation(vid_path)

cap = cv2.VideoCapture(vid_path) # Read video from video file.
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # Get total number of frames in video
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # Width of video
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Height of video
FPS = cap.get(cv2.CAP_PROP_FPS) # Get frame rate of video.
cap.set(cv2.CAP_PROP_POS_FRAMES, pos)

detector = dlib.get_frontal_face_detector() # Setup face detector from dlib
predictor = dlib.shape_predictor(dat_file_path) # Input trained model file for facial landmark detection

filename = os.path.basename(vid_path) # Extract filename from path
filename = os.path.splitext(filename)[0] # Extract filename without the extension

csv_file_ear = open(filename + '_ear.csv', 'w', newline='') # Open a .CSV file.
csv_file_info = open(filename + '_info.csv', 'w', newline='') # Open a .CSV file.
out = cv2.VideoWriter(filename + '_output.mov', cv2.VideoWriter_fourcc(*'mp4v'), FPS, (int(w*scale), int(h*scale))) # Setup output video

c_lr = 0 # Counter for eye blink detection
t_lr = 0 # Counter for total number of eye blinks
ind_list = [] # Create an empty list for holding eye status values.
earr_list = [] # Create an empty list for average EAR values.
pbar = tqdm(total=frame_count, ncols=100, desc='Processing') # Initialize progress bar for video processing.
while True: # Run this loop always (until cancelled by some condition)
    success, image = cap.read() # Read frame from the video

    # Exit out of the while loop if cannot get frame
    if success == False:
        break

    image = utils.fix_orientation(image, rot_count)

    image = cv2.resize(image, (0,0), fx=scale, fy=scale) # Resize frame.

    image, left_eye_marks, right_eye_marks = utils.get_landmarks(image, detector, predictor) # Get cropped left and right eye images and coordinates
    if left_eye_marks != [] or right_eye_marks != []: # Only run this if eye landmarks were detected
        leftEAR = utils.eye_aspect_ratio(left_eye_marks) # Get aspect ratio of left eye
        rightEAR = utils.eye_aspect_ratio(right_eye_marks) # Get aspect ratio of right eye
        
        ear, t_lr, ind_list = utils.detect_blink(leftEAR, rightEAR, t_lr, th_b, ind_list)  # Detect if a person blinked.

        utils.draw(image, leftEAR, rightEAR, ear, t_lr) # Draw values on frame

        earr_list.append(ear) # Add EAR value to earr_list.

    if visualize == 1:
        cv2.namedWindow("Visual Video Output", cv2.WINDOW_NORMAL)
        cv2.imshow("Visual Video Output", image) # Show the frame in a window
        cv2.waitKey(1) # Keep the output window opened for 1 ms

    if save_output == 1:
        out.write(image) # Write the frame to output video file.

    pbar.update(1) # Print the overall progress

pbar.close() # Close the progress bar.

if save_output == 1:
    # Plot the graph for average EAR values.
    plt.figure('Eye Aspect Ratio Graph')
    plt.plot(earr_list, 'r', linestyle='-', linewidth=0.2)
    plt.xlabel('Frame Number')
    plt.ylabel('Eye Aspect Ratio')

    print ("Saving graph.")
    plt.savefig(filename + '_Graph.png', dpi=1200) # Save the graph to an image file.

writer = csv.writer(csv_file_ear)
csvbar = tqdm(total=len(earr_list), ncols=100, desc='Writing .CSV file.') # Initialize progress bar for .CSV file processing.
for ear in earr_list:
    writer.writerow([ear])  # Write average EAR value to .CSV file
    csvbar.update(1)  # Print the overall progress
csvbar.close() # Close the progress bar.

video_dur = (frame_count/FPS)/60
freq = t_lr/video_dur

writer = csv.writer(csv_file_info)
writer.writerow(["Filename", "Blink Count", "Frequency (Blinks/min)"])
writer.writerow([filename, str(t_lr), str(freq)])

cv2.destroyAllWindows() # Close all windows
cap.release() # Release the window
out.release() # Release the output video

print ('Finished.')