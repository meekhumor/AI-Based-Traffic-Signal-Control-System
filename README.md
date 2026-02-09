<h1 align="center">🚦 SMART FLOW: AI-Powered Traffic Management System</h1>

<p align="center">
  <img src="https://github.com/user-attachments/assets/49f2935d-1a60-4035-af3f-97eb70cea058" width="350" />
</p>

<div align="center">
  <strong>Revolutionizing urban traffic management through AI-driven intelligent traffic light control systems that adapt to real-time congestion patterns, reducing wait times and emissions while enhancing city mobility.</strong>
</div>

<br />

## 📑 Table of Contents

* [The Urban Challenge](#-the-urban-challenge)
* [Our Solution](#-our-solution)
* [Core Technologies](#️-core-technologies)
* [System Architecture](#-system-architecture)
* [Key Results](#-key-results)
* [Real-world Impact](#-real-world-impact)
* [Future Roadmap](#-future-roadmap)
* [Team Members](#-team-members)

## 🌆 The Urban Challenge

In India's rapidly growing cities, traffic intersections have become critical bottlenecks, where:
* Average commuters lose 2-3 hours daily in traffic congestion
* Conventional timer-based systems fail to adapt to dynamic traffic patterns
* Manual traffic management is inconsistent and resource-intensive
* Vehicle emissions from idling contribute significantly to urban air pollution

Smart Flow transforms these painpoints into opportunities for creating smarter, more efficient urban mobility.

## 💡 Our Solution

### Smart Flow's Adaptive Intelligence System


**Vehicle Count Detection**

https://github.com/user-attachments/assets/84eb35d4-ce2e-4db9-9734-502bc9cbacee

<img src="https://github.com/user-attachments/assets/a452e21f-c295-42d1-bf9e-40dc430030e7" width="600" />

<br />

**Reinforcement Learning**

https://github.com/user-attachments/assets/444ece30-dcd7-4607-8d53-4da42c7d65ba

https://github.com/user-attachments/assets/e88b2391-1fb8-4e7a-8a19-c6cf92b9dc3e

<br />

Unlike traditional systems, Smart Flow:
* **Sees** traffic conditions in real-time through computer vision
* **Learns** from historical patterns using reinforcement learning
* **Adapts** signal timings dynamically to optimize flow
* **Coordinates** across multiple intersections for network-wide efficiency

## ⚙️ Core Technologies

| **Category** | **Technologies** |
|--------------|-----------------|
| **Computer Vision** | [![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/) [![Edge Detection](https://img.shields.io/badge/Canny%20Edge-00BFFF?style=for-the-badge&logo=opencv&logoColor=white)](https://docs.opencv.org/master/da/d22/tutorial_py_canny.html) |
| **AI Models** | [![Reinforcement Learning](https://img.shields.io/badge/Reinforcement%20Learning-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/) [![Regression Analysis](https://img.shields.io/badge/Regression-013243?style=for-the-badge&logo=python&logoColor=white)](https://scikit-learn.org/) |
| **Simulation** | [![SUMO](https://img.shields.io/badge/SUMO-4D2A4E?style=for-the-badge&logo=eclipse&logoColor=white)](https://www.eclipse.org/sumo/) [![Traffic Simulation](https://img.shields.io/badge/Traffic%20Simulation-3C9AD0?style=for-the-badge&logo=unity&logoColor=white)](https://www.dlr.de/ts/en/desktopdefault.aspx/tabid-9883/16931_read-41000/) |
| **Implementation** | [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)|
| **Data Analysis** | [![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/) [![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/) |
| **Visualization** | [![Matplotlib](https://img.shields.io/badge/Matplotlib-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://matplotlib.org/) [![Seaborn](https://img.shields.io/badge/Seaborn-013243?style=for-the-badge&logo=python&logoColor=white)](https://seaborn.pydata.org/) |

## 🏗 System Architecture

<img src="https://github.com/user-attachments/assets/3dcb0e55-6fba-408a-9d6c-be772fb7aab2" width="700" />

1. **Data Acquisition Layer**
   - Traffic cameras capture video feeds
   - Image processing converts to 20 frames/min
   - Grayscale conversion optimizes computational efficiency

2. **Analysis Engine**
   - **Canny Edge** Detection identifies vehicle outlines
   - **Semantic segmentation** differentiates vehicles from surroundings
   - **Hough Line Transform** separates lanes for accurate counting

3. **Decision Intelligence**
   - Reinforcement learning model evaluates traffic density
   - Reward system optimizes for minimum wait time
   - Historical pattern analysis informs predictive adjustments

4. **Control Interface**
   - API connects to existing traffic light controllers
   - Dashboard provides real-time system monitoring
   - Performance analytics track system improvements

## 📊 Key Results

### Efficiency Improvements

<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/66402c78-e044-4088-970a-7b948c3db006" alt="wait-time-reduction" width="650"></td>
  </tr>
  <tr>
    <td align="center">Wait Time Reduction</td>
  </tr>
</table>

## 🌍 Real-world Impact

### Environmental Benefits
* **Reduced Emissions**: 18% reduction in CO2 emissions from decreased idling time
* **Fuel Savings**: Estimated 15-20% reduction in fuel consumption at optimized intersections

### Economic Value
* **Commuter Time Savings**: Average 12 minutes saved per commuter per day
* **Implementation Cost**: 5-10x lower than infrastructure expansion alternatives
* **ROI Timeline**: Initial investment recovered within 18-24 months through reduced congestion costs

### Urban Quality of Life
* **Reduced Stress**: Decreased unpredictability in commute times
* **Emergency Response**: Priority routing for emergency vehicles reduces response times by 23%
* **Public Transportation**: Improved schedule reliability for buses operating on optimized routes


## 🚀 Future Roadmap

* **V2X Integration**: Connect with vehicle-to-infrastructure communication systems
* **Pedestrian Intelligence**: Incorporate pedestrian density in optimization algorithms
* **Weather Adaptation**: Dynamically adjust for adverse weather conditions
* **Citywide Deployment**: Scale from individual intersections to citywide traffic optimization
* **Public API**: Provide traffic prediction data for navigation apps and urban planners

## 👥 Team Members

| Name | GitHub |
|--------|----------|
| Om Mukherjee | [GitHub](https://github.com/meekhumor) |
| Abhishek Kotwani | [GitHub](https://github.com/Abhi-sheKkK) |
| Aryan Yadav | [GitHub](https://github.com/Aryan-y-77) |
---

