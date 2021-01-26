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
    4.	pos: Keep this = 0.
    5.	th_b: This is the threshold value for detecting blinks. If the average eye aspect ratio (EAR) is less than or equal to th_b, then the system thinks that the eyes are closed. ‘analyze_ear.py’ can be used to decide this threshold value. The blinking counting is sensitive to this threshold value and a wrong threshold value will lead to wrong number of blinks.
    6.	visualize: This is to tell the system whether to visualize the output video or not while the system is processing. Visualize = 0 for not visualizing and visualize = 1 for visualizing.
    7.	save_output: This is to tell the system whether to save the output video, graph, and excel file or not. save_output = 0 for not saving and save_output = 1 for saving.

2. Run main.py

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

_For more examples and usage, please refer to the [Wiki][wiki]._

Chris Henry – engr.chrishenry@gmail.com


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


