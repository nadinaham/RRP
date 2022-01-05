# RRP documentation

This is the official documentation and repository for Professor Lixin Gao's project, Privacy-Preserving Data Analytics on Complex Networks. The readme will be updated everytime a new commit is pushed to the main branch. 

**Research partners:** Nadine Han (25), Shirley Zhu (25), and Anaga Dinesh (23)

# Week 1
Goals were to find an online model using Python to filter out videos for moving objects.

**Files used:** model1_orig.py, model2_mod.py

**File explanation:**

(1) _model1_orig.py_

First model, simple / uses one frame in order to compare new frames in video to determine differences. Returns four different versions of webcam video with different filters, as well as a CSV file with movement times.

Can be run by using the command: python model1_orig.py

pulled from: https://www.geeksforgeeks.org/webcam-motion-detector-python/

(2) _model1_mod.py_

First model but modified in order to get rid of some of the video filters and not return the CSV files with movement times.

Can be run by using the command: python model1_mod.py

# Week 2
**Files used:** model2_orig.py, model2_mod.py, TempImage.py

**File explanation:**

(1) _model2_orig.py_

Second model, simple / uses one frame in order to compare new frames in video to determine differences. Returns three different versions of the video input, can both take inputs and record from webcam if no input is given. 

Can be run by using the command in the RRP folder: python model2_orig.py --video /videos/VIDNAME

pulled from: https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

(2) _model2_mod.py_

Second model, similar to original but a WIP. Currently the code is designed to be hooked up to an RPi camera and Dropbox, but am trying to rework it to be for laptop only. The point of this file is to use a background average system to serve as the comparison for new frames, which reduces false positives in the video caused by lighting and other processing problems, thus making the algorithm more accurate.

pulled from: https://www.pyimagesearch.com/2015/06/01/home-surveillance-and-motion-detection-with-the-raspberry-pi-python-and-opencv/

(3) _TempImage.py_

Helper file for model2_mod.py

# MASTER UPDATE: Weeks 3-7 (End of Fall Semester)
**Status:** Foreground masking & background subtraction models acquired and tested; now looking into homomorphic encryption and microcontroller usage


**Noteable Updates since last commit:**

(1) Reorganization of folders according to what model they house

(2) Microcontroller files/files designed for microcontroller and above implementation


**Files highlighted:** detect.py and detect_bg.py (in frameDifferencing)


**Files explanation:**

(1) detect.py: new model currently used for foreground masking; when run, it loads an input video (or camera input) and blots out the moving objects

pulled from: https://debuggercafe.com/moving-object-detection-using-frame-differencing-with-opencv/


(2) detect_bg.py: new model currently used for background subrtaction; when run, it loads an input video (or camera input) and blots out the background around the moving objects. based off of detect.py


(3) get_background.py: helper function for the prior two files that acquires and identifies the background of the video
