"""
ShieldNet - Command Centre Dashboard
Team CodeStorm | EQUINOX 2026

A real-time Flask web dashboard showing:
- Live threat detection feed
- Active drone fleet status
- Mission log
- System statistics
"""

from flask import Flask, render_template_string, jsonify
import random
import time
from datetime import datetime
from threading import Thread

app = Flask(__name__)

# ─── Simulated Live Data ──────────────────────────────────────────────────────

THREAT_TYPES = ["Ballistic Missile", "Cruise Missile", "Attack Drone", "UAV Swarm"]

system_data = {
    "threats_detected"   : 0,
    "threats_neutralised": 0,
    "drones_active"      : 0,
    "uptime_seconds"     : 0,
    "recent_threats"     : [],
    "fleet"              : [
        {"id": f"SN-{i+1:02d}", "status": "IDLE", "battery": 100, "missions": 0}
        for i in range(6)
    ]
}

start_time = time.time()


def simulate_live_data():
    """Background thread to simulate live threat data."""
    while True:
        time.sleep(random.randint(8, 20))  # Random threat every 8-20 sec

        threat = {
            "id"         : system_data["threats_detected"] + 1,
            "type"       : random.choice(THREAT_TYPES),
            "confidence" : round(random.uniform(0.75, 0.99), 2),
            "position"   : f"({random.randint(100,900)}, {random.randint(50,300)})",
            "timestamp"  : datetime.now().strftime("%H:%M:%S"),
            "status"     : "NEUTRALISED"
        }

        system_data["threats_detected"]    += 1
        system_data["threats_neutralised"] += 1
        system_data["recent_threats"].insert(0, threat)
        system_data["recent_threats"] = system_data["recent_threats"][:10]

        # Update a random drone
        drone = random.choice(system_data["fleet"])
        drone["missions"] += 1
        drone["battery"]   = max(20, drone["battery"] - random.randint(5, 15))


# Start background simulation
thread = Thread(target=simulate_live_data, daemon=True)
thread.start()


