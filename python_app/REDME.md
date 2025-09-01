# Face-Aware Screen Brightness 💡

A **Python application** that intelligently adjusts your screen brightness based on face detection from your webcam.  
This project helps **save energy** and reduce eye strain by automatically dimming the screen when you're away and restoring brightness when you're present.

---

## Features ✨
- **Real-time face detection** using OpenCV.  
- **Automatic brightness control** with `screen_brightness_control`.  
- Optimized **CPU usage** (single core + frame skipping).  
- **System tray icon** for easy exit and control.  
- Visual feedback: rectangles drawn around detected faces.

---

## Requirements 🛠️
- Python 3.x  
- Libraries:
  - `opencv-python`
  - `psutil`
  - `screen_brightness_control`
  - `pystray`
  - `Pillow`

---

## How It Works ⚙️
1. Captures video frames from your webcam.  
2. Detects faces using a **Haar Cascade Classifier**.  
3. If a face is detected:  
   - Sets screen brightness to the initial level.  
4. If no face is detected for a while:  
   - Gradually decreases screen brightness to save energy.  
5. Runs in the **system tray** for minimal interference.

---

## Usage 🚀
1. Make sure `haarcascade_frontalface_default.xml` is in the same folder.  
2. Place your custom tray icon as `battry_icon.png` (optional).  
3. Run the script:  
```bash
python face_brightness.py
