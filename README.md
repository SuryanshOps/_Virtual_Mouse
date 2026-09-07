<div align="center">

# 🖱️ AI Virtual Mouse: Touchless Cursor Control

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange.svg)](https://google.github.io/mediapipe/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

*A Next-Generation Human-Computer Interface using Artificial Intelligence, Computer Vision, and Hand Biometrics.*

</div>

---

## 📖 Table of Contents
1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [System Architecture & Tech Stack](#-system-architecture--tech-stack)
4. [In-Depth Mechanism & Mathematics](#-in-depth-mechanism--mathematics)
5. [Prerequisites & Installation](#-prerequisites--installation)
6. [Usage Guide](#-usage-guide)
7. [Troubleshooting](#-troubleshooting)
8. [Future Roadmap](#-future-roadmap)
9. [Author](#-author)

---

## 🌌 Project Overview

Traditional hardware mice have been the standard for decades, but the future of human-computer interaction lies in spatial computing and touchless interfaces. This project bridges the gap between hardware limitations and software potential by creating a **Virtual AI Mouse**. 

By leveraging deep learning models for hand tracking, this application transforms any standard webcam into a highly precise, low-latency tracking device. You can navigate your operating system, browse the web, and execute clicks entirely through mid-air hand gestures. It is designed with accessibility, hygiene (touchless public kiosks), and futuristic UI experiences in mind.

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
| **PyAutoGUI / AutoPy** | Acts as the bridge to the Operating System, executing the actual mouse move and click commands. |

---

## 🧠 In-Depth Mechanism & Mathematics

To understand how physical gestures translate into digital actions, we must break down the pipeline into four critical computational steps.

### 1. Neural Hand Landmark Extraction
The webcam captures a frame (an array of pixels). This frame is converted from BGR (OpenCV's default) to RGB and passed into MediaPipe's hand tracking model. The model outputs 21 distinct `(x, y, z)` coordinates. 

For the Virtual Mouse, we isolate two specific nodes:
* **Node 8:** Index Finger Tip (The Navigator)
* **Node 4:** Thumb Tip (The Clicker)

### 2. The Virtual Boundary & Coordinate Interpolation
A webcam might capture video at `640 x 480` resolution, while your monitor might be `1920 x 1080`. If we mapped this 1:1, you could only reach a fraction of your screen. 

To fix this, we draw a **Virtual Bounding Box** inside the webcam feed. When your finger moves within this smaller box, NumPy's interpolation function linearly scales those coordinates to the full dimensions of your monitor. This allows full-screen traversal with minimal physical arm movement.

### 3. Euclidean Distance for Click Detection
To determine if a user intends to click, the system continuously calculates the spatial distance between the tip of the Index Finger (Node 8) and the tip of the Thumb (Node 4). 

This is achieved using the standard Euclidean distance formula:

`d = √((x2 - x1)² + (y2 - y1)²)`

Where:
* `(x1, y1)` are the coordinates of the Index Finger tip.
* `(x2, y2)` are the coordinates of the Thumb tip.

When `d` falls below a rigorously tested threshold (e.g., `< 40` pixels), the system registers a "Pinch" and triggers the OS-level click event. A cooldown flag is implemented immediately after to prevent accidental rapid-fire double clicks.

### 4. Low-Pass Filtering (Jitter Stabilization)
Because webcam feeds are subject to sensor noise and fluctuating lighting, raw coordinates jump around slightly frame-to-frame. Without smoothing, the cursor would aggressively vibrate.

We apply a moving average filter to the coordinates:
`Current_X = Previous_X + ((Target_X - Previous_X) / Smoothing_Factor)`

This mathematical "drag" dampens sudden micro-movements, resulting in a cursor that feels heavy, fluid, and precise—mimicking the physical friction of a real mouse on a mousepad.

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
git clone [https://github.com/yourusername/ai-virtual-mouse.git](https://github.com/yourusername/ai-virtual-mouse.git)
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
