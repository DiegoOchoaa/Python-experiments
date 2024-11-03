import cv2 as cv
import time
import os

INTENSITY = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzc     vunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'.                                            "
poem = """PERHAPS the sentiments contained in the following pages, are not yet
sufficiently fashionable to procure them general favor; a long habit of
not thinking a thing wrong, gives it a superficial appearance of being
right, and raises at first a formidable outcry in defence of custom. But
the tumult soon subsides. Time makes more converts than reason.
As a long and violent abuse of power, is generally the Means of
calling the right of it in question (and in Matters too which might
never have been thought of, had not the Sufferers been aggravated
into the inquiry) and as the K- of England hath undertaken in his
own Right, to support the Parliament in what he calls Theirs, and as
the good people of this country are grievously oppressed by the
combination, they have an undoubted privilege to inquire into the
pretensions of both, and equally to reject the usurpation of either.
In the following sheets, the author has studiously avoided every
thing which is personal among ourselves. Compliments as well as
censure to individuals make no part thereof. The wise and the worthy need not the triumph of a pamphlet; and those whose sentiments
are injudicious, or unfriendly, will cease of themselves unless too
much pains is bestowed upon their conversion.
The cause of America is in a great measure the cause of all
mankind. Many circumstances hath, and will arise, which are not
local, but universal, and through which the principles of all Lovers
of Mankind are affected, and in the Event of which their Affections
are interested. The laying a Country desolate with Fire and Sword,
declaring War against the natural rights of all Mankind, and extirpating the Defenders thereof from the Face of the Earth, is the Concern of every man to whom Nature hath given the Power of feeling; of which Class, regardless of Party Censure, is the
A
"""

# Load the video
original_img = cv.imread('/Users/diegoochoa/Documents/python/poetry/cage.png')


# Define pixel size for pixelation
pixel_size =10

# Map a grayscale value to an intensity character
def map_value(value, old_min, old_max, new_min, new_max):
    return int(new_min + (value - old_min) * (new_max - new_min) / (old_max - old_min))

# Pixelate and convert to grayscale
def pixelate_image(img, pixel_size):
    height, width = img.shape[:2]
    img_resized = cv.resize(img, (width // pixel_size, height // pixel_size), interpolation=cv.INTER_LINEAR)
    return cv.cvtColor(img_resized, cv.COLOR_BGR2GRAY)

index = 1



pixelated_img = pixelate_image(original_img, pixel_size)
output = []

# Loop over each row
for row in pixelated_img:
        line = ""
        letters = 0
        
        # Loop over each pixel in the row
        for pixel in row:
            intensity = INTENSITY[map_value(int(pixel), 0, 255, 0, len(INTENSITY) - 1)]
            if index > len(poem)-1:
                index = 0
            
            if pixel > 10:
                letter = poem[index-1]
                index +=1 
                if letter == "\n":
                    line += " "
                    print(" ", end="", flush=True)
                else:
                    line += letter
                    print(letter, end="", flush=True)
                    time.sleep(0.0006)
                    letters += 1
                if letter == " ":
                 for i in range(letters):
                    line += " "
                    print(" ", end="", flush=True)
                 letters = 0
                    
                
            else:
                line += "  "
                print("  ", end="", flush=True)
            
            
        print("")


       
    

 

