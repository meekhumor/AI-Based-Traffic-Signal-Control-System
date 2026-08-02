# Smart Flow: System Workflow & Execution Guide

This document details the step-by-step workflow for setting up, running, training, and deploying the **Smart Flow** AI-Based Traffic Signal Control System.

---

## 1. Setup & Environment Preparation

### Prerequisites
- **Python 3.10+**
- **SUMO Traffic Simulator** (`sumo` and `sumo-gui` installed and in system `PATH`)
- Dependencies: `opencv-python`, `numpy`, `matplotlib`, `torch`, `ultralytics`, `stable-baselines3`, `gymnasium`, `traci`

### Download Sample Video Dataset
For running the Computer Vision modules (`cv/vehicle_counter.py`, `cv/yolo_counter.py`), download the sample test videos folder and place it in the root directory as `videos/`:

🔗 **[Download Videos Directory (Google Drive)](https://drive.google.com/drive/folders/1JRi_RcdV4Azvd7tk1Hysj_cmv0SHjuLW?usp=sharing)**

Expected folder structure after setup:
```
AI-Based-Traffic-Signal-Control-System/
├── videos/
│   ├── road.mp4
│   └── rush.mp4
```

---

## 2. Computer Vision Pipeline Execution

Run vehicle counting and lane detection from the repository root:

### Contour-Based Vehicle Counter
```bash
python3 -m cv.vehicle_counter
```
*Processes the video feed using Hough-based lane detection, subtracts calibrated background noise, and counts vehicle contours in real time.*

### YOLOv8 Object Detection Counter
```bash
python3 -m cv.yolo_counter
```
*Uses YOLOv8 nano model (`yolov8n.pt`) to count vehicles (cars, trucks, buses, motorbikes) within the monitored approach.*

---

## 3. SUMO Network Creation & Simulation

### Step 3.1: Create Network File
Use SUMO's `netedit` GUI or convert an OpenStreetMap `.osm` export:
```bash
netconvert --osm-files sumo/maps/kingcircle.osm -o sumo/maps/kingcircle.net.xml
```

### Step 3.2: Generate Vehicle Route File
Generate random trip demand for the network:
```bash
python3 sumo/maps/randomTrips.py -n sumo/maps/kingcircle.net.xml -r sumo/maps/kingcircle.rou.xml
```

### Step 3.3: Verify Simulation Setup
Launch SUMO-GUI to verify network traffic flow:
```bash
sumo-gui -c sumo/kingcircle.sumocfg
```

---

## 4. Reinforcement Learning (DQN Signal Control)

### Step 4.1: Train DQN Agent
Train a Deep Q-Network agent in SUMO:
```bash
python3 -m rl.train_dqn
```
*The model observes halting vehicle counts per lane and learns an optimal phase timing policy. Trained model snapshots are saved in `rl/saved_models/`.*

### Step 4.2: Evaluate Model in SUMO-GUI
Test the trained agent with live SUMO visual feedback:
```bash
python3 -m rl.test_dqn
```

---

## 5. Model Export & Edge Deployment Pipeline

Convert trained Stable-Baselines3 policies for high-performance edge deployment:

$$\text{SUMO TraCI} \longrightarrow \text{DQN Model (.zip)} \longrightarrow \text{ONNX Export} \longrightarrow \text{OpenVINO IR}$$

### Step 5.1: Export Policy to ONNX
```python
from stable_baselines3 import DQN

model = DQN.load("rl/saved_models/traffic_light_dqn")
model.policy.to_onnx("traffic_light_dqn.onnx", export_params=True)
```

### Step 5.2: Convert to OpenVINO IR
Optimize the ONNX model for Intel edge hardware:
```bash
ovc traffic_light_dqn.onnx --output_model optimized_model/traffic_light_dqn --input "input[1,6]"
```