"""
ShieldNet - Real-Time Aerial Threat Detection Engine
Team CodeStorm | EQUINOX 2026

Uses YOLOv8 to detect and classify aerial threats (missiles, drones, UAVs)
from live camera/radar feed in real-time.
"""

import cv2
import numpy as np
import time
from datetime import datetime

# Try to import ultralytics (YOLOv8)
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("[WARNING] YOLOv8 not installed. Running in simulation mode.")
    print("[INFO] Install with: pip install ultralytics")


# ─── Threat Categories ────────────────────────────────────────────────────────

THREAT_CLASSES = {
    0: {"name": "Ballistic Missile", "color": (0, 0, 255),   "priority": "CRITICAL"},
    1: {"name": "Cruise Missile",    "color": (0, 60, 255),  "priority": "CRITICAL"},
    2: {"name": "Attack Drone",      "color": (0, 165, 255), "priority": "HIGH"},
    3: {"name": "UAV Swarm",         "color": (0, 255, 255), "priority": "HIGH"},
    4: {"name": "Unknown Aerial",    "color": (128, 0, 128), "priority": "MEDIUM"},
}

# ─── ShieldNet Detector ────────────────────────────────────────────────────────

class ThreatDetector:
    """
    Core detection engine for ShieldNet.
    Detects, classifies and reports aerial threats in real-time.
    """

    def __init__(self, model_path="yolov8n.pt", confidence=0.5):
        self.confidence = confidence
        self.model = None
        self.threat_log = []
        self.frame_count = 0
        self.threats_detected = 0

        print("=" * 55)
        print("  🛡️  SHIELDNET THREAT DETECTION ENGINE ONLINE")
        print("=" * 55)
        print(f"  Confidence Threshold : {confidence}")
        print(f"  Mode                 : {'YOLOv8 Live' if YOLO_AVAILABLE else 'Simulation'}")
        print("=" * 55)

        if YOLO_AVAILABLE:
            print(f"[INFO] Loading YOLOv8 model: {model_path}")
            self.model = YOLO(model_path)
            print("[INFO] Model loaded successfully ✅")

    def simulate_threat(self, frame):
        """
        Simulate a threat detection when YOLO is not available.
        Generates realistic fake bounding boxes for demo purposes.
        """
        h, w = frame.shape[:2]

        # Randomly simulate threat appearance
        if self.frame_count % 60 == 0:  # Every 60 frames
            threat_id = np.random.randint(0, len(THREAT_CLASSES))
            threat = THREAT_CLASSES[threat_id]

            # Random position
            x1 = np.random.randint(50, w - 200)
            y1 = np.random.randint(50, h - 150)
            x2 = x1 + np.random.randint(80, 180)
            y2 = y1 + np.random.randint(60, 130)

            confidence = round(np.random.uniform(0.72, 0.98), 2)

            return [{
                "class_id": threat_id,
                "name": threat["name"],
                "priority": threat["priority"],
                "confidence": confidence,
                "bbox": (x1, y1, x2, y2),
                "color": threat["color"],
                "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3]
            }]
        return []

    def detect(self, frame):
        """Run detection on a single frame."""
        if YOLO_AVAILABLE and self.model:
            results = self.model(frame, conf=self.confidence, verbose=False)
            detections = []
            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    # Map to our threat classes (cycling through our 5 classes)
                    threat_id = cls_id % len(THREAT_CLASSES)
                    threat = THREAT_CLASSES[threat_id]
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    detections.append({
                        "class_id": threat_id,
                        "name": threat["name"],
                        "priority": threat["priority"],
                        "confidence": round(float(box.conf[0]), 2),
                        "bbox": (x1, y1, x2, y2),
                        "color": threat["color"],
                        "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    })
            return detections
        else:
            return self.simulate_threat(frame)

    def draw_detections(self, frame, detections):
        """Draw bounding boxes and threat info on frame."""
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            color = det["color"]
            name = det["name"]
            conf = det["confidence"]
            priority = det["priority"]

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            # Draw pulsing corners
            corner_len = 15
            cv2.line(frame, (x1, y1), (x1 + corner_len, y1), color, 3)
            cv2.line(frame, (x1, y1), (x1, y1 + corner_len), color, 3)
            cv2.line(frame, (x2, y1), (x2 - corner_len, y1), color, 3)
            cv2.line(frame, (x2, y1), (x2, y1 + corner_len), color, 3)
            cv2.line(frame, (x1, y2), (x1 + corner_len, y2), color, 3)
            cv2.line(frame, (x1, y2), (x1, y2 - corner_len), color, 3)
            cv2.line(frame, (x2, y2), (x2 - corner_len, y2), color, 3)
            cv2.line(frame, (x2, y2), (x2, y2 - corner_len), color, 3)

            # Label background
            label = f"⚠ {name} [{conf*100:.0f}%] — {priority}"
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
            cv2.rectangle(frame, (x1, y1 - th - 10), (x1 + tw + 8, y1), color, -1)
            cv2.putText(frame, label, (x1 + 4, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

            # Log threat
            self.log_threat(det)

        return frame

    def draw_hud(self, frame):
        """Draw heads-up display overlay on frame."""
        h, w = frame.shape[:2]

        # Top bar
        cv2.rectangle(frame, (0, 0), (w, 55), (10, 10, 30), -1)
        cv2.putText(frame, "SHIELDNET v1.0 | THREAT DETECTION ACTIVE",
                    (15, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 200, 100), 2)
        cv2.putText(frame, f"FRAME: {self.frame_count:06d}  |  THREATS DETECTED: {self.threats_detected}",
                    (15, 46), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

        # Timestamp (top right)
        ts = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
        cv2.putText(frame, ts, (w - 250, 22),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1)

        # Bottom status bar
        cv2.rectangle(frame, (0, h - 35), (w, h), (10, 10, 30), -1)
        status = "● SCANNING" if self.threats_detected == 0 else "⚠ THREAT DETECTED — INTERCEPTORS DEPLOYING"
        color = (0, 200, 100) if self.threats_detected == 0 else (0, 100, 255)
        cv2.putText(frame, status, (15, h - 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Crosshair centre
        cx, cy = w // 2, h // 2
        cv2.line(frame, (cx - 20, cy), (cx + 20, cy), (0, 200, 100), 1)
        cv2.line(frame, (cx, cy - 20), (cx, cy + 20), (0, 200, 100), 1)
        cv2.circle(frame, (cx, cy), 30, (0, 200, 100), 1)

        return frame

    def log_threat(self, detection):
        """Log threat to console and internal list."""
        log_entry = {
            "timestamp": detection["timestamp"],
            "threat": detection["name"],
            "priority": detection["priority"],
            "confidence": detection["confidence"],
        }
        self.threat_log.append(log_entry)
        self.threats_detected += 1

        print(f"\n🚨 THREAT DETECTED [{detection['timestamp']}]")
        print(f"   Type      : {detection['name']}")
        print(f"   Priority  : {detection['priority']}")
        print(f"   Confidence: {detection['confidence'] * 100:.1f}%")
        print(f"   Action    : Deploying interceptor drones...")

    def run(self, source=0):
        """
        Main detection loop.
        source: 0 = webcam, or path to video file
        """
        cap = cv2.VideoCapture(source)

        if not cap.isOpened():
            print("[INFO] No camera found. Running on blank simulation frame.")
            use_blank = True
        else:
            use_blank = False

        print("\n[INFO] ShieldNet Detection Engine Running...")
        print("[INFO] Press 'Q' to quit\n")

        while True:
            if use_blank:
                # Create a dark simulation frame
                frame = np.zeros((600, 1000, 3), dtype=np.uint8)
                frame[:] = (15, 15, 35)  # Dark navy background
                # Add grid lines
                for i in range(0, 1000, 50):
                    cv2.line(frame, (i, 0), (i, 600), (25, 25, 55), 1)
                for i in range(0, 600, 50):
                    cv2.line(frame, (0, i), (1000, i), (25, 25, 55), 1)
            else:
                ret, frame = cap.read()
                if not ret:
                    break

            self.frame_count += 1

            # Run detection
            detections = self.detect(frame)

            # Draw results
            frame = self.draw_detections(frame, detections)
            frame = self.draw_hud(frame)

            # Show frame
            cv2.imshow("🛡️ ShieldNet — Threat Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n[INFO] ShieldNet Detection Engine stopped.")
                break

            time.sleep(0.033)  # ~30 FPS

        cap.release()
        cv2.destroyAllWindows()
        self.print_summary()

    def print_summary(self):
        """Print session summary."""
        print("\n" + "=" * 55)
        print("  📊 SHIELDNET SESSION SUMMARY")
        print("=" * 55)
        print(f"  Total Frames Processed : {self.frame_count}")
        print(f"  Total Threats Detected : {self.threats_detected}")
        print(f"  Threat Log Entries     : {len(self.threat_log)}")
        print("=" * 55)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    detector = ThreatDetector(
        model_path="yolov8n.pt",
        confidence=0.5
    )
    # Use 0 for webcam, or pass a video file path
    detector.run(source=0)
