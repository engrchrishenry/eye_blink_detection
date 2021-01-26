# Eye Blink Calculator using OpenCV Python

This software can calculate the number of times a person blinked his/her eyes.

## Requirements:
This project was tested with python 3.6 on Windows 10.
 - dlib
 - opencv
 - tqdm
 - matplotlib
 - imutils
 - scipy

## Install Dependencies

```sh
python -m pip install -r requirements.txt
```

## How to Use?

### Detecting number of eye blinks in video

1. Set the following parameters in main.py:
    1. vid_path: Here the path to the video file be added. For example:
    
       ```sh
       vid_path = ‘D:Videos/VideoX.MOV’
       ```
    
    2. dat_file_path: This is path to the file to predict facial landmarks. If "shape_predictor_68_face_landmarks.dat" file is in the folder where ‘main.py’ is located, then:
    
       ```sh
       dat_file_path = "shape_predictor_68_face_landmarks.dat"
       ```
       
    3. scale: This is the number (from 0.1 to 1.0) to decrease the resolution of video for faster processing. For example, if:
    
       ```sh
       scale = 0.2
       ```
       
       then the software will resize the video to 20% resolution of the original video. For a full HD video, scale = 0.2 or scale = 0.3 is fine. The smaller the value of scale, the faster the system will work and the larger the value of scale the slower the system will work.
    4.	pos: Use
       
        ```sh
        pos = 0
        ```

    5.	th_b (see 'How to set threshold for detecting eye blinks'): This is the threshold value for detecting blinks. If the average eye aspect ratio (EAR) is less than or equal to th_b, then the system thinks that the eyes are closed. ‘analyze_ear.py’ can be used to decide this threshold value. The blinking counting is sensitive to this threshold value and a wrong threshold value will lead to wrong number of blinks.
    6.	visualize: This is to tell the system whether to visualize the output video or not while the system is processing. For visualizing:
    
        ```sh
        visualize = 1
        ```
        For not visualizing:
       
        ```sh
        visualize = 0
        ```
       
    7.	save_output: This is to tell the system whether to save the output video, graph, and excel file or not. For saving:
        
        ```sh
        save_output = 1
        ```
        For not saving:
       
        ```sh
        save_output = 0
        ```

2. Run main.py
3. A window will pop up to check the orientation of the video file. Due to certain bug in OpenCV Python, sometimes the loaded frames from video have incorrect orientation. If the orienatation is incorrect, press 'r' to rotate the frame. Once you see the correct orientation, press 'q' to proceed. If orientation is already correct, directly press 'q' to skip this step.
3. The output after running main.py will be (provided that save_output = 1):
   1.	Output video file
   2.	Excel file containing the average EAR values for each frame in the video.
   3.	An image file containing the graph of average EAR values with respect to frame number.

### How to set threshold for detecting eye blinks

1. Set the following parameters in analyze_ear.py:
    1. vid_path: Here the path to the video file be added. For example:
    
       ```sh
       vid_path = ‘D:Videos/VideoX.MOV’
       ```
    
    2. dat_file_path: This is path to the file to predict facial landmarks. If "shape_predictor_68_face_landmarks.dat" file is in the folder where ‘main.py’ is located, then:
    
       ```sh
       dat_file_path = "shape_predictor_68_face_landmarks.dat"
       ```
       
    3.	start_vid_time: This is the start time in format hh:mm:ss. This defines from what time to start processing the video. This is done so the system does not process the entire video.
    4.	end_vid_time: This is the end time in format hh:mm:ss. This defines at what time to end processing the video. This is done so the system does not process the entire video.
    5.	scale: This is the number (from 0.1 to 1.0) to decrease the resolution of video for faster processing. For example, if:
    
       ```sh
       scale = 0.2
       ```
       then the software will resize the video to 20% resolution of the original video. For a full HD video, scale = 0.2 or scale = 0.3 is fine. The smaller the value of scale, the faster the system will work and the larger the value of scale the slower the system will work.

2. Run analyze_ear.py.
3. The output after running main.py will be (provided that save_output = 1):
   1.	Excel file containing the average EAR values for each frame in the video.
   2.	An image file containing the graph of average EAR values with respect to frame number.

## Note
[Windows Users] If dlib fails to install via pip, then download .whl file from https://pypi.org/simple/dlib/ and install manually.

## To Do
Add command-line usage.

## Acknowledgment
This code is heavily inspired from Adrian Rosebrock's amazing tutorial (https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/).

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki


