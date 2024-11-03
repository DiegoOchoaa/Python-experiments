import cv2 as cv
import time

INTENSITY = " $@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
INTENSITY = " $@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'.                              "
poem ="""If we ourselves are valued by intelligence,
All throughout the ages,
We use our negligence,
We encase pigs in cages, 
Pen animals in zoos,
Use horses as transportation,
Our trees fall for our jewels,
If something surpasses our civilization,
Does it possess the right to rule,
Is wisdom what makes us masters
If something larger were to rise,
Something brilliant past our matters,
Would it be our demise.
.
"""
# Load the image
original_img = cv.imread('/Users/diegoochoa/Documents/python/poetry/cuplt.png')

# Define pixel size for pixelation
pixel_size = 8

# Map a grayscale value to an intensity character
def map_value(value, old_min, old_max, new_min, new_max):
    return int(new_min + (value - old_min) * (new_max - new_min) / (old_max - old_min))


# Pixelate and convert to grayscale
def pixelate_image(img, pixel_size):
    height, width = img.shape[:2]
    img_resized = cv.resize(img, (width // pixel_size, height // pixel_size), interpolation=cv.INTER_LINEAR)
    return cv.cvtColor(img_resized, cv.COLOR_BGR2GRAY)


pixelated_img = pixelate_image(original_img, pixel_size)
# Loop over each row
index = 0
notspace = 0
for i, row in enumerate(pixelated_img):
        
    # Loop over each pixel in the row
    for j, pixel in enumerate(row):
       
        
        if pixel > 90:
            index += 1
            if index > len(poem)-1:
                index = 0
            letter = poem[index]
            if letter == '\n':
                letter = " "
            print(letter, end='',flush=True)
            print(' ', end='')
            time.sleep(0.0006)
        else:
            print('  ', end='')
            
   
    print("")

        
