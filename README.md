# ShieldNet

An AI-based system that focuses on detecting and responding to incoming missile threats using drones.

---

## What this project is about

This project is built around a simple idea — **react faster than the threat**.

ShieldNet uses basic AI concepts and drone coordination to:

* detect a possible incoming missile
* track its movement
* send a response using a drone system

It’s not a finished defence product, but more like a **working concept / prototype** showing how AI + drones can be combined for real-time defence.

---

## How it works (in simple terms)

1. Input comes from surveillance (camera / radar simulation)
2. AI model checks if it’s a threat
3. If yes → system starts tracking
4. A drone is triggered for response
5. Everything is monitored in real-time

---

## Tech used

* Python
* OpenCV (for basic detection)
* Some ML logic (model can be improved)
* Git & GitHub

---

## Project structure

```
ShieldNet/
├── src/        # main logic
├── models/     # trained / dummy models
├── data/       # test inputs
├── docs/       # ppt / report
└── main.py
```

---

## Running the project

```bash
git clone https://github.com/your-username/shieldnet.git
cd shieldnet
pip install -r requirements.txt
python main.py
```

---

## Current state

This is still in an early stage.
Some parts are simulated, especially:

* drone response
* real-world missile data

---

## What can be improved

* better detection accuracy
* real-time hardware integration
* more realistic simulation
* faster decision making

---

## Why I built this

Mostly to explore how AI can be used in **real-world high-risk systems**, not just small apps.

---

## Author

Prabanjan T
