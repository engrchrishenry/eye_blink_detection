# Import all the necessary libraries
import dlib
import cv2
import os
import utils
from tqdm import tqdm
import matplotlib.pyplot as plt
import csv

vid_path = 'Videos/WIN_20210126_19_36_39_Pro.mp4' # Path to video file.
dat_file_path = "shape_predictor_68_face_landmarks.dat" # Path to .dat file.
start_vid_time = '00:00:00' # Time in hh:mm:ss format to specify the start time to process the video.
end_vid_time = '00:00:04' # Time in hh:mm:ss format to specify the end time to process the video.
scale = 0.5 # Video resize value (0.1-1.0). 1.0 means no resizing while 0.2 means resize video to 20% of the orginal video's resolution.

start_msec = utils.get_msec_pos(start_vid_time) # Convert time to milli seconds.
end_msec = utils.get_msec_pos(end_vid_time) # Convert time to milli seconds.

rot_count = utils.check_video_orientation(vid_path)

cap = cv2.VideoCapture(vid_path) # Read video from video file
FPS = cap.get(cv2.CAP_PROP_FPS) # Get frame rate of video.
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # Width of video
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # Height of video
cap.set(cv2.CAP_PROP_POS_MSEC, start_msec) # Set the position of video to start_msec.
filename = os.path.basename(vid_path) # Extract filename from path
filename = os.path.splitext(filename)[0] # Extract filename without the extension

csv_file_ear = open(filename + '_ear.csv', 'w', newline='') # Open a .CSV file.

detector = dlib.get_frontal_face_detector()  # Setup face detector from dlib
predictor = dlib.shape_predictor(dat_file_path)  # Input trained model file for facial landmark detection

total = (int((end_msec-start_msec)/1000 * FPS)) # Calculate total number of iterations for progress bar.
pbar = tqdm(total=total, ncols=100, desc='Processing') # Initialize progress bar for video processing.
earr_list = [] # Create an empty list for average EAR values.
while True:  # Run this loop always (until cancelled by some condition)
    success, image = cap.read()  # Read frame from the video

    # Exit out of the while loop if it reaches the end time.
    if int(cap.get(cv2.CAP_PROP_POS_MSEC)) >= end_msec:
        break

    image = utils.fix_orientation(image, rot_count)

    image = cv2.resize(image, (0, 0), fx=scale, fy=scale) # Resize frame.

    image, left_eye_marks, right_eye_marks = utils.get_landmarks(image, detector, predictor)  # Get cropped left and right eye images and coordinates
    if left_eye_marks != [] or right_eye_marks != []:  # Only run this if eye landmarks were detected
        leftEAR = utils.eye_aspect_ratio(left_eye_marks)  # Get aspect ratio of left eye
        rightEAR = utils.eye_aspect_ratio(right_eye_marks)  # Get aspect ratio of right eye
        ear = float("{:.2f}".format((leftEAR + rightEAR) / 2.0)) # Calculate average of left and right eye EAR.
        earr_list.append(ear) # Add EAR value to earr_list.

    pbar.update(1) # Print the overall progress

pbar.close() # Close the progress bar.

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
    writer.writerow([ear]) # Write average EAR value to .CSV file
    csvbar.update(1)# Print the overall progress
csvbar.close() # Close the progress bar.

cap.release()  # Release the window
print ('Finished.')