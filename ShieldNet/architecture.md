# ShieldNet — System Architecture

## Overview

ShieldNet operates as a 4-layer autonomous defence pipeline:

```
Layer 1: SENSING
  ├── Radar arrays
  ├── IR thermal cameras
  └── Acoustic sensors

       ↓

Layer 2: DETECTION & CLASSIFICATION  
  ├── YOLOv8 real-time object detection
  ├── Threat classifier (missile / drone / UAV)
  └── Confidence scoring

       ↓

Layer 3: TRACKING & PREDICTION
  ├── Kalman Filter trajectory tracking
  ├── Future position prediction
  └── Intercept point calculation

       ↓

Layer 4: INTERCEPTION
  ├── Swarm controller assigns nearest drone
  ├── Interceptor drone deployed autonomously
  └── Net-capture / signal-jamming neutralisation

       ↓

Layer 5: REPORTING
  ├── Mission logged to command dashboard
  ├── Drone returns to base
  └── System ready for next threat
```

## Response Time Breakdown

| Step | Time |
|------|------|
| Detection | ~0.1s |
| Classification | ~0.2s |
| Trajectory Prediction | ~0.3s |
| Drone Dispatch | ~0.5s |
| **Total** | **< 1.5s** |

## Scalability

- Start: 1 facility, 6 drones
- Scale: Add drone units → coverage expands linearly
- City-wide: 100+ drone mesh with central AI coordination
