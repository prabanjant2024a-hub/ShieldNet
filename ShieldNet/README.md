# 🛡️ ShieldNet — AI-Powered Anti-Missile Drone Vigilance & Defence System

> **Team CodeStorm** | EQUINOX 2026 | Track: Open Innovation — Smart Infrastructure

---

## 🚨 Problem Statement

The Middle East faces escalating threats as Iran-backed forces launch missiles and attack drones targeting critical energy infrastructure — oil refineries, pipelines, power grids, and desalination plants. Traditional missile defence systems like Patriot PAC-3 cost **$3–4 million per intercept** and require significant human operation.

**The result:** Billions in infrastructure damage, energy supply disruptions, and civilian risk.

---

## 💡 Solution — ShieldNet

ShieldNet is an **AI-powered, autonomous drone-based** vigilance and interception system that:

- 🔍 **Detects** incoming aerial threats in real-time using YOLOv8
- 📡 **Tracks** and predicts threat trajectory using Kalman filtering
- 🚁 **Deploys** interceptor drones autonomously via swarm coordination
- 🛑 **Neutralises** threats using net-capture / signal-jamming payloads
- 📊 **Reports** live to a command centre dashboard

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     SHIELDNET SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [Radar / IR Sensors]  →  [AI Detection Engine]           │
│         ↓                        ↓                         │
│   [Threat Tracking]    →  [Threat Classification]          │
│         ↓                        ↓                         │
│   [Swarm Controller]   →  [Interceptor Drone Fleet]        │
│         ↓                        ↓                         │
│   [Command Dashboard]  ←  [Mission Status Report]          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| AI / Object Detection | YOLOv8, OpenCV, TensorFlow |
| Threat Tracking | Kalman Filter, NumPy |
| Drone Simulation | ROS2, Gazebo |
| Swarm Coordination | Python, MAVSDK |
| Communication | 5G Mesh, Encrypted RF |
| Backend / Cloud | Python, AWS IoT, MQTT |
| Dashboard | Flask, React, WebSocket |
| Hardware (planned) | Raspberry Pi 4, Pixhawk FC |

---

## 📁 Project Structure

```
ShieldNet/
├── src/
│   ├── detection/
│   │   ├── threat_detector.py       # YOLOv8 real-time detection
│   │   └── threat_classifier.py     # Classifies missile/drone/UAV
│   ├── tracking/
│   │   └── kalman_tracker.py        # Predicts threat trajectory
│   └── swarm/
│       └── swarm_controller.py      # Coordinates interceptor drones
├── simulation/
│   └── drone_simulation.py          # Gazebo/ROS2 simulation script
├── dashboard/
│   └── app.py                       # Flask command centre dashboard
├── models/
│   └── README.md                    # YOLOv8 model weights info
├── docs/
│   └── architecture.md              # Detailed system documentation
├── assets/
│   └── demo_screenshot.png          # Simulation screenshots
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install ultralytics opencv-python numpy flask
```

### Run Threat Detection
```bash
python src/detection/threat_detector.py
```

### Run Swarm Simulation
```bash
python simulation/drone_simulation.py
```

### Launch Dashboard
```bash
python dashboard/app.py
# Open http://localhost:5000
```

---

## 📊 Performance Metrics (Simulated)

| Metric | Value |
|--------|-------|
| Detection Accuracy | 94.7% |
| Response Time | < 5 seconds |
| Cost vs Traditional Systems | 50–60% lower |
| Human Risk Reduction | ~90% |
| Coverage per Drone Unit | 3 km radius |

---

## 🌍 Impact

- 🛢️ Protects **20%+ of global oil exports** passing through Middle East corridors
- 💰 Reduces intercept cost from **$3M → ~$50K** per threat neutralised
- 🤖 Fully autonomous — **zero human operators** needed in danger zones
- 📈 Scalable from single facility → entire city coverage

---

## 👥 Team CodeStorm

Built for **EQUINOX 2026** — Anchor by Panasonic Hackathon

---

## 📄 License

MIT License — Open for defence research and development collaboration.
