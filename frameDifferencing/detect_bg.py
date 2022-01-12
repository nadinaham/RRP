# COMMAND TO RUN: python detect_bg.py --input /Users/Nadine/Desktop/RRP/videos/VIDEONAME.mp4

# should remove the background by blacking it out, leaving the moving objects

import cv2
import argparse
from get_background import get_background
import numpy
import time

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='path to the input video',
                    required=True)
parser.add_argument('-c', '--consecutive-frames', default=4, type=int,
                    dest='consecutive_frames', help='path to the input video')
args = vars(parser.parse_args())

cap = cv2.VideoCapture(args['input'])

start = time.time()

# get the video frame height and width
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
save_name = f"outputs/{args['input'].split('/')[-1]}"
# define codec and create VideoWriter object
out = cv2.VideoWriter(
    save_name,
    cv2.VideoWriter_fourcc(*'mp4v'), 10, 
    (frame_width, frame_height)
)

# get the background model
background = get_background(args['input'])
# convert the background model to grayscale format
background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
frame_count = 0
consecutive_frame = args['consecutive_frames']

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        frame_count += 1
        orig_frame = frame.copy()
        stencil = numpy.zeros(frame.shape).astype(frame.dtype)
        # IMPORTANT STEP: convert the frame to grayscale first
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if frame_count % consecutive_frame == 0 or frame_count == 1:
            frame_diff_list = []
        # find the difference between current frame and base frame
        frame_diff = cv2.absdiff(gray, background)
        # thresholding to convert the frame to binary
        ret, thres = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)
        # dilate the frame a bit to get some more white area...
        # ... makes the detection of contours a bit easier
        dilate_frame = cv2.dilate(thres, None, iterations=2)
        # append the final result into the `frame_diff_list`
        frame_diff_list.append(dilate_frame)
        # if we have reached `consecutive_frame` number of frames
        if len(frame_diff_list) == consecutive_frame:
            # add all the frames in the `frame_diff_list`
            sum_frames = sum(frame_diff_list)
            # find the contours around the white segmented areas
            contours, hierarchy = cv2.findContours(sum_frames, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # draw the contours, not strictly necessary
            for i, cnt in enumerate(contours):
                cv2.drawContours(frame, contours, i, (0, 0, 255), 3)
            for contour in contours:
                # continue through the loop if contour area is less than 500...
                # ... helps in removing noise detection
                if cv2.contourArea(contour) < 500:
                    continue
        
            # fill in contours
            cv2.fillPoly(stencil, contours, color = (255, 255, 255))
            result = cv2.bitwise_and(frame, stencil)
            cv2.imshow('Detected Objects', result)
            #out.write(result)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
    else:
        break

end = time.time()

cap.release()
cv2.destroyAllWindows()

print("runtime", end-start)