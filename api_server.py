#!/usr/bin/env python3
"""
FUSION-AI // DASHBOARD API MEMORY CORE v1.3
Central API layer between:
- Neon Dashboard
- Reporting Engine
- Scan Memory
- SOAR Services

Port: 8000
"""

import os
import json
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

HOST = "127.0.0.1"
PORT = 8000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(BASE_DIR, "outputs", "fusion_history.json")
ENGINE_FILE = os.path.join(BASE_DIR, "outputs", "engine_status.json")

memory_lock = threading.Lock()

# ============================================================ #
# UNIFIED DATABASE SYSTEM OPERATIONS INFRASTRUCTURE
# ============================================================ #
def initialize_memory():
    """ Ensures database structures are mapped correctly before any fetch operation triggers """
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)

def load_memory():
    with memory_lock:
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            return []

def save_memory(data):
    with memory_lock:
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

def load_engine_status():
    """
    Reads the live engine telemetry without affecting
    the findings database.
    """
    try:
        with open(ENGINE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {
            "engine": "OFFLINE",
            "batch": 0,
            "mode": "UNKNOWN",
            "health": 0,
            "elapsed": "00:00",
            "stream": "OFFLINE",
            "nuclei": {
                "status": "OFFLINE",
                "last_match": "Unavailable",
                "matches": 0
            }
        }

# ============================================================ #
# REAL-TIME METRICS DYNAMIC RESOLUTION ENGINE
# ============================================================ #
def calculate_status():
    findings = load_memory()
    if not isinstance(findings, list):
        findings = []
    
    critical = 0
    high = 0
    medium = 0
    low = 0
    
    for item in findings:
        severity = str(item.get("severity", "")).lower()
        if severity == "critical":
            critical += 1
        elif severity == "high":
            high += 1
        elif severity == "medium":
            medium += 1
        elif severity == "low":
            low += 1
            
    return {
        "status": "ONLINE",
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_findings": len(findings),
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "findings": findings  
    }

# ============================================================ #
# ADVANCED EXECUTIVE SECURITY POSTURE CALCULATOR ENGINE
# ============================================================ #
def calculate_security_posture():
    """
    📊 DYNAMIC INTEL POSTURE INTERPRETER
    Parses unlinked logging streams and cross-references active module tags 
    to map architectural findings into real asset evaluation metrics.
    """

    findings = load_memory()

    if not isinstance(findings, list):
        findings = []

    devices = 0
    services = 0
    weak_points = 0
    confirmed = 0

    for item in findings:

        module = str(item.get("module", "")).upper()
        severity = str(item.get("severity", "")).lower()
        title = str(item.get("title", "")).lower()
        finding_type = str(item.get("type", "")).lower()


        # 🟢 Devices discovered classifier matrix
        if "IOT_SCAN" in module or "device" in title:
            devices += 1


        # 🟡 Services exposed map infrastructure resolution
        if "NMAP" in module:
            services += 1


        # 🟠 Weak points detected surface mapping (Recon components)
        if any(x in module for x in [
            "FFUF",
            "GOBUSTER",
            "HTTPX",
            "KATANA",
            "PROTOCOL_HEURISTIC"
        ]):
            weak_points += 1


        # 🔴 Confirmed vulnerabilities explicit validations
        if severity in ["critical", "high"] or any(x in title for x in [
            "cve",
            "exploit",
            "vulnerability validated"
        ]):
            confirmed += 1


    return {
        "devices_discovered": devices,
        "services_exposed": services,
        "weak_points_detected": weak_points,
        "confirmed_vulnerabilities": confirmed
    }
# ============================================================ #
# HTTP API SERVER CORE LAYER WITH ENFORCED CORS MANAGEMENT
# ============================================================ #
class FusionAPIHandler(BaseHTTPRequestHandler):
    
    def send_json(self, payload):
        data = json.dumps(payload, indent=4).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        """ Handles complex asynchronous browser CORS pre-flight handshake tracking procedures safely """
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path

        # Real-time metrics statistical calculations dashboard pipeline mapping
        if path == "/api/dashboard/status":
            self.send_json(calculate_status())
            return

        # 📊 EXECUTIVE SECURITY POSTURE ENDPOINT RESOLUTION
        if path == "/api/dashboard/posture":
            self.send_json(calculate_security_posture())
            return

        # Explicit full database files raw dump endpoint lookup boundings
        if path == "/api/dashboard/findings":
            self.send_json(load_memory())
            return

        # ⚡ ENGINE LIVE TELEMETRY
        if path == "/api/dashboard/engine":
            self.send_json(load_engine_status())
            return

        # General system environmental check loop trace validation parameters
        if path == "/api/health":
            self.send_json({
                "fusion": "online",
                "time": datetime.now().isoformat()
            })
            return

        self.send_response(404)
        self.end_headers()

# ================================================================= #
# RUNTIME START SEQUENCE BOOTSTRAPPING MATRIX                      #
# ================================================================= #

def run_server(host_ip="127.0.0.1", port_num=8000):
    """
    AUTONOMOUS API SERVER DAEMON LAUNCHER
    Allows the HTTP server instance to be dynamically invoked by main.py 
    inside an isolated asynchronous background memory process window.
    """
    initialize_memory()
    print(f"""
 ⚡ FUSION-AI // UNIFIED MEMORY API CORE v1.3
 Dashboard API:   http://{host_ip}:{port_num}
 Core Status:     /api/dashboard/status
 Executive Intel: /api/dashboard/posture
 Sync Source:     outputs/fusion_history.json
 CORS Control:    ENABLED [HTTP/WS Matrix Sync]
    """)
    try:
        server = HTTPServer((host_ip, port_num), FusionAPIHandler)
        server.serve_forever()
    except Exception:
        pass

if __name__ == "__main__":
    # Maintained for backwards compatibility and standalone manual invocation
    run_server("127.0.0.1", 8000)
