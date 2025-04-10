import RPi.GPIO as GPIO
import time
from capture import capture_image
from ocr_reader import process_image
from audio_controller import toggle_volume_mode, pause_or_resume_speech

# GPIO pins
CAPTURE_BUTTON = 17
PAUSE_BUTTON = 27
SOUND_BUTTON = 22

def setup_buttons():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CAPTURE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PAUSE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SOUND_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def loop_buttons():
    try:
        while True:
            if GPIO.input(CAPTURE_BUTTON) == GPIO.LOW:
                print("📸 Capture button pressed")
                path = capture_image()
                process_image(path)
                time.sleep(1)

            if GPIO.input(PAUSE_BUTTON) == GPIO.LOW:
                print("⏯️ Pause/Play button pressed")
                pause_or_resume_speech()
                time.sleep(0.5)

            if GPIO.input(SOUND_BUTTON) == GPIO.LOW:
                print("🔊 Sound mode button pressed")
                toggle_volume_mode()
                time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()
