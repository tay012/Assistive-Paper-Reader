# 📬 Angel's Mail Reader (Capstone Project - CPSC 498)

A Raspberry Pi–based assistive device that allows visually impaired users (like Ray's mom!) to place a document under a camera, press a button, and hear the content read aloud using OCR and text-to-speech.

---

## 🎯 Goals

- Provide an accessible, standalone tool for reading mail or documents aloud
- Enable single-button use for ease of operation
- Speak all outputs using onboard TTS (eSpeak)
- Track temperature and announce warnings to prevent hardware issues
- Maintain logs and backups of scanned content
- Serve as a platform for adding future accessibility features

---

## 💡 Key Features

- 🖼️ Camera capture via button press
- 🧠 Optical Character Recognition (OCR) using EasyOCR
- 🔊 Audio feedback with espeak
- ⏯️ Play/pause and volume toggle buttons
- 🌡️ CPU temperature monitoring with spoken warnings
- 📝 Optional saving of text files and sending to phone (stretch goal)
- 🔁 Full offline support – no screen required

---

## 📦 Project Structure

capstone-proposal-s25/ ├── main.py # Main button loop ├── capture.py # Captures image from camera ├── ocr_reader.py # OCR processing + espeak output ├── audio_controller.py # Play/pause/volume logic ├── welcome.py # Startup greeting script ├── requirements.txt # All Python package dependencies └── README.md # This file!


---

## 🚀 Setup Instructions

### ✅ 1. Set Up Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


If needed:
sudo apt install python3-opencv espeak python3-pip python3-dev


✅ 2. Enable Auto-Run on Boot (via crontab)
crontab -e
Add:
@reboot /home/pi/venv/bin/python /home/pi/capstone-proposal-s25/welcome.py
@reboot /home/pi/venv/bin/python /home/pi/capstone-proposal-s25/main.py

To test manually:

source venv/bin/activate
python main.py


👩‍💻 Contributors

Angel Taylor – Developer & Designer
Angel’s Mom – The inspiration 💛
