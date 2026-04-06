"""
ShieldNet - Full System Simulation
Team CodeStorm | EQUINOX 2026

Runs a complete end-to-end simulation of the ShieldNet system:
  1. Threats are randomly generated
  2. Detection engine flags them
  3. Kalman tracker predicts trajectory
  4. Swarm controller dispatches interceptors
  5. Dashboard logs everything

Run this file to see the full ShieldNet pipeline in action.
"""

import time
import random
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tracking.kalman_tracker import KalmanTracker
from src.swarm.swarm_controller import SwarmController


# ─── Threat Simulator ─────────────────────────────────────────────────────────

THREAT_TYPES = [
    "Ballistic Missile",
    "Cruise Missile",
    "Attack Drone",
    "UAV Swarm",
    "Unknown Aerial Object"
]

def generate_threat():
    """Generate a random incoming threat."""
    return {
        "name"    : random.choice(THREAT_TYPES),
        "position": (
            random.randint(100, 900),
            random.randint(50, 200)
        ),
        "velocity": (
            random.uniform(-5, -1),   # Moving left
            random.uniform(2, 8)      # Moving down
        )
    }


# ─── Full Pipeline ────────────────────────────────────────────────────────────

def run_simulation(num_threats=5, simulation_speed=0.05):
    """
    Run the full ShieldNet detection → tracking → intercept pipeline.
    """

    print("\n")
    print("╔══════════════════════════════════════════════════════╗")
    print("║      🛡️  SHIELDNET FULL SYSTEM SIMULATION           ║")
    print("║         Team CodeStorm | EQUINOX 2026               ║")
    print("╚══════════════════════════════════════════════════════╝")
    print()

    # Initialise swarm controller
    controller = SwarmController(num_drones=6)

    print(f"\n[SIM] Generating {num_threats} incoming threats...\n")
    time.sleep(1)

    for threat_num in range(1, num_threats + 1):

        print(f"\n{'─'*55}")
        print(f"  ⚡ THREAT {threat_num} OF {num_threats}")
        print(f"{'─'*55}")

        # Step 1: Generate threat
        threat = generate_threat()
        print(f"  Threat Type : {threat['name']}")
        print(f"  Origin      : {threat['position']}")

        # Step 2: Track with Kalman filter
        tracker = KalmanTracker(
            initial_position=threat["position"],
            threat_name=threat["name"]
        )

        # Simulate 10 frames of tracking
        pos = list(threat["position"])
        print(f"\n  [TRACKING] Predicting trajectory...")
        for frame in range(10):
            pos[0] += threat["velocity"][0] + np.random.normal(0, 2)
            pos[1] += threat["velocity"][1] + np.random.normal(0, 2)
            tracker.predict()
            tracker.update(pos)
            time.sleep(simulation_speed)

        # Step 3: Get intercept point
        intercept_point = tracker.get_intercept_point(steps=15)
        speed = tracker.get_speed()

        print(f"  [TRACKER]  Speed     : {speed:.1f} units/frame")
        print(f"  [TRACKER]  Intercept : ({intercept_point[0]:.0f}, {intercept_point[1]:.0f})")

        # Step 4: Dispatch interceptor
        print(f"\n  [SWARM]    Dispatching interceptor...")
        controller.dispatch(intercept_point, threat["name"])

        time.sleep(0.5)

    # Final report
    print(f"\n\n{'═'*55}")
    print(f"  ✅  SIMULATION COMPLETE")
    print(f"{'═'*55}")
    controller.fleet_status()
    controller.mission_summary()

    print(f"\n  🛡️  All threats neutralised. Infrastructure secured.")
    print(f"{'═'*55}\n")


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_simulation(num_threats=5, simulation_speed=0.03)
