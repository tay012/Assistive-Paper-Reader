import easyocr
import subprocess
import cv2
import os
from datetime import datetime

reader = easyocr.Reader(['en'], gpu=False)
volume = 100  # default volume

def process_image(image_path):
    if image_path is None:
        return

    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    results = reader.readtext(thresh)

    print("📖 Reading out text...")
    spoken_text = ""

    for _, text, _ in results:
        print(f"Detected: {text}")
        spoken_text += text + "\n"
        subprocess.run(["espeak", f"-a {volume}", text])

    save_text(image_path, spoken_text)

def save_text(image_path, text):
    if not os.path.exists("texts"):
        os.mkdir("texts")

    base = os.path.basename(image_path).split(".")[0]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"texts/{base}_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(text)

    print(f"💾 Text saved to {filename}")
