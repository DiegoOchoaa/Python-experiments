import cv2 as cv



cam = cv.VideoCapture(0)
INTENSITY = "N@#W$9876543210?!abc;:+=-,._' "
INTENSITY = "  '.-,=+;:cba?!0123456789$W#@N"



original_img = cv.imread('/Users/diegoochoa/Documents/python/text_images/3-duck-png-image.png')
result, original_img = cam.read()
height, width = original_img.shape[:2]
pixel_size =20

def map_value(value, old_min, old_max, new_min, new_max):
    return new_min + (value - old_min) * (new_max - new_min) // (old_max - old_min)

def make_img_list(img):
    pixel_values = []
    for x in range(img.shape[0]):  
        pixel_values.append([])
        for y in range(img.shape[1]):
            value = img[x][y]
            new_value = map_value(value, 0, 255, 0, len(INTENSITY)-1 )
            pixel_values[x].append(new_value)
        


    return pixel_values


def print_img(pixel_values):

    for row in range(len(pixel_values)):
        print('')
        for col in range(len(pixel_values[0])):
            print(INTENSITY[pixel_values[row][col]], end = ' ')


    



def pixelate(img, pixel_size):
    height, width = original_img.shape[:2]
    
    
    
 
    new_width, new_height = width // pixel_size, height // pixel_size
 

    img_temp = cv.resize(original_img, (new_width, new_height), interpolation=cv.INTER_LINEAR)
    #img_output =  cv.resize(img_temp, (width//2, height//2), interpolation=cv.INTER_NEAREST)
    grayscale = cv.cvtColor(img_temp, cv.COLOR_BGR2GRAY)
    return new_width, new_height, grayscale







while True:
    result, original_img = cam.read()
    new_w,new_h, img = pixelate(original_img, pixel_size)
    pixel_valuse = make_img_list(img)
    print_img(pixel_valuse)
    
    
    #cv.imshow("output", cv.resize(img, (width//2, height//2), interpolation=cv.INTER_NEAREST))
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


