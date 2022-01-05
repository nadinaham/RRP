# import the necessary packages
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt
import skimage.io
import skimage.color
import skimage.filters

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

# otherwise, we are reading from a video file
else:
	vs = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None
# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	text = "Unoccupied"

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if frame is None:
		break

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)

    # FROM MODULE3: convert the image to grayscale
        gray_image = skimage.color.rgb2gray(frame)

    # FROM MODULE3: blur the image to denoise
        blurred_image = skimage.filters.gaussian(gray_image, sigma=1.0)

	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = blurred_image
		continue

    # compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, blurred_image)
	thresh = cv2.threshold(frameDelta, 125, 255, cv2.THRESH_BINARY)[1]

    # FROM MODULE3: create a mask based on the threshold
        binary_mask = blurred_image < thresh

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)

    # FROM MODULE3: use the binary_mask to select the "interesting" part of the image
        selection = np.zeros_like(frame)
        selection[binary_mask] = frame[binary_mask]

        fig, ax = plt.subplots()
        plt.imshow(selection)
        plt.show()

    # draw the text and timestamp on the frame
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break