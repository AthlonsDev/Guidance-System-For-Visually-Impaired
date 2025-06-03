# Guidance System for the Visually Impaired

This project is a wearable assistive device designed to help visually impaired users navigate their environment independently and safely. It combines embedded systems, distance sensors, haptic feedback, and a deep learning-enabled edge device to provide real-time object detection and spatial awareness.

## Overview

The system uses microcontrollers and distance sensors to detect nearby obstacles and provides feedback to the user through haptic actuators. An NVIDIA Jetson platform runs a YOLO object detection model locally, enabling the device to recognize and classify objects in real-time without relying on cloud services. The entire setup is integrated into a wearable form factor for hands-free operation.

This project was developed as part of my final year dissertation and was recognized as one of the top projects of the year.

## Features

- Real-time object detection using YOLOv4 on an NVIDIA Jetson device  
- Distance sensing with ultrasonic sensors  
- Haptic feedback for obstacle notification  
- Fully offline operation using edge computing  
- Embedded system programming in C++ and Python  
- ~95% spatial awareness accuracy across diverse environments  
- Optimized for performance, with a 30% efficiency improvement on the Jetson platform  

## Tech Stack

- **Languages:** Python, C++  
- **Deep Learning:** YOLOv4 via Darknet  
- **Platform:** NVIDIA Jetson (running Arch Linux)  
- **Microcontrollers:** [e.g., Arduino Nano, ESP32 – please update based on your setup]  
- **Sensors:** Ultrasonic Distance Sensors (e.g., HC-SR04)  
- **Feedback:** Vibration motors / Haptic actuators  

## Setup & Installation

This repository is intended for educational and reference purposes. Due to its reliance on hardware components, full setup requires:

- An NVIDIA Jetson device (e.g., Jetson Nano)
- Compatible ultrasonic sensors
- A microcontroller (e.g., Arduino or ESP32)
- Haptic feedback motors
- Basic soldering and circuit assembly skills

### Software Setup

> ⚠️ This project is not fully plug-and-play. It assumes you have the hardware and basic embedded development experience.

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AthlonsDev/Guidance-System-For-Visually-Impaired.git
   cd Guidance-System-For-Visually-Impaired
2. Jetson Setup
   Install dependencies on Jetson (Python, OpenCV, Darknet)
   Compile Darknet with GPU and OpenCV support
   Follow instructions in the /jetson/ folder (if available)

3. Microcontroller Code
   Flash the code from /microcontroller/ to your board
   Connect sensors and actuators as per wiring diagrams (to be added if not present)

4. Python Scripts
   Used for integration and testing
   Install requirements (if applicable):
   pip install -r requirements.txt


Results
Achieved ~95% accuracy in obstacle detection and object recognition (depends on device's computing power)

30% increase in performance efficiency on the Jetson through model and code optimization

Successfully tested in diverse indoor and outdoor environments

Demo


Acknowledgements
Developed as part of my final year dissertation at [Your University Name]. Special thanks to mentors and peers for their valuable input.

License
This project is licensed under the MIT License.