# ─── Dashboard HTML ───────────────────────────────────────────────────────────

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="5">
<title>ShieldNet Command Centre</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0a0e1a; color: #e0e0e0; font-family: 'Courier New', monospace; }

  header {
    background: #0d1428;
    border-bottom: 2px solid #00c864;
    padding: 16px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  header h1 { color: #00c864; font-size: 1.4rem; letter-spacing: 3px; }
  header .status { color: #aaa; font-size: 0.8rem; }
  .live-dot {
    display: inline-block; width: 10px; height: 10px;
    background: #00c864; border-radius: 50%;
    animation: pulse 1.2s infinite;
    margin-right: 8px;
  }
  @keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.2;} }

  .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; padding: 20px; }

  .card {
    background: #0d1428;
    border: 1px solid #1e2d4d;
    border-radius: 8px;
    padding: 20px;
  }
  .card.green  { border-color: #00c864; }
  .card.red    { border-color: #ff4444; }
  .card.yellow { border-color: #ffcc00; }
  .card.blue   { border-color: #4488ff; }

  .card .label { font-size: 0.7rem; color: #888; letter-spacing: 2px; text-transform: uppercase; }
  .card .value { font-size: 2.5rem; font-weight: bold; margin-top: 8px; }
  .card.green  .value { color: #00c864; }
  .card.red    .value { color: #ff4444; }
  .card.yellow .value { color: #ffcc00; }
  .card.blue   .value { color: #4488ff; }

  .section { padding: 0 20px 20px; }
  .section h2 { color: #ffcc00; font-size: 0.85rem; letter-spacing: 2px;
                border-bottom: 1px solid #1e2d4d; padding-bottom: 8px; margin-bottom: 12px; }

  table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
  th { color: #888; text-align: left; padding: 6px 10px;
       border-bottom: 1px solid #1e2d4d; font-weight: normal; letter-spacing: 1px; }
  td { padding: 8px 10px; border-bottom: 1px solid #111827; }
  tr:hover td { background: #111827; }

  .badge {
    display: inline-block; padding: 2px 8px; border-radius: 4px;
    font-size: 0.72rem; font-weight: bold;
  }
  .badge.green  { background: #003318; color: #00c864; }
  .badge.red    { background: #330000; color: #ff4444; }
  .badge.yellow { background: #332200; color: #ffcc00; }
  .badge.blue   { background: #001133; color: #4488ff; }

  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

  footer {
    text-align: center; padding: 12px;
    color: #333; font-size: 0.72rem;
    border-top: 1px solid #111827;
  }
</style>
</head>
<body>

<header>
  <h1>🛡️ SHIELDNET — COMMAND CENTRE</h1>
  <div class="status">
    <span class="live-dot"></span>LIVE |
    Team CodeStorm | EQUINOX 2026 |
    {{ timestamp }}
  </div>
</header>

<!-- Stats -->
<div class="grid">
  <div class="card green">
    <div class="label">Threats Detected</div>
    <div class="value">{{ data.threats_detected }}</div>
  </div>
  <div class="card green">
    <div class="label">Threats Neutralised</div>
    <div class="value">{{ data.threats_neutralised }}</div>
  </div>
  <div class="card blue">
    <div class="label">Drones in Fleet</div>
    <div class="value">{{ data.fleet | length }}</div>
  </div>
  <div class="card yellow">
    <div class="label">System Uptime</div>
    <div class="value">{{ uptime }}</div>
  </div>
</div>

<div class="two-col section">

  <!-- Threat Log -->
  <div>
    <h2>⚠ RECENT THREAT LOG</h2>
    <table>
      <tr>
        <th>#</th><th>TIME</th><th>TYPE</th><th>CONF</th><th>STATUS</th>
      </tr>
      {% for t in data.recent_threats %}
      <tr>
        <td>{{ t.id }}</td>
        <td>{{ t.timestamp }}</td>
        <td>{{ t.type }}</td>
        <td>{{ (t.confidence * 100)|int }}%</td>
        <td><span class="badge green">{{ t.status }}</span></td>
      </tr>
      {% else %}
      <tr><td colspan="5" style="color:#555;text-align:center;">
        Monitoring... No threats detected yet.
      </td></tr>
      {% endfor %}
    </table>
  </div>

  <!-- Fleet Status -->
  <div>
    <h2>🚁 FLEET STATUS</h2>
    <table>
      <tr>
        <th>DRONE</th><th>STATUS</th><th>BATTERY</th><th>MISSIONS</th>
      </tr>
      {% for d in data.fleet %}
      <tr>
        <td>{{ d.id }}</td>
        <td>
          <span class="badge {% if d.status == 'IDLE' %}green{% else %}yellow{% endif %}">
            {{ d.status }}
          </span>
        </td>
        <td>
          <span style="color: {% if d.battery > 50 %}#00c864{% elif d.battery > 25 %}#ffcc00{% else %}#ff4444{% endif %}">
            {{ d.battery }}%
          </span>
        </td>
        <td>{{ d.missions }}</td>
      </tr>
      {% endfor %}
    </table>
  </div>

</div>

<footer>
  ShieldNet v1.0 | AI-Powered Anti-Missile Drone Defence System | Auto-refreshes every 5 seconds
</footer>

</body>
</html>
"""


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    uptime_sec = int(time.time() - start_time)
    h = uptime_sec // 3600
    m = (uptime_sec % 3600) // 60
    s = uptime_sec % 60
    uptime_str = f"{h:02d}:{m:02d}:{s:02d}"

    return render_template_string(
        DASHBOARD_HTML,
        data=system_data,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        uptime=uptime_str
    )

@app.route("/api/status")
def api_status():
    return jsonify(system_data)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  🛡️  SHIELDNET COMMAND DASHBOARD")
    print("  Open: http://localhost:5000")
    print("=" * 55)
    app.run(debug=False, host="0.0.0.0", port=5000)
