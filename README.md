<div align="center">

# 🖱️ AI Virtual Mouse: Touchless Cursor Control

<!-- Replace 'assets/demo.gif' with the path to your actual GIF once you record it -->
<img src="assets/demo.gif" alt="AI Virtual Mouse Demo" width="700" style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">

<br>

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange.svg)](https://google.github.io/mediapipe/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*A Next-Generation Human-Computer Interface using Artificial Intelligence, Computer Vision, and Hand Biometrics.*

</div>

---

## 📖 Table of Contents
1. [Project Overview](#-project-overview)
2. [Video Demonstration](#-video-demonstration)
3. [Key Features](#-key-features)
4. [System Architecture & Tech Stack](#-system-architecture--tech-stack)
5. [In-Depth Mechanism & Mathematics](#-in-depth-mechanism--mathematics)
6. [Prerequisites & Installation](#-prerequisites--installation)
7. [Usage Guide](#-usage-guide)
8. [Troubleshooting](#-troubleshooting)
9. [Future Roadmap](#-future-roadmap)

---

## 🌌 Project Overview

Traditional hardware mice have been the standard for decades, but the future of human-computer interaction lies in spatial computing and touchless interfaces. This project bridges the gap between hardware limitations and software potential by creating a **Virtual AI Mouse**. 

By leveraging deep learning models for hand tracking, this application transforms any standard webcam into a highly precise, low-latency tracking device. You can navigate your operating system, browse the web, and execute clicks entirely through mid-air hand gestures. It is designed with accessibility, hygiene (touchless public kiosks), and futuristic UI experiences in mind.

---

## 🎥 Video Demonstration

<!-- Replace YOUR_YOUTUBE_VIDEO_ID with the actual ID of your YouTube video. -->
[![Watch the Demo](https://img.youtube.com/vi/YOUR_YOUTUBE_VIDEO_ID/maxresdefault.jpg)](https://youtu.be/YOUR_YOUTUBE_VIDEO_ID)

> **Click the image above to watch the full technical walkthrough and live demonstration on YouTube!**

---

## ✨ Key Features

* **Real-Time Hand Tracking:** Detects 21 3D hand landmarks in milliseconds using optimized machine learning models.
* **Frictionless Cursor Navigation:** Pinpoint accuracy achieved by tracking the absolute tip of your index finger.
* **Pinch-to-Click Mechanism:** Seamlessly execute left-clicks by pinching your index finger and thumb together.
* **Mathematical Jitter Reduction:** Built-in low-pass filtering to ensure the cursor glides smoothly without the vibrating effect common in raw webcam data.
* **Dynamic Resolution Scaling:** Intelligently maps the low-resolution webcam coordinate space to your high-resolution monitor space (e.g., 4K or 1080p).
* **Live FPS Counter:** Real-time performance monitoring displayed directly on the video feed.

---

## 🏗️ System Architecture & Tech Stack

This project is built on a modular Python architecture, utilizing state-of-the-art computer vision libraries:

| Technology | Purpose in Project |
| :--- | :--- |
| **Python** | The core programming language powering the logic, loops, and system calls. |
| **OpenCV (cv2)** | Handles video I/O, frame-by-frame image processing, and drawing UI overlays on the screen. |
| **Google MediaPipe** | Provides the pre-trained neural network for robust, real-time hand and finger landmark detection. |
| **NumPy** | Performs high-speed array operations and mathematical interpolations for coordinate mapping. |
| **PyAutoGUI** | Acts as the bridge to the Operating System, executing the actual mouse move and click commands. |

---

## 🧠 In-Depth Mechanism & Mathematics

Translating three-dimensional human motion into a precise two-dimensional digital cursor requires a robust pipeline of computer vision models, linear algebra, and digital signal processing. Here is the exact breakdown of the system's underlying logic.

### 1. Two-Stage Neural Network Pipeline (MediaPipe)
The system uses a two-stage pipeline for extreme efficiency:
* **BlazePalm Detector:** A lightweight model first scans the entire webcam frame to locate the bounding box of a palm.
* **Hand Landmark Model:** Once the palm is found, this secondary model analyzes that specific cropped region to predict exactly 21 3D points `(x, y, z)`.

The model outputs normalized coordinates between `[0.0, 1.0]`. To use these, we perform **Coordinate Denormalization** based on the webcam resolution:
* `Pixel_X = Normalized_X * Frame_Width`
* `Pixel_Y = Normalized_Y * Frame_Height`

For this project, we extract **Node 8** (Index Finger Tip) for movement and **Node 4** (Thumb Tip) for clicks.

### 2. The Active Tracking Region (Bounding Box Interpolation)
If we mapped the `640x480` webcam frame directly to a `1920x1080` monitor, the user would have to extend their arm wildly out of frame to reach the corners of their screen. 

To solve this, we define a smaller **Active Tracking Region** (e.g., a `400x300` rectangle) in the center of the camera feed. We then use **Linear Interpolation** to map this inner box to the full screen resolution.

The mathematical mapping function (handled by `numpy.interp`) works as follows:
`Screen_X = ((Cam_X - Box_X1) / (Box_X2 - Box_X1)) * Screen_Width`

### 3. Euclidean Distance & Hysteresis (Click State Machine)
To register a click, we calculate the magnitude of the vector connecting the Index Finger tip `(x1, y1)` and the Thumb tip `(x2, y2)`. This is done using the standard **Euclidean Distance Formula**:

`Distance = √((x2 - x1)² + (y2 - y1)²)`

However, relying on a single threshold (e.g., click if `Distance < 40`) causes a major bug: **Click Flickering**. If the user's distance hovers exactly at 40, the system rapidly spams clicks.

**The Solution: Hysteresis (State Debouncing)**
We implement a state machine with two different thresholds to create a buffer zone:
* If `Click_State` is FALSE and `Distance < 35` ➡️ Register Click, set `Click_State = TRUE`.
* If `Click_State` is TRUE and `Distance > 55` ➡️ Reset to unclicked, set `Click_State = FALSE`.
This ensures a deliberate pinch is required to click, and a deliberate release is required to reset it, eliminating accidental double-clicks.

### 4. Exponential Moving Average (Jitter Stabilization)
Webcam sensors are noisy. Lighting changes and pixel limitations mean that even if your hand is perfectly still, the raw coordinates will vibrate by 2-5 pixels every frame. 

To give the cursor a smooth, frictionless glide, we pass the raw coordinates through an **Exponential Moving Average (EMA) Low-Pass Filter**:

`Current_Position = (α * Target_Position) + ((1 - α) * Previous_Position)`
*(Where α is the smoothing factor, usually between 0.1 and 0.3)*

Alternatively written as a damping function:
`Current_X = Previous_X + ((Target_X - Previous_X) / Smoothing_Factor)`

This mathematical "drag" mimics the physical friction of a real mousepad, creating a natural user experience.

---

## ⚙️ Prerequisites & Installation

Follow these steps to deploy the AI Virtual Mouse on your local machine.

### Prerequisites
* A functional integrated or external webcam.
* Python 3.8 or higher installed on your system.
* Adequate room lighting (the neural network performs best in well-lit environments).

### Installation Steps

**1. Clone the Source Code**
Download the project repository to your local machine:
```bash
git clone https://github.com/SuryanshOps/_Virtual_Mouse.git
cd _Virtual_Mouse
```

**2. Isolate the Environment (Highly Recommended)**
Create a Python virtual environment to prevent dependency conflicts with your system Python:
```bash
# Create the environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

**3. Install Dependencies**
Install the required computer vision and automation packages:
```bash
pip install opencv-python mediapipe numpy pyautogui
```
*(Note: Mac users may need to grant IDE/Terminal accessibility permissions in System Preferences for PyAutoGUI to control the mouse).*

---

## 🚀 Usage Guide

1. Ensure your environment is active and dependencies are installed.
2. Run the entry point script:
   ```bash
   python main.py
   ```
3. A window will open showing your webcam feed. 
4. **To Move the Cursor:** Raise your hand and point your **Index Finger** upwards. Move it around the frame.
5. **To Click:** Bring your **Index Finger** and **Thumb** together in a pinching motion.
6. **To Exit:** Bring the webcam window into focus and press the `q` key on your keyboard.

---

## 🛠️ Troubleshooting

* **Lag or Low FPS:** Ensure your system has sufficient CPU/GPU resources. MediaPipe is highly optimized, but running it alongside heavy IDEs can cause throttling.
* **Cursor Stuck in Corner:** This happens if the program loses track of the hand landmarks. Keep your hand flat and facing the camera.
* **PyAutoGUI FailsSafeException:** If the cursor is thrown to the absolute corner of the screen (0,0), PyAutoGUI triggers a safety abort. Relaunch the script and keep your hand steady.

---

## 🗺️ Future Roadmap

* [ ] **Right-Click Functionality:** Implement a gesture using the index, middle, and thumb fingers.
* [ ] **Drag & Drop:** Maintain the pinch gesture to click and drag files across the desktop.
* [ ] **Volume Control:** Map the distance between the index and thumb to system volume when in a specific mode.
* [ ] **Multi-Monitor Support:** Dynamic mapping across dual-display setups.

---

<div align="center">
<b>Developed with 💡 by Suryansh Kushwaha</b><br>
<i>Exploring the intersection of Artificial Intelligence and Everyday Utilities.</i>
</div>
