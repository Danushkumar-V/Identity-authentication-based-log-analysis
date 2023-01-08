import cv2
from functions import encoding as ed
import os

def do_encoding(imagedirpath):


    images = []

    imgclasses = []

    list_of_trainingimg = os.listdir(imagedirpath)

    for cl in list_of_trainingimg:
        curImg = cv2.imread(f'{imagedirpath}/{cl}')
        images.append(curImg)
        imgclasses.append(os.path.splitext(cl)[0])

    encodedimgs = ed.findEncodings(images)
    return encodedimgs , imgclasses