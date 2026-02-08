# Import all the necessary libraries
import argparse
import dlib
import cv2
import os
import utils
from tqdm import tqdm
import matplotlib.pyplot as plt
import csv


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compute Eye Aspect Ratio (EAR) from a video using dlib facial landmarks"
    )

    parser.add_argument(
        "--video",
        type=str,
        required=True,
        help="Path to input video file"
    )

    parser.add_argument(
        '--dat',
        type=str,
        default="shape_predictor_68_face_landmarks.dat",
        help='Path to dlib shape predictor .dat file.'
    )

    parser.add_argument(
        "--start_time",
        type=str,
        default="00:00:00",
        help="Start time (hh:mm:ss) [default: 00:00:00]"
    )

    parser.add_argument(
        "--end_time",
        type=str,
        default=None,
        help="End time (hh:mm:ss). If not provided, process till end of video"
    )

    parser.add_argument(
        '--scale',
        type=float,
        default=1.0,
        help='Video resize scale (0.1-1.0) for faster video processing. scale: 0.5 -> resizes video to 50%% of the original size.'
    )

    return parser.parse_args()


def main():
    args = parse_args()

    vid_path = args.video
    dat_file_path = args.dat
    start_vid_time = args.start_time
    end_vid_time = args.end_time
    scale = args.scale

    start_msec = utils.get_msec_pos(start_vid_time)

    cap = cv2.VideoCapture(vid_path)
    FPS = cap.get(cv2.CAP_PROP_FPS)

    if end_vid_time is not None:
        end_msec = utils.get_msec_pos(end_vid_time)
    else:
        end_msec = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / FPS * 1000)

    rot_count = utils.check_video_orientation(vid_path)

    cap.set(cv2.CAP_PROP_POS_MSEC, start_msec)

    video_name = os.path.splitext(os.path.basename(vid_path))[0]
    output_dir = f"ear_analysis_{video_name}"

    # Create output folder if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    csv_file_path = os.path.join(output_dir, f"{video_name}_ear.csv")
    csv_file_ear = open(csv_file_path, "w", newline="")

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(dat_file_path)

    total = int((end_msec - start_msec) / 1000 * FPS)
    pbar = tqdm(total=total, ncols=100, desc="Processing")

    earr_list = []

    while True:
        success, image = cap.read()
        if not success:
            break

        if int(cap.get(cv2.CAP_PROP_POS_MSEC)) >= end_msec:
            break

        image = utils.fix_orientation(image, rot_count)
        image = cv2.resize(image, (0, 0), fx=scale, fy=scale)

        image, left_eye_marks, right_eye_marks = utils.get_landmarks(
            image, detector, predictor
        )

        if left_eye_marks.size > 0 or right_eye_marks.size > 0:
            leftEAR = utils.eye_aspect_ratio(left_eye_marks)
            rightEAR = utils.eye_aspect_ratio(right_eye_marks)
            ear = float("{:.2f}".format((leftEAR + rightEAR) / 2.0))
            earr_list.append(ear)

        pbar.update(1)

    pbar.close()
    cap.release()

    # Plot EAR graph
    plt.figure("Eye Aspect Ratio Graph")
    plt.plot(earr_list, "r", linestyle="-", linewidth=0.2)
    plt.xlabel("Frame Number")
    plt.ylabel("Eye Aspect Ratio")
    graph_file_path = os.path.join(output_dir, f"{video_name}_Graph.png")
    print(f"Saving graph to {graph_file_path}")
    plt.savefig(graph_file_path, dpi=1200)

    # Write CSV
    writer = csv.writer(csv_file_ear)
    csvbar = tqdm(total=len(earr_list), ncols=100, desc="Writing .CSV file")
    for ear in earr_list:
        writer.writerow([ear])
        csvbar.update(1)

    csvbar.close()
    csv_file_ear.close()

    print(f"Finished. All outputs saved in folder: {output_dir}")


if __name__ == "__main__":
    main()
