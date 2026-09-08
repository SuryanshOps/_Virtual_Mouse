<div align="center">

# 🖱️ AI Virtual Mouse: Touchless Cursor Control

<!-- Replace 'assets/demo.gif' with the path to your actual GIF -->
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

By leveraging deep learning models for hand tracking, this application transforms any standard webcam into a highly precise, low-latency tracking device. You can navigate your operating system, browse the web, execute clicks, drag files, and open context menus entirely through mid-air hand gestures. It is designed with accessibility, hygiene (touchless public kiosks), and futuristic UI experiences in mind.

---

## 🎥 Video Demonstration

<!-- Replace YOUR_YOUTUBE_VIDEO_ID with the actual ID of your YouTube video. -->
[![Watch the Demo](https://img.youtube.com/vi/YOUR_YOUTUBE_VIDEO_ID/maxresdefault.jpg)](https://youtu.be/YOUR_YOUTUBE_VIDEO_ID)

## ✨ Key Features

* **Real-Time Hand Tracking:** Detects 21 3D hand landmarks in milliseconds using optimized machine learning models.
* **Frictionless Cursor Navigation:** Pinpoint accuracy achieved by tracking the absolute tip of your index finger.
* **Left-Click & Right-Click Mechanisms:** Execute primary clicks by pinching your index finger and thumb, and secondary context-menu clicks using your middle finger.
* **Fluid Drag & Drop:** Maintain a pinch gesture to lock the cursor, allowing you to intuitively drag files, windows, and sliders across the screen.
* **Mathematical Jitter Reduction:** Built-in low-pass filtering ensures the cursor glides smoothly without the vibrating effect common in raw webcam data.
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
| **PyAutoGUI** | Acts as the bridge to the Operating System, executing the actual mouse move, click, and drag commands. |

---

## 🧠 In-Depth Mechanism & Mathematics

Translating three-dimensional human motion into precise digital cursor manipulation requires a robust pipeline of computer vision models, linear algebra, and state-machine logic. Here is the exact breakdown of the system's underlying mechanisms.

### 1. Neural Network Pipeline & Landmark Extraction
The system uses MediaPipe's two-stage pipeline for extreme efficiency:
* **BlazePalm Detector:** A lightweight model first scans the entire frame to locate the bounding box of a palm.
* **Hand Landmark Model:** This secondary model analyzes the cropped palm region to predict exactly 21 3D points `(x, y, z)`.

The model outputs normalized coordinates `[0.0, 1.0]`. We perform **Coordinate Denormalization** based on the webcam resolution (`Pixel_X = Normalized_X * Frame_Width`). For this project, we extract:
* **Node 8:** Index Finger Tip (Navigation & Left Click)
* **Node 12:** Middle Finger Tip (Right Click)
* **Node 4:** Thumb Tip (The reference point for clicking)

### 2. The Active Tracking Region (Bounding Box Interpolation)
If we mapped the `640x480` webcam frame directly to a `1920x1080` monitor, the user would have to extend their arm wildly out of frame. To solve this, we define an **Active Tracking Region** in the center of the camera feed. 

We use **Linear Interpolation** to map this inner box to the full screen resolution:
`Screen_X = ((Cam_X - Box_X1) / (Box_X2 - Box_X1)) * Screen_Width`

### 3. Euclidean Distance & Gestural State Machines
All clicks are registered by calculating the vector magnitude between finger tips using the **Euclidean Distance Formula**:

`Distance = √((x2 - x1)² + (y2 - y1)²)`

To handle advanced functionality like Drag-and-Drop and prevent "Click Flickering," we implement strict state machines with **Hysteresis** (buffer zones):

* **Left Click (Node 8 & Node 4):**
  If `Distance < 35`, we trigger a left click. To prevent rapid double-clicks, the system must see the fingers separate (`Distance > 55`) before it arms the next click.
  
* **Right Click (Node 12 & Node 4):**
  Calculating the distance between the Middle Finger and Thumb allows us to independently trigger secondary `pyautogui.rightClick()` events.

* **Drag and Drop (Continuous State):**
  Instead of a single click event, dragging requires tracking sustained distance. 
  1. If Index & Thumb `Distance < 35` for a sustained period, trigger `pyautogui.mouseDown()`.
  2. The script continues updating the `X, Y` coordinates while the mouse state is physically held down.
  3. When `Distance > 55`, trigger `pyautogui.mouseUp()`, successfully dropping the item.

### 4. Exponential Moving Average (Jitter Stabilization)
Webcam sensors are noisy. To give the cursor a smooth, frictionless glide during movement and dragging, we pass the raw coordinates through an **Exponential Moving Average (EMA) Low-Pass Filter**:

`Current_Position = (α * Target_Position) + ((1 - α) * Previous_Position)`
*(Where α is the smoothing factor, usually between 0.1 and 0.3)*

This mathematical "drag" mimics the physical friction of a real mousepad, ensuring that when you are dragging a file, micro-jitters in the camera feed don't cause you to accidentally drop it.

---

## ⚙️ Prerequisites & Installation

Follow these steps to deploy the AI Virtual Mouse on your local machine.

### Prerequisites
* A functional integrated or external webcam.
* Python 3.8 or higher installed on your system.
* Adequate room lighting (the neural network performs best in well-lit environments).

### Installation Steps

**1. Clone the Source Code**
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
4. **Navigation:** Raise your hand and point your **Index Finger** upwards. Move it around the frame to control the cursor.
5. **Left Click:** Bring your **Index Finger** and **Thumb** together in a quick pinching motion.
6. **Right Click:** Bring your **Middle Finger** and **Thumb** together in a quick pinching motion.
7. **Drag & Drop:** Pinch your **Index Finger** and **Thumb** together and *hold it*. Move your hand to drag the selected item, and release the pinch to drop it.
8. **Exit:** Bring the webcam window into focus and press the `q` key on your keyboard.

---

## 🛠️ Troubleshooting

* **Lag or Low FPS:** Ensure your system has sufficient CPU/GPU resources. Running this alongside heavy IDEs can cause throttling.
* **Cursor Dropping Items while Dragging:** Your hand might be moving out of the webcam's optimal lighting, causing the distance calculation to spike. Keep your hand steady and well-lit.
* **PyAutoGUI FailsSafeException:** If the cursor is thrown to the absolute corner of the screen (0,0), PyAutoGUI triggers a safety abort. Relaunch the script and keep your hand within the camera frame.

---

## 🗺️ Future Roadmap

* [ ] **Gesture-based Scrolling:** Implement an open-palm up/down swipe gesture for web page scrolling.
* [ ] **Volume & Brightness Control:** Map dynamic distances (e.g., spreading fingers apart) to system volume or screen brightness when toggled.
* [ ] **Virtual Keyboard Integration:** On-screen typing using index-finger hovering.
* [ ] **Multi-Monitor Support:** Dynamic Active Region mapping across dual-display setups.

---

<div align="center">
<b>Developed with 💡 by Suryansh Kushwaha</b><br>
<i>Exploring the intersection of Artificial Intelligence and Everyday Utilities.</i>
</div>
