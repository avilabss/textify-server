import cv2
import base64
import numpy as np
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"./Tesseract-OCR/tesseract.exe"

def _decodeBase64String(base64String):
    image = base64.b64decode(base64String); 
    npImage = np.frombuffer(image, dtype=np.uint8); 
    source = cv2.imdecode(npImage, 1) 

    return source

def _manipulateImage(npArray):
    grayImage = cv2.cvtColor(npArray, cv2.COLOR_BGR2GRAY)

    # cv2.imwrite("out.png", grayImage) # Test ManipulateImage by Saving
    return grayImage

def _getTextFromOCR(npArray):
    with Image.fromarray(npArray) as image:
        text = pytesseract.image_to_string(image, lang="eng")
    
    correctedText = "".join(text[:-2])

    return correctedText

def getTextFromBase64(base64String):
    decodeded = _decodeBase64String(base64String)
    manipulated = _manipulateImage(decodeded)
    textified = _getTextFromOCR(manipulated)

    return textified

# with open("in.png", "rb") as image_file:
#     encoded_string = base64.b64encode(image_file.read())

# print(getTextFromBase64(encoded_string))
