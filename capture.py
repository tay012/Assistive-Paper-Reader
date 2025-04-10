import cv2
import time

def capture_image():
    cap = cv2.VideoCapture(0)
    time.sleep(1)  # Warm up the camera
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("❌ Failed to capture image")
        return None

    filename = f"capture_{int(time.time())}.jpg"
    cv2.imwrite(filename, frame)
    print(f"✅ Image saved as {filename}")
    return filename
