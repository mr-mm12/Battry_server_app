import cv2 as cv
import psutil
import time
import screen_brightness_control as sbc
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading
import sys

# Only use a single CPU core
p = psutil.Process()
p.cpu_affinity([0])

# Cascade Classifier for face detection
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv.CascadeClassifier(cascPath)
if faceCascade.empty():
    print("Error loading cascade classifier!")
    sys.exit()

# Open video capture (webcam)
cam = cv.VideoCapture(0)
if not cam.isOpened():
    print("Error opening video stream or file")
    sys.exit()

last_face_detected_time = time.time()

# Set initial screen brightness
initial_brightness = sbc.get_brightness()[0] if sbc.get_brightness() else 90

# Frame rate control (skip more frames to reduce CPU usage)
frame_skip = 20
frame_count = 0

# Minimum delay to reduce the processing frequency
frame_delay = 1.5

# Load your custom image for the icon
def load_icon_image():
    try:
        icon_image = Image.open("battry_icon.png")
        return icon_image
    except Exception as e:
        print("Error loading icon image:", e)
        return Image.new("RGB", (64, 64), (255, 255, 255))  # Fallback to a default image

def create_image():
    width = 64
    height = 64
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), fill="green")
    return image

def on_quit(icon, item):
    print("Exiting...")
    icon.stop()
    cam.release()
    cv.destroyAllWindows()

# Define icon menu
icon_menu = Menu(MenuItem('Quit', on_quit))
icon = Icon("Battery Saver", load_icon_image(), menu=icon_menu)

# Monitor face and adjust screen brightness accordingly
def monitor_face():
    global last_face_detected_time, frame_count
    while True:
        result, image = cam.read()
        if not result:
            print("Failed to grab frame")
            break

        frame_count += 1
        if frame_count % frame_skip != 0:
            continue
        
        # Convert image to grayscale only if no face detected in previous frame
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        # Perform face detection
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=4,
            minSize=(25, 30) 
        )

        # If no face detected, decrease brightness after a delay
        if len(faces) == 0:
            current_time = time.time()
            
            if current_time - last_face_detected_time > 30:
                current_brightness = sbc.get_brightness()
                if current_brightness:
                    new_brightness = max(5, current_brightness[0] - 5)
                    sbc.set_brightness(new_brightness)
                time.sleep(0.2)
        else:
            last_face_detected_time = time.time()
            sbc.set_brightness(initial_brightness)  # Restore brightness

        # Draw rectangle around detected face (for visualization)
        for (x, y, w, h) in faces:
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 5)

        # Sleep for a longer amount of time to reduce frequency of frame processing
        time.sleep(frame_delay)

# Start the face monitoring in a separate thread
face_thread = threading.Thread(target=monitor_face)
face_thread.daemon = True
face_thread.start()

# Run the icon menu
icon.run()
