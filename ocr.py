#
# import easyocr
# import cv2
# import pyttsx3  # For text-to-speech
#
# # Initialize TTS engine
# engine = pyttsx3.init()
#
# # Example of reading an image and getting text
# reader = easyocr.Reader(['en'], gpu=False)
# result = reader.readtext('/Users/angeltay/Desktop/Testimg1.jpeg')
#
# # Load the image
# img = cv2.imread('/Users/angeltay/Desktop/Testimg1.jpeg')
#
# for detection in result:
#     bbox, text, confidence = detection
#
#     # Extract the top-left and bottom-right points
#     top_left = (int(bbox[0][0]), int(bbox[0][1]))
#     bottom_right = (int(bbox[2][0]), int(bbox[2][1]))
#
#     # Draw the rectangle
#     cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 3)
#
#     # Put the text on the image
#     cv2.putText(img, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
#
#     # Read the text aloud
#     engine.say(f": {text}")
#
# # Finish the text-to-speech and close the engine
# engine.runAndWait()
#
# # Display the image
# cv2.imshow('Result', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()




# import sys
# import easyocr
# import cv2
# import pyttsx3  # For text-to-speech

# # Initialize TTS
# engine = pyttsx3.init()

# # Initialize the camera (0 is usually the default for the webcam)
# cap = cv2.VideoCapture(0)

# if not cap.isOpened():
#     print("Error: Could not open camera.")
#     exit()

# print("Press 's' to capture an image and process it.")
# print("Press 'q' to quit.")

# while True:
#     # Read a frame from the camera
#     ret, frame = cap.read()

#     if not ret:
#         print("Failed to grab frame.")
#         break

#     # Show the live camera feed
#     cv2.imshow("Camera Feed - Press 's' to Capture", frame)

#     # Wait for user input
#     key = cv2.waitKey(1) & 0xFF

#     if key == ord('s'):  # If 's' is pressed, capture the image
#         captured_image = frame.copy()
#         cv2.imwrite("captured_image.jpg", captured_image)
#         print("Image captured!")

#         # Process the captured image with EasyOCR
#         reader = easyocr.Reader(['en'], gpu=False)
#         result = reader.readtext(captured_image)

#         for detection in result:
#             bbox, text, confidence = detection

#             # Extract the top-left and bottom-right points
#             top_left = (int(bbox[0][0]), int(bbox[0][1]))
#             bottom_right = (int(bbox[2][0]), int(bbox[2][1]))

#             # Draw the rectangle around detected text
#             cv2.rectangle(captured_image, top_left, bottom_right, (0, 0, 255), 3)

#             # Put the recognized text on the image
#             cv2.putText(captured_image, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

#             # Read the text aloud
#             engine.say(text)

#         # Finish the text-to-speech processing
#         engine.runAndWait()

#         # Show the image with detected text
#         cv2.imshow("Processed Image", captured_image)
#         cv2.waitKey(0)

#     elif key == ord('q'):  # Press 'q' to quit
#         break


# cap.release()
# cv2.destroyAllWindows()


import sys
import os
import cv2
import easyocr
import pyttsx3
from pdf2image import convert_from_path
from PIL import Image
import numpy as np

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Check for file input
if len(sys.argv) < 2:
    print("Usage: python ocr.py <image_or_pdf_path>")
    sys.exit(1)

input_path = sys.argv[1]

# Make sure the file exists
if not os.path.exists(input_path):
    print(f"Error: File not found at {input_path}")
    sys.exit(1)

# Convert PDF to image if needed
if input_path.lower().endswith(".pdf"):
    print("PDF detected. Converting first page to image...")
    images = convert_from_path(input_path, dpi=150, thread_count=1)
    if not images:
        print("Error: Could not convert PDF to image.")
        sys.exit(1)
    image_path = "temp_page.png"
    images[0].save(image_path, "PNG")
else:
    image_path = input_path

# Load image with OpenCV
image = cv2.imread(image_path)
if image is None:
    print(f"Error: Could not load image: {image_path}")
    sys.exit(1)

# Pre-process image for better OCR
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Use EasyOCR
reader = easyocr.Reader(['en'], gpu=False)
results = reader.readtext(thresh)

# Draw and speak text
for bbox, text, confidence in results:
    top_left = tuple(map(int, bbox[0]))
    bottom_right = tuple(map(int, bbox[2]))
    cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)
    cv2.putText(image, text, (top_left[0], top_left[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    print(f"Detected: {text}")
    engine.say(text)

engine.runAndWait()

# Save final image instead of displaying (for headless Pi)
cv2.imwrite("ocr_result.png", image)
print("OCR result saved as ocr_result.png")

# Cleanup temporary file
if input_path.lower().endswith(".pdf"):
    os.remove(image_path)
