import time
import threading
import subprocess

# Try to import GPIO — fallback if not on real Pi or GPIO fails
try:
    import RPi.GPIO as GPIO
    gpio_enabled = True
except (ImportError, RuntimeError):
    print("⚠️ GPIO not available — running in test mode")
    gpio_enabled = False

# Import other scripts (assuming they exist)
from capture import capture_image
from ocr_reader import process_image
from audio_controller import pause_or_resume_speech, toggle_volume_mode

# === BUTTON PIN SETUP ===
CAPTURE_BUTTON = 17       # Press to capture and read
PAUSE_BUTTON = 27         # Play/Pause TTS
VOLUME_BUTTON = 22        # Toggle volume modes

# === SETUP GPIO ===
def setup_buttons():
    if not gpio_enabled:
        return
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CAPTURE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PAUSE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(VOLUME_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# === TEMP MONITOR ===
def check_temperature_periodically():
    def monitor():
        while True:
            temp_output = subprocess.run(
                ["vcgencmd", "measure_temp"],
                capture_output=True, text=True
            )
            try:
                temp_str = temp_output.stdout.strip().split('=')[1].replace("'C", "")
                temp = float(temp_str)
                if temp >= 75:
                    print(f"🔥 WARNING: High temperature detected: {temp}°C")
                    subprocess.run(["espeak", "Warning. I am feeling a bit warm. Please check my ventilation."])
            except Exception as e:
                print(f"[Temp Monitor] Error: {e}")
            time.sleep(30)
    threading.Thread(target=monitor, daemon=True).start()

# === MAIN BUTTON LOOP ===
def real_loop_buttons():
    try:
        while True:
            if GPIO.input(CAPTURE_BUTTON) == GPIO.LOW:
                print("📸 Capture button pressed")
                subprocess.run(["espeak", "Taking picture. Please hold still."])
                image_path = capture_image()
                process_image(image_path)
                subprocess.run(["espeak", "Done reading. Ready for more mail."])
                time.sleep(1)

            if GPIO.input(PAUSE_BUTTON) == GPIO.LOW:
                print("⏯️ Pause/Play button pressed")
                pause_or_resume_speech()
                time.sleep(0.5)

            if GPIO.input(VOLUME_BUTTON) == GPIO.LOW:
                print("🔊 Volume button pressed")
                toggle_volume_mode()
                time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()

# === FALLBACK LOOP FOR TESTING ===
def loop_buttons():
    if not gpio_enabled:
        print("🔁 GPIO disabled — skipping button loop")
        while True:
            time.sleep(5)  # Stay alive
    else:
        real_loop_buttons()

# === STARTUP ===
if __name__ == "__main__":
    print("🟢 Capstone Reader is starting up...")
    subprocess.run(["espeak", "Capstone Reader ready. Press the big button to begin."])
    setup_buttons()
    check_temperature_periodically()
    loop_buttons()
