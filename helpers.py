from concurrent.futures import ProcessPoolExecutor
import asyncio
import base64
import pytesseract
from PIL import Image
import numpy as np
import cv2


pytesseract.pytesseract.tesseract_cmd = r"./Tesseract-OCR/tesseract.exe"


def _decodeBase64String(base64String):
    image = base64.b64decode(base64String)
    npImage = np.frombuffer(image, dtype=np.uint8)
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
    base64_string = "".join(base64String.split(",")[1]).encode("utf-8")

    decodeded = _decodeBase64String(base64_string)
    manipulated = _manipulateImage(decodeded)
    textified = _getTextFromOCR(manipulated)

    return textified


async def processTextifyRequest(sio, sid, data):
    loop = asyncio.get_running_loop()

    print(f"[REQUEST RECEIVED] {sid}")

    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, getTextFromBase64, data)

        print(f"[PROCESSED] {sid}")

        await sio.emit("text", result, to=sid)