# modules/ocr.py

import easyocr
import cv2

reader = easyocr.Reader(['en'])

def preprocess_image(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.threshold(
        gray,
        150,
        255,
        cv2.THRESH_BINARY
    )[1]

    return gray


def extract_text(image_path):

    img = cv2.imread(image_path)

    processed_img = preprocess_image(img)

    results = reader.readtext(processed_img)

    extracted_text = []

    for result in results:

        text = result[1]

        extracted_text.append(text)

    return " ".join(extracted_text)