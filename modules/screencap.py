# modules/screencap.py

import mss
import cv2
import numpy as np
from datetime import datetime
import os

OUTPUT_DIR = "outputs/screenshots"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def capture_screen():

    with mss.mss() as sct:

        monitor = sct.monitors[1]

        screenshot = sct.grab(monitor)

        img = np.array(screenshot)

        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_path = f"{OUTPUT_DIR}/screen_{timestamp}.png"

        cv2.imwrite(file_path, img)

        print(f"[INFO] Screenshot saved: {file_path}")

        return file_path