import cv2 as cv
import time
import os

INTENSITY = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'.                                            "
poem = """
As autumn descends in a slow steday drift,
they keep ourselves from fallling,
falling down the path so worn and weary,
Golden and red they scatter as whispers,
and a massive turkey on my plater,
ready to be devoured on a crater,
and I worry about these calls,
"""

# Load the video
vid = '/Users/diegoochoa/Documents/python/poetry/never_gonna_gup.mp4'
cap = cv.VideoCapture(vid)

# Define pixel size for pixelation
pixel_size =25

# Map a grayscale value to an intensity character
def map_value(value, old_min, old_max, new_min, new_max):
    return int(new_min + (value - old_min) * (new_max - new_min) / (old_max - old_min))

# Pixelate and convert to grayscale
def pixelate_image(img, pixel_size):
    height, width = img.shape[:2]
    img_resized = cv.resize(img, (width // pixel_size, height // pixel_size), interpolation=cv.INTER_LINEAR)
    return cv.cvtColor(img_resized, cv.COLOR_BGR2GRAY)

t = 0
index = 1
while True:
    ret, frame = cap.read()
    if not ret:
        break

    pixelated_img = pixelate_image(frame, pixel_size)
    output = []

    # Loop over each row
    for row in pixelated_img:
        line = ""

        
        # Loop over each pixel in the row
        for pixel in row:
            intensity = INTENSITY[map_value(int(pixel), 0, 255, 0, len(INTENSITY) - 1)]
            if index > len(poem)-1:
                index = 0
            
            if pixel > 95:
                letter = poem[index-1]
                index +=1 
                if letter == "\n":
                    line += " "
                else:
                    line += letter
     
  
     
                line += " "

                    
                
            else:
                
                line += "  "


            
                
        output.append(line)
    
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print the frame
    
    print("\n".join(output))
    t+=1
    print(t)
    
    # Small delay to smooth the display
    time.sleep(0.006)
    index = 0

cap.release()
