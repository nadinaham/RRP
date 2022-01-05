# import the necessary packages
import numpy as np
import argparse
import time
import cv2
import os
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", type=str,
	default=os.path.sep.join(["images", "lighthouse.png"]),
	help="path to input image that we'll apply GrabCut to")
ap.add_argument("-mask", "--mask", type=str,
	default=os.path.sep.join(["images", "lighthouse_mask.png"]),
	help="path to input mask")
ap.add_argument("-c", "--iter", type=int, default=10,
	help="# of GrabCut iterations (larger value => slower runtime)")
args = vars(ap.parse_args())

# load the input image and associated mask from disk
image = cv2.imread(args["image"])
mask = cv2.imread(args["mask"], cv2.IMREAD_GRAYSCALE)
# apply a bitwise mask to show what the rough, approximate mask would
# give us
roughOutput = cv2.bitwise_and(image, image, mask=mask)
# show the rough, approximated output
cv2.imshow("Rough Output", roughOutput)
cv2.waitKey(0)

# any mask values greater than zero should be set to probable
# foreground
mask[mask > 0] = cv2.GC_PR_FGD
mask[mask == 0] = cv2.GC_BGD

# allocate memory for two arrays that the GrabCut algorithm internally
# uses when segmenting the foreground from the background
fgModel = np.zeros((1, 65), dtype="float")
bgModel = np.zeros((1, 65), dtype="float")
# apply GrabCut using the the mask segmentation method
start = time.time()
(mask, bgModel, fgModel) = cv2.grabCut(image, mask, None, bgModel,
	fgModel, iterCount=args["iter"], mode=cv2.GC_INIT_WITH_MASK)
end = time.time()
print("[INFO] applying GrabCut took {:.2f} seconds".format(end - start))

# the output mask has for possible output values, marking each pixel
# in the mask as (1) definite background, (2) definite foreground,
# (3) probable background, and (4) probable foreground
values = (
	("Definite Background", cv2.GC_BGD),
	("Probable Background", cv2.GC_PR_BGD),
	("Definite Foreground", cv2.GC_FGD),
	("Probable Foreground", cv2.GC_PR_FGD),
)
# loop over the possible GrabCut mask values
for (name, value) in values:
	# construct a mask that for the current value
	print("[INFO] showing mask for '{}'".format(name))
	valueMask = (mask == value).astype("uint8") * 255
	# display the mask so we can visualize it
	cv2.imshow(name, valueMask)
	cv2.waitKey(0)

# set all definite background and probable background pixels to 0
# while definite foreground and probable foreground pixels are set
# to 1, then scale teh mask from the range [0, 1] to [0, 255]
outputMask = np.where((mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD),
	0, 1)
outputMask = (outputMask * 255).astype("uint8")
# apply a bitwise AND to the image using our mask generated by
# GrabCut to generate our final output image
output = cv2.bitwise_and(image, image, mask=outputMask)

# show the input image followed by the mask and output generated by
# GrabCut and bitwise masking
cv2.imshow("Input", image)
cv2.imshow("GrabCut Mask", outputMask)
cv2.imshow("GrabCut Output", output)
cv2.waitKey(0)