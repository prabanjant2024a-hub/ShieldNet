"""
ShieldNet - Kalman Filter Threat Trajectory Tracker
Team CodeStorm | EQUINOX 2026

Predicts where a missile/drone will be in the next N seconds
so interceptor drones can be deployed AHEAD of the threat path.
"""

import numpy as np
from datetime import datetime


class KalmanTracker:
    """
    Tracks a detected aerial threat using a Kalman Filter.
    Predicts future position to enable proactive interception.
    """

    def __init__(self, initial_position, threat_name="Unknown"):
        self.threat_name = threat_name
        self.track_id = id(self)
        self.created_at = datetime.now()
        self.history = []

        # State vector: [x, y, vx, vy] — position + velocity
        self.state = np.array([
            initial_position[0],  # x
            initial_position[1],  # y
            0.0,                  # vx (velocity x)
            0.0                   # vy (velocity y)
        ], dtype=float)

        # State covariance
        self.P = np.eye(4) * 100

        # State transition matrix (constant velocity model)
        self.F = np.array([
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=float)

        # Measurement matrix (we observe x, y only)
        self.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ], dtype=float)

        # Process noise
        self.Q = np.eye(4) * 0.1

        # Measurement noise
        self.R = np.eye(2) * 10

        print(f"[TRACKER] Tracking: {threat_name} | ID: {self.track_id}")

    def predict(self):
        """Predict the next state."""
        self.state = self.F @ self.state
        self.P = self.F @ self.P @ self.F.T + self.Q
        return self.state[:2]  # Return predicted (x, y)

    def update(self, measurement):
        """Update state with new measurement."""
        z = np.array(measurement, dtype=float)

        # Kalman gain
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)

        # Update state
        y = z - self.H @ self.state
        self.state = self.state + K @ y
        self.P = (np.eye(4) - K @ self.H) @ self.P

        self.history.append(tuple(self.state[:2]))
        return self.state[:2]

    def predict_future(self, steps=10):
        """
        Predict threat position N steps into the future.
        Used to calculate interceptor drone deployment point.
        """
        future_state = self.state.copy()
        predictions = []

        for _ in range(steps):
            future_state = self.F @ future_state
            predictions.append((future_state[0], future_state[1]))

        return predictions

    def get_velocity(self):
        """Returns current estimated velocity (vx, vy)."""
        return self.state[2], self.state[3]

    def get_speed(self):
        """Returns scalar speed in units/frame."""
        vx, vy = self.get_velocity()
        return np.sqrt(vx**2 + vy**2)

    def get_intercept_point(self, steps=15):
        """
        Returns the recommended interception point —
        where the interceptor drone should aim.
        """
        predictions = self.predict_future(steps)
        return predictions[-1]  # Intercept at last predicted point

    def summary(self):
        """Print tracker status."""
        vx, vy = self.get_velocity()
        speed = self.get_speed()
        intercept = self.get_intercept_point()

        print(f"\n📡 TRACKER REPORT — {self.threat_name}")
        print(f"   Current Position : ({self.state[0]:.1f}, {self.state[1]:.1f})")
        print(f"   Velocity         : vx={vx:.2f}, vy={vy:.2f}")
        print(f"   Speed            : {speed:.2f} units/frame")
        print(f"   Intercept Point  : ({intercept[0]:.1f}, {intercept[1]:.1f})")
        print(f"   Track History    : {len(self.history)} points")


# ─── Demo ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  🛡️  SHIELDNET KALMAN TRACKER — DEMO")
    print("=" * 55)

    # Simulate a missile flying from top-right to bottom-left
    tracker = KalmanTracker(
        initial_position=(800, 50),
        threat_name="Ballistic Missile"
    )

    # Simulate 20 frames of detection
    print("\n[SIM] Simulating missile trajectory...\n")
    for i in range(20):
        # Fake measurement: missile moving diagonally
        noisy_x = 800 - (i * 30) + np.random.normal(0, 5)
        noisy_y = 50  + (i * 20) + np.random.normal(0, 5)

        predicted = tracker.predict()
        updated   = tracker.update([noisy_x, noisy_y])

        print(f"  Frame {i+1:02d} | Measured: ({noisy_x:.1f}, {noisy_y:.1f}) "
              f"| Predicted: ({predicted[0]:.1f}, {predicted[1]:.1f})")

    # Final report
    tracker.summary()

    # Intercept points
    future = tracker.predict_future(steps=10)
    print(f"\n🎯 INTERCEPT TRAJECTORY (next 10 frames):")
    for i, (fx, fy) in enumerate(future):
        print(f"   t+{i+1:02d}: ({fx:.1f}, {fy:.1f})")

    intercept = tracker.get_intercept_point()
    print(f"\n🚁 DEPLOYING INTERCEPTOR DRONE TO: ({intercept[0]:.1f}, {intercept[1]:.1f})")
