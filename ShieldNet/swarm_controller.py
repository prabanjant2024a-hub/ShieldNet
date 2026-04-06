"""
ShieldNet - Interceptor Drone Swarm Controller
Team CodeStorm | EQUINOX 2026

Manages a fleet of autonomous interceptor drones.
Assigns the nearest available drone to intercept a detected threat.
"""

import math
import time
import random
from datetime import datetime


# ─── Drone Status ──────────────────────────────────────────────────────────────

class DroneStatus:
    IDLE       = "IDLE"
    DEPLOYING  = "DEPLOYING"
    INTERCEPT  = "INTERCEPTING"
    RETURNING  = "RETURNING"
    RECHARGING = "RECHARGING"


# ─── Individual Drone ─────────────────────────────────────────────────────────

class InterceptorDrone:
    """Represents a single interceptor drone in the ShieldNet fleet."""

    def __init__(self, drone_id, base_position):
        self.drone_id      = drone_id
        self.base_position = base_position
        self.position      = list(base_position)
        self.status        = DroneStatus.IDLE
        self.battery       = 100.0   # %
        self.target        = None
        self.missions      = 0

    def assign_target(self, target_position):
        """Assign this drone to intercept a threat."""
        self.target = target_position
        self.status = DroneStatus.DEPLOYING
        self.missions += 1

        dist = self.distance_to(target_position)
        eta  = round(dist / 50, 2)  # Assume 50 units/sec speed

        print(f"  🚁 Drone {self.drone_id} → Target ({target_position[0]:.0f}, {target_position[1]:.0f})")
        print(f"     Distance : {dist:.1f} units | ETA : {eta}s")
        return eta

    def distance_to(self, point):
        """Calculate Euclidean distance from current position to a point."""
        return math.sqrt(
            (self.position[0] - point[0])**2 +
            (self.position[1] - point[1])**2
        )

    def distance_from_base(self):
        return self.distance_to(self.base_position)

    def is_available(self):
        return self.status == DroneStatus.IDLE and self.battery > 20.0

    def return_to_base(self):
        self.status   = DroneStatus.RETURNING
        self.position = list(self.base_position)
        self.status   = DroneStatus.IDLE
        self.battery  = max(0, self.battery - random.uniform(8, 15))

    def recharge(self):
        self.status  = DroneStatus.RECHARGING
        self.battery = 100.0
        self.status  = DroneStatus.IDLE

    def __repr__(self):
        return (f"Drone[{self.drone_id}] "
                f"pos=({self.position[0]:.0f},{self.position[1]:.0f}) "
                f"status={self.status} battery={self.battery:.0f}%")


# ─── Swarm Controller ─────────────────────────────────────────────────────────

class SwarmController:
    """
    Central controller for the ShieldNet interceptor drone fleet.
    Receives threat coordinates and dispatches nearest available drone.
    """

    def __init__(self, num_drones=6, base_positions=None):
        self.fleet        = []
        self.mission_log  = []
        self.threats_neutralised = 0

        # Default base positions (spread around perimeter)
        if base_positions is None:
            base_positions = [
                (100, 100), (500, 100), (900, 100),
                (100, 500), (500, 500), (900, 500),
            ]

        for i in range(num_drones):
            pos = base_positions[i % len(base_positions)]
            self.fleet.append(InterceptorDrone(
                drone_id=f"SN-{i+1:02d}",
                base_position=pos
            ))

        print("=" * 55)
        print("  🛡️  SHIELDNET SWARM CONTROLLER ONLINE")
        print("=" * 55)
        print(f"  Fleet Size   : {len(self.fleet)} drones")
        print(f"  All Systems  : READY")
        print("=" * 55)

    def get_nearest_available(self, target):
        """Find the nearest available drone to the threat."""
        available = [d for d in self.fleet if d.is_available()]
        if not available:
            return None
        return min(available, key=lambda d: d.distance_to(target))

    def dispatch(self, threat_position, threat_name="Unknown"):
        """
        Main dispatch function.
        Finds best drone and sends it to intercept the threat.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n🚨 [{timestamp}] THREAT ALERT: {threat_name}")
        print(f"   Location : ({threat_position[0]:.0f}, {threat_position[1]:.0f})")

        drone = self.get_nearest_available(threat_position)

        if drone is None:
            print("   ⚠️  WARNING: No drones available! All units busy or low battery.")
            return None

        eta = drone.assign_target(threat_position)

        mission = {
            "timestamp"  : timestamp,
            "threat"     : threat_name,
            "target"     : threat_position,
            "drone_id"   : drone.drone_id,
            "eta_seconds": eta,
            "status"     : "DISPATCHED"
        }
        self.mission_log.append(mission)

        # Simulate intercept
        time.sleep(0.3)
        drone.status = DroneStatus.INTERCEPT
        print(f"   ✅ INTERCEPT SUCCESSFUL — {drone.drone_id} neutralised threat!")
        drone.return_to_base()
        self.threats_neutralised += 1
        mission["status"] = "NEUTRALISED"

        return drone

    def fleet_status(self):
        """Print full fleet status."""
        print(f"\n{'='*55}")
        print(f"  📊 FLEET STATUS REPORT")
        print(f"{'='*55}")
        for drone in self.fleet:
            avail = "✅ READY" if drone.is_available() else f"🔴 {drone.status}"
            print(f"  {drone.drone_id} | Battery: {drone.battery:.0f}% | "
                  f"Missions: {drone.missions} | {avail}")
        print(f"{'='*55}")
        print(f"  Total Threats Neutralised : {self.threats_neutralised}")
        print(f"{'='*55}")

    def mission_summary(self):
        """Print all mission logs."""
        print(f"\n{'='*55}")
        print(f"  📋 MISSION LOG ({len(self.mission_log)} missions)")
        print(f"{'='*55}")
        for m in self.mission_log:
            print(f"  [{m['timestamp']}] {m['threat']:20s} → "
                  f"{m['drone_id']} | ETA {m['eta_seconds']}s | {m['status']}")


# ─── Demo ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    controller = SwarmController(num_drones=6)

    # Simulate 4 incoming threats
    threats = [
        ((750, 80),  "Ballistic Missile"),
        ((300, 120), "Attack Drone"),
        ((600, 200), "Cruise Missile"),
        ((150, 300), "UAV Swarm"),
    ]

    print("\n[SIM] Simulating incoming threats...\n")
    for pos, name in threats:
        controller.dispatch(pos, name)
        time.sleep(0.5)

    controller.fleet_status()
    controller.mission_summary()
