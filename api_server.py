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
# UNIFIED STORAGE LAYERS BINDING: Redirects source files toward the real output live database tracking engine
MEMORY_FILE = os.path.join(BASE_DIR, "outputs", "fusion_history.json")

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

# ============================================================ #
# REAL-TIME METRICS DYNAMIC RESOLUTION ENGINE
# ============================================================ #
def calculate_status():
    # Direct list layout extraction from the live unlinked automated reporting history logs database
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
        "findings": findings  # INJECTION PARADIGM: Passes down real runtime objects arrays to populate the supreme dashboard grid
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

        # Explicit full database files raw dump endpoint lookup boundings
        if path == "/api/dashboard/findings":
            self.send_json(load_memory())
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

# ============================================================ #
# RUNTIME START SEQUENCE BOOTSTRAPPING MATRIX
# ============================================================ #
if __name__ == "__main__":
    initialize_memory()
    print("""
 ══════════════════════════════════════════════
 ⚡ FUSION-AI // UNIFIED MEMORY API CORE v1.2
 Dashboard API: http://192.168.56.101:8000
 Endpoint:      /api/dashboard/status
 Sync Source:   outputs/fusion_history.json
 CORS Control:  ENABLED [HTTP/WS Matrix Sync]
 ══════════════════════════════════════════════
 """)
    server = HTTPServer((HOST, PORT), FusionAPIHandler)
    server.serve_forever()
