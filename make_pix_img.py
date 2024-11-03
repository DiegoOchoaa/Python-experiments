import cv2 as cv
import os
from PIL import Image

# Load the image
original_img = cv.imread('/Users/diegoochoa/Documents/python/poetry/pixelator/landing 2.jpg')

# Define pixel size for pixelation
#pixel_size = input("pixelation: ")
pixel_size = 4

# Pixelate the image
def pixelate_image(img, pixel_size):
    height, width = img.shape[:2]
    img_resized = cv.resize(img, (width // pixel_size, height // pixel_size), interpolation=cv.INTER_LINEAR)
    return img_resized

pixelated_img = pixelate_image(original_img, pixel_size)
pixelated_height, pixelated_width = pixelated_img.shape[:2]

# Create a new image with RGBA mode
image = Image.new("RGBA", (pixelated_width, pixelated_height), color=(255, 255, 255, 0))  # Transparent background

# Define a threshold for white pixels
white_threshold = 240  # This allows for some variation in white pixels

for i, row in enumerate(pixelated_img):
    for j, pixel in enumerate(row):
        # Check if the pixel is considered "white" using the threshold
        if pixel[0] >= white_threshold and pixel[1] >= white_threshold and pixel[2] >= white_threshold:
            image.putpixel((j, i), (pixel[2], pixel[1], pixel[0], 0))  # Fully transparent for white-like pixels
        else:
            image.putpixel((j, i), (pixel[2], pixel[1], pixel[0], 255))  # Fully opaque for other colors

output_directory = "poetry/pixelator/images"  # Ensure this directory exists

# Create the directory if it does not exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

name = "pixel"
#name = input("input name: ")
output_filename =name + ".png"
output_path = os.path.join(output_directory, output_filename)

# Save the image
image.save(output_path)

# Optional: Show the image
image.show()
