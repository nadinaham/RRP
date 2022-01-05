import numpy as np
import glob
import matplotlib.pyplot as plt
import skimage.io
import skimage.color
import skimage.filters

# load the image
image = skimage.io.imread("assets/shapes.png")

fig, ax = plt.subplots()
plt.imshow(image)

# convert the image to grayscale
gray_image = skimage.color.rgb2gray(image)

# blur the image to denoise
blurred_image = skimage.filters.gaussian(gray_image, sigma=1.0)

fig, ax = plt.subplots()
plt.imshow(blurred_image, cmap='gray')

# create a mask based on the threshold
t = 0.8
binary_mask = blurred_image < t

fig, ax = plt.subplots()
plt.imshow(binary_mask, cmap='gray')

# use the binary_mask to select the "interesting" part of the image
selection = np.zeros_like(image)
selection[binary_mask] = image[binary_mask]

fig, ax = plt.subplots()
plt.imshow(selection)
plt.show()