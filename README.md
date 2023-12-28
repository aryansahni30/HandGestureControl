# Hand Gesture Music Control

Hand Gesture Music Control is an Opencv-Python program that allows you to control music playback using hand gestures captured through a webcam. The program uses the Mediapipe library for hand tracking and Osascript for interacting with the Music application on MacOS.

## Features

- **Volume Control:** Control the volume by adjusting the distance between your index finger and thumb of your left hand. As the distance increases, the volume will also increase upto max and vice versa. 
- **Play/Pause:** To pause music, close your right fist entirely. To play music, open your right fist completely, showing your palm and fingers stretched out.
- **Next/Previous Track:** Close your right fist completely with only thumb stretched out to play the previous track. To play the next track, close your right fist, with thumb and index finger, both stretched out.
  
## Prerequisites

- Python 3.x
- OpenCV
- Mediapipe
- Osascript

## Install the required dependencies

- pip install opencv-python
- pip install mediapipe
- pip install osascript
