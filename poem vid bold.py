import cv2 as cv
import time
import os

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

INTENSITY = " $@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'.                                            "
poem = """We're no strangers to love
You know the rules and so do I (do I)
A full commitment's what I'm thinking of
You wouldn't get this from any other guy
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
We've known each other for so long
Your heart's been aching, but you're too shy to say it (say it)
Inside, we both know what's been going on (going on)
We know the game and we're gonna play it
And if you ask me how I'm feeling
Don't tell me you're too blind to see
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
We've known each other for so long
Your heart's been aching, but you're too shy to say it (to say it)
Inside, we both know what's been going on (going on)
We know the game and we're gonna play it
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
"""

# Load the video
vid = '/Users/diegoochoa/Documents/python/poetry/never_gonna_gup.mp4'
cap = cv.VideoCapture(vid)

# Define pixel size for pixelation
pixel_size =30

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
                letter = poem[index-1]
                
                
                index += 1
                if letter == "\n":
                    line += " "
                else:
                    if pixel > 20:
                        line += '\033[2m'+letter+'\033[0m'
                    

                    else:
                        line += ' '
               
     
  
     
                line += " " 


            
                
        output.append(line)
    
    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print the frame
    
    print("\n".join(output))
    t+=1
    print(t)
    
    # Small delay to smooth the display
    time.sleep(0.03)
    index = 0

cap.release()
