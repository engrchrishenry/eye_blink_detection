# Eye Blink Counter using OpenCV Python and Dlib

This software can count the number of times a person blinked his/her eyes. It uses facial landmarks and analyzes the eye aspect ratio (EAR). In addition, since most people have different EAR values, this project also provides an option to select the threshold value required for detecting eye blinks.

<img src="https://github.com/engrchrishenry/eye_blink_detection/blob/main/images/gif.gif" width="500" />

## Requirements:
This project was tested with python 3.10 on Linux.
 - dlib
 - opencv-python
 - tqdm
 - matplotlib
 - imutils
 - scipy

## Installation

- Clone this repository
   ```bash
   git clone https://github.com/engrchrishenry/eye_blink_detection.git
   cd eye_blink_detection
   ```
- Create conda environment
   ```bash
   conda create --name eye python=3.10
   conda activate eye
   ```
- Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Demo
Download the [shape_predictor_68_face_landmarks.dat.bz2](https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2) file and extract it get the 'shape_predictor_68_face_landmarks.dat'. Place the .dat file in the parent directory.

Run [main.py](https://github.com/engrchrishenry/eye_blink_detection/blob/main/main.py) to detect the number of eye blink in a video.
```bash
python main.py --video "path_to_video"
```

#### Parameters
```
usage: main.py [-h] --video VIDEO [--dat DAT] [--scale SCALE] [--th_b TH_B] [--visualize VISUALIZE] [--save SAVE] [--pos POS]

Eye Blink Detection using OpenCV and dlib

options:
  -h, --help            show this help message and exit
  --video VIDEO         Path to video file.
  --dat DAT             Path to dlib shape predictor .dat file.
  --scale SCALE         Video resize scale (0.1-1.0) for faster video processing. scale: 0.5 -> resizes video to 50% of the
                        original size.
  --th_b TH_B           Threshold for detecting eye blink. This is the threshold value for detecting blinks. If the average eye
                        aspect ratio (EAR) is less than or equal to th_b, then the system thinks that the eyes are closed.
                        ‘analyze_ear.py’ can be used to decide this threshold value.
  --visualize VISUALIZE
                        Visualize output: 1 = Yes, 0 = No.
  --save SAVE           Save output: 1 = Yes, 0 = No.
  --pos POS             Starting frame position.
```

After running [main.py](https://github.com/engrchrishenry/eye_blink_detection/blob/main/main.py), a window will pop up to check the orientation of the video file. If the video orientation is incorrect, press 'r' to rotate the frame until orientation is fixed. Once orientation if fixed, press 'q' to proceed. If orientation is already correct, directly press 'q' to skip this step.

See results in 'results_<video_name>' folder (if save = 1). 'results_<video_name>' will contain:
- Output video file
- Excel file containing the average EAR values for each frame in the video.
- An image file containing the graph of average EAR values with respect to frame number.
- A CSV file containg information such as blink count and blink frequency.

## Optimal threshold for detecting eye blinks
Run [analyze_ear.py](https://github.com/engrchrishenry/eye_blink_detection/blob/main/main.py) to find the optimal threshold for detecting eye blinks.
```bash
python analyze_ear.py --video "path_to_video"
```

#### Parameters
```
usage: analyze_ear.py [-h] --video VIDEO [--dat DAT] [--start_time START_TIME]
                      [--end_time END_TIME] [--scale SCALE]

Compute Eye Aspect Ratio (EAR) from a video using dlib facial landmarks

options:
  -h, --help            show this help message and exit
  --video VIDEO         Path to input video file
  --dat DAT             Path to dlib shape predictor .dat file.
  --start_time START_TIME
                        Start time (hh:mm:ss) [default: 00:00:00]
  --end_time END_TIME   End time (hh:mm:ss). If not provided, process till end
                        of video
  --scale SCALE         Video resize scale (0.1-1.0) for faster video
                        processing. scale: 0.5 -> resizes video to 50% of the
                        original size.
```

Similar to running [main.py](https://github.com/engrchrishenry/eye_blink_detection/blob/main/main.py), a window will pop up for checking video orientation.

See results in 'ear_analysis_<video_name>' folder (if save = 1). 'ear_analysis_<video_name>' will contain:
- Excel file containing the average EAR values for each frame in the video.
- An image file containing the graph of average EAR values with respect to frame number.

Based on the graph generated, analyze the peaks to set the threshold value.
<img src="https://github.com/engrchrishenry/eye_blink_detection/blob/main/images/EAR%20Graph.png" width="500" />

## Acknowledgment
This code is inspired from Adrian Rosebrock's amazing tutorial:

https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)
