#!/usr/bin/env python3
"""
FUSION-AI // DASHBOARD API MEMORY CORE
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

HOST = "192.168.56.101"
PORT = 8000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MEMORY_FILE = os.path.join(DATA_DIR, "fusion_memory.json")

os.makedirs(DATA_DIR, exist_ok=True)
memory_lock = threading.Lock()

# ============================================================ #
# MEMORY ENGINE
# ============================================================ #
def initialize_memory():
    if not os.path.exists(MEMORY_FILE):
        initial = {
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "findings": [],
            "history": []
        }
        save_memory(initial)

def load_memory():
    with memory_lock:
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            return {"findings": [], "history": []}

def save_memory(data):
    with memory_lock:
        with open(MEMORY_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

# ============================================================ #
# DASHBOARD STATISTICS & DATA INJECTION
# ============================================================ #
def calculate_status():
    memory = load_memory()
    findings = memory.get("findings", [])
    
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
        "memory_entries": len(memory.get("history", [])),
        "findings": findings  # CORRECCIÓN EXPLICITA: Entrega el buffer para que JS renderice las tarjetas dinámicamente
    }

# ============================================================ #
# HTTP API SERVER WITH ADVANCED CORS CONTROL
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
        """ Manejo nativo de pre-vuelo CORS para evitar bloqueos en navegadores """
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path

        # ==================================================
        # Dashboard live status
        # ==================================================
        if path == "/api/dashboard/status":
            self.send_json(calculate_status())
            return

        # ==================================================
        # Full findings memory
        # ==================================================
        if path == "/api/dashboard/findings":
            self.send_json(load_memory())
            return

        # ==================================================
        # Health check
        # ==================================================
        if path == "/api/health":
            self.send_json({
                "fusion": "online",
                "time": datetime.now().isoformat()
            })
            return

        self.send_response(404)
        self.end_headers()

# ============================================================ #
# START
# ============================================================ #
if __name__ == "__main__":
    initialize_memory()
    print("""
 ══════════════════════════════════════════════
 ⚡ FUSION-AI // MEMORY API CORE v1.1
 Dashboard API: http://192.168.56.101:8000
 Endpoint:      /api/dashboard/status
 Memory:        data/fusion_memory.json
 CORS Control:  ENABLED [HTTP/WS Matrix Sync]
 ══════════════════════════════════════════════
 """)
    server = HTTPServer((HOST, PORT), FusionAPIHandler)
    server.serve_forever()
