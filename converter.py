import numpy as np
import cv2
import math
import json

with open('data.json', 'r') as f:
    json_string = f.read()

data = json.loads(json_string)

scale_factor = 0.3

char = '@#ADBI!i+*^"\' '[::-1]
# char = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{/}[]?-_+~<>i!lI;:,"^`\'.'[::-1]

def get_character(n):
    charlist = list(char)
    interval = len(charlist)/256
    return charlist[math.floor(n*interval)]

def get_text_ASCII_art(path, file_name):
    one_character_height = 18
    one_character_width = 8
    img = cv2.imread(path, -1)
    img = cv2.resize(img, (0,0), fx=scale_factor, fy=scale_factor*one_character_width/one_character_height)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray_image.shape
    with open(file_name, 'w') as f:
        for i in range(h):
            for j in range(w):
                f.write(get_character(gray_image[i][j]))
            f.write('\n')

def get_jpg_ASCII_art(path):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.4
    font_thickness = 1
    textsize = cv2.getTextSize('@', font, font_scale, font_thickness)[0]
    char_width, char_height = textsize
    char_height= char_height + 4
    img = cv2.imread(path, -1)
    img = cv2.resize(img, (0,0), fx=scale_factor, fy=scale_factor*char_width/char_height)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray_image.shape
    image = np.zeros((char_height*h,char_width*w,3), np.uint8)
    for i in range(h):
        for j in range(w):
            b, g, r = img[i][j]
            b = int(b)
            g = int(g)
            r = int(r)
            image = cv2.putText(image, get_character(gray_image[i][j]), (j*char_width,(i+1)*char_height), font, font_scale, (b,g,r), font_thickness, cv2.LINE_AA)
    return image



if __name__ == "__main__":
    while True:
        name = input('Complete name of image file in input_image directory : ')
        try :
            image_name = name.split('.')[0]
            path = data['path_of_input_folder'] + name
            text_file_name = data['path_of_ASCII_art_text'] + image_name + '_ASCII_art.text'
            image_file_name = data['path_of_ASCII_art_image'] + image_name + '_ASCII_art.jpg'
            get_text_ASCII_art(path, text_file_name)
            image = get_jpg_ASCII_art(path)
            cv2.imwrite(image_file_name, image)
            print('Your image is converted and saved')
            break
        except Exception as e:
            if name == 'exit':
                break
            else:
                print('Your image is not present in the input_image directory or the name is invalid \nenter a valid name of the image or enter exit to exit\n')
        

