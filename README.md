# Hand Gesture Music Control

Hand Gesture Music Control is an Opencv-Python program that allows you to control music playback using hand gestures captured through a webcam. The program uses the Mediapipe library for hand tracking and Osascript for interacting with the Music application on MacOS.

## Features

- **Volume Control:** Adjust the volume dynamically by altering the distance between your left hand's index finger and thumb. Increase the distance to raise the volume, and decrease it to lower the volume, with a maximum and minimum limit.
- **Play/Pause:** Effortlessly manage music playback with simple hand gestures. Fully close your right fist to pause the music. Open your right fist entirely, displaying your palm and extended fingers, to resume playback.
- **Next/Previous Track:** Navigate through tracks seamlessly using distinct hand gestures. Close your right fist completely, leaving only the thumb extended, to play the previous track. To play the next track, close your right fist with both the thumb and index finger fully extended.
  
## Prerequisites

- Python 3.x
- OpenCV
- Mediapipe
- Osascript

## Install the required dependencies

- pip install opencv-python
- pip install mediapipe
- pip install osascript
