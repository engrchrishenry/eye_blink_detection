# Import all the necessary libraries
from imutils import face_utils
import cv2
import numpy as np
from scipy.spatial import distance as dist

# Function to convert time to milli seconds.
def get_msec_pos(vid_time):
    vid_time = vid_time.split(":")
    hour = int(vid_time[0])
    min = int(vid_time[1])
    msec = ((hour * 60 * 60) + (min * 60) + int(vid_time[2])) * 1000
    return msec

# Function to get cropped left and right eye and coordinates
def get_landmarks(image, detector, predictor):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Convert image to grayscale
    landmarks = detector(gray_image, 0) # Detect face in image
    left_eye_marks, right_eye_marks = np.array([]), np.array([]) # Assign empty numpy array
    if landmarks != []: # If face was detected
        for (i, rect) in enumerate(landmarks): # Detect face in the frame
            (x, y, w, h) = face_utils.rect_to_bb(rect) # Get coordinates of face
            # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2) # Draw box around the detected face
            shape = predictor(gray_image, rect) # Predict landmarks in the detected face
            shape = face_utils.shape_to_np(shape) # Convert landmarks to numpy array

            (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"] # Extract landmarks for left eye
            left_eye_marks = shape[lStart:lEnd] # Extract landmarks for left eye

            (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"] # Extract landmarks for right eye
            right_eye_marks = shape[rStart:rEnd] # Extract landmarks for right eye

            cv2.polylines(image, [left_eye_marks], True, (0, 255, 255)) # Draw boundary on left eye
            cv2.polylines(image, [right_eye_marks], True, (0, 255, 255)) # Draw boundary on right eye

            # for (x, y) in shape: # Draw detected facial landmarks
            #     cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
    return image, left_eye_marks, right_eye_marks


# Function to calculate eye aspect ratio
def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return float("{:.2f}".format(ear))


def detect_blink(leftEAR, rightEAR, t_lr, th_b, ind_list):
    ear = float("{:.2f}".format((leftEAR + rightEAR) / 2.0)) # Calculate average of left and right eye EAR.

    if len(ind_list) < 2:
        if ear <= th_b:
            ind_list.append('close')
        else:
            ind_list.append('open')
    else:
        prev1 = ind_list[-1]
        prev2 = ind_list[-2]
        if ear <= th_b:
            ind_list.append('close')
            curr = 'close'
        else:
            ind_list.append('open')
            curr = 'open'
        if curr == 'open' and prev1 == 'close' and prev2 == 'close':
            t_lr = t_lr + 1

    return ear, t_lr, ind_list


# Function to draw values on image.
def draw(image, leftEAR, rightEAR, ear, t_lr):
    cv2.putText(image, "EAR Left: " + str(leftEAR), (image.shape[1] // 2, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 255, 255), 2)
    cv2.putText(image, "EAR Right: " + str(rightEAR), (image.shape[1] // 2, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 255, 255), 2)
    cv2.putText(image, "EAR Avg: " + str(ear), (image.shape[1] // 2, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 255, 255), 2)
    cv2.putText(image, "Blinks: " + str(t_lr), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

# Function to fix orientation
def fix_orientation(img, rot_count):
    for i in range(rot_count):
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    return img

# Function to check video orientation
def check_video_orientation(vid_path):
    temp_cap = cv2.VideoCapture(vid_path)
    err, img = temp_cap.read()
    cv2.namedWindow("Check Video Orientation", cv2.WINDOW_NORMAL)
    cv2.imshow("Check Video Orientation", img)
    k = cv2.waitKey(0) & 0xFF
    if k == ord("q"):
        cv2.destroyWindow("Check Video Orientation")
        return 0
    if k == ord("r"):
        rot_count = 0
        while 1:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            cv2.imshow("Check Video Orientation", img)
            rot_count = rot_count + 1
            k = cv2.waitKey(0) & 0xFF
            if k == ord("q"):
                cv2.destroyWindow("Check Video Orientation")
                return rot_count


