import cv2 as cv
import numpy as np
from PIL import Image
import pytesseract
import cv2
import os
import numpy as np
import re 
import moment
from datetime import datetime

#method to change the dpi of the image
def set_image_dpi(filepath):
    im = Image.open(filepath)
    length_x, width_y = im.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    im_resized = im.resize(size, Image.ANTIALIAS)
    file_name = "{}.png".format(os.getpid())
    im_resized.save(file_name, dpi=(300, 300))
    return file_name
#method to covent brg to hsv 
def using_hsv_extract(image_file):
    
    img = cv2.imread(image_file)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # define range of black color in HSV
    lower_val = np.array([0,0,0])
    upper_val = np.array([180,255,140])
    # Threshold the HSV image to get only black colors
    mask = cv2.inRange(hsv, lower_val, upper_val)
    # Bitwise AND mask and original image
    res = cv2.bitwise_and(img,img, mask = mask)
    # invert the mask to get black letters on white background
    res2 = cv2.bitwise_not(mask)
    return res2
#method to remove noise from the image
def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, 0)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return img
# method to get the text from image 
def extract_datetext(image):
    
    #save the gray image
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, image)

    # load the image as a PIL/Pillow image, apply OCR
    text = pytesseract.image_to_string(Image.open(filename))
    text = text.replace('\n', ' ').replace('\r', '')
    
    # date extraction pattern
    pat1 = r'(\b(0?[1-9]|[12]\d|30|31)[^\w\d\r\n\s:](0?[1-9]|1[0-2])[^\w\d\r\n\s:](\d{4}|\d{2})\b)'
    pat2 = r'(\b(0?[1-9]|1[0-2])[^\w\d\r\n\s:](0?[1-9]|[12]\d|30|31)[^\w\d\r\n\s:](\d{4}|\d{2})\b)'
    pat3 = r'(\b(0?[1-9]|[12]\d|30|31)[^\w\d\r\n\s:](0?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[^\w\d\r\n\s:](\d{4}|\d{2})\b)'
    pat4 = r'(\b(0?Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[^\w\d\r\n:](0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](\d{4}|\d{2})\b)'
    pat5 = r'(\b(\d{4})[^\w\d\r\n\s:](0?[1-9]|1[0-2])[^\w\d\r\n\s:](0?[1-9]|[12]\d|30|31)\b)'

    #combine all the five pattern
    combined_pat = r'|'.join((pat1, pat2, pat3, pat4, pat5))
    pattern = re.compile(combined_pat, re.IGNORECASE)
    #get the date
    extract_date = re.search(pattern,text)
    if extract_date is not None:
        date = extract_date.group()
    else:
        date = "empty"   
    return date

def date_extractor(file_path):
    image_file = set_image_dpi(file_path)
    image = remove_noise_and_smooth(image_file)
    date_text = extract_datetext(image)
    if date_text == "empty":
        image = using_hsv_extract(image_file)
        date_text = extract_datetext(image)
    
    if date_text == "empty":
        date_text = "null"
    else:
        date_text = moment.date(date_text).strftime('%Y-%m-%d')

    #remove the temporary file 
    os.remove(image_file)    

    return date_text







    

