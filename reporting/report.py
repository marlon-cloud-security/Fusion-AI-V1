# reporting/report.py
import logging
import json
import os
import sys
import socket
import uuid
from datetime import datetime
from typing import Dict, Any, List
from core.types import ScanContext

logger = logging.getLogger("FusionEngine.Reporting.ReportGenerator")

# ============================================================================ #
# FUSION-AI MEMORY CORE ENGINE
# Persistent intelligence storage layer
# ============================================================================ #
BASE_OUTPUT_DIR = "outputs"
HISTORY_DATABASE = os.path.join(BASE_OUTPUT_DIR, "fusion_history.json")
REMEDIATION_DATABASE = os.path.join(BASE_OUTPUT_DIR, "fusion_remediation_history.json")

def ensure_storage():
    os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)
    if not os.path.exists(HISTORY_DATABASE):
        with open(HISTORY_DATABASE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)
    if not os.path.exists(REMEDIATION_DATABASE):
        with open(REMEDIATION_DATABASE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4)

def load_json_database(path):
    ensure_storage()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as error:
        logger.error(f"Database load failure {path}: {error}")
        return []

def save_json_database(path, data):
    ensure_storage()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as error:
        logger.error(f"Database commit failure {path}: {error}")

# ============================================================================ #
# NETWORK IDENTITY RESOLUTION
# ============================================================================ #
def get_live_attacker_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"

# ============================================================================ #
# HISTORICAL FINDING MEMORY
# ============================================================================ #
def archive_pipeline_report(scan_report: Dict[str, Any]):
    try:
        history = load_json_database(HISTORY_DATABASE)
        scan_report["record_id"] = str(uuid.uuid4())
        scan_report["created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history.append(scan_report)
        save_json_database(HISTORY_DATABASE, history)
    except Exception as error:
        logger.error(f"Historical archive failure: {error}")

def register_remediation_event(data):
    remediation = load_json_database(REMEDIATION_DATABASE)
    data["ticket"] = "FX-" + str(uuid.uuid4())[:8].upper()
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    remediation.append(data)
    save_json_database(REMEDIATION_DATABASE, remediation)

def calculate_live_metrics():
    history = load_json_database(HISTORY_DATABASE)
    critical = 0
    high = 0
    medium = 0
    for item in history:
        severity = str(item.get("severity", "")).lower()
        if "critical" in severity:
            critical += 1
        elif "high" in severity:
            high += 1
        elif "medium" in severity:
            medium += 1
    return {
        "critical": critical,
        "high": high,
        "medium": medium,
        "total_findings": len(history),
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
# ============================================================================ #
# REPORT GENERATOR CORE
# ============================================================================ #
class ReportGenerator:
    def __init__(self, context: ScanContext):
        ensure_storage()
        self.context = context
        self.output_dir = BASE_OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        self.target_ip = context.target if context.target else "Unknown Target"
        self.hacker_ip = get_live_attacker_ip()
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.analyst_name = getattr(context, "analyst_name", "Lead Cyber Operator")
        self.corporate_email = getattr(context, "corporate_email", "soc@fusion-ai.open")
        self.license_tier = getattr(context, "license_tier", "FREEMIUM")
        
        self.os_type = "Linux Operating System Environment"
        if hasattr(context, "asset"):
            if hasattr(context.asset, "technologies"):
                techs = [str(t).lower() for t in context.asset.technologies]
                if any("windows" in t for t in techs):
                    self.os_type = "Microsoft Windows Server Infrastructure"
                elif any("docker" in t or "kubernetes" in t for t in techs):
                    self.os_type = "Containerized Cloud Architecture"

    def generate_html_report(self, findings: List[Any], report_name: str = "fusion_neon_dashboard.html") -> str:
        report_path = os.path.join(self.output_dir, report_name)
        resolved_hacker_ip = self.hacker_ip
        
        metrics = calculate_live_metrics()
        critical_count = metrics["critical"]
        high_count = metrics["high"]
        medium_count = metrics["medium"]
        total_exploits = metrics["total_findings"]
        
        cards_html_buffer = self._compile_vulnerability_cards(findings)

        html_template = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fusion-AI // Autonomous Penetration Matrix Suite</title>
    <style>
        :root {
            --bg: #05050a;
            --panel: #0d0d1a;
            --green: #39ff14;
            --cyan: #00f3ff;
            --pink: #ff007f;
            --yellow: #fff01f;
            --red: #ff003c;
            --text: #e8e8ef;
            --border: #1c1c35;
        }
        * { box-sizing: border-box; }
        body {
            background: radial-gradient(circle at top, #101025, var(--bg));
            color: var(--text);
            font-family: "Courier New", monospace;
            margin: 0;
            padding: 25px;
        }
        #gatekeeper-overlay {
            position: fixed;
            inset: 0;
            background: rgba(2,2,8,.98);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }
        .login-box {
            width: 480px;
            background: linear-gradient(145deg, #111122, #05050c);
            border: 2px solid var(--cyan);
            padding: 35px;
            box-shadow: 0 0 35px rgba(0,243,255,.35);
        }
        .splash-title { color: var(--green); font-size: 24px; font-weight: bold; text-align: center; text-shadow: 0 0 20px var(--green); margin-bottom: 5px; }
        .splash-phrase { text-align: center; margin: 15px 0; color: white; font-style: italic; }
        .form-input { width: 100%; background: #020205; border: 1px solid var(--border); padding: 12px; color: white; margin-top: 8px; font-family: monospace; }
        .form-input:focus { border-color: var(--green); outline: none; box-shadow: 0 0 15px rgba(57,255,20,.5); }
        .btn-neon { background: transparent; padding: 12px 18px; border: 2px solid var(--cyan); color: var(--cyan); cursor: pointer; font-weight: bold; transition: .3s; width: 100%; margin-top: 20px; font-family: monospace; }
        .btn-neon:hover { background: var(--cyan); color: #000; box-shadow: 0 0 25px var(--cyan); }
        .btn-premium { border-color: var(--green); color: var(--green); }
        .btn-premium:hover { background: var(--green); box-shadow: 0 0 30px var(--green); }
        .btn-remediate { border-color: var(--yellow); color: var(--yellow); width: auto; margin-top: 10px;}
        .btn-remediate:hover { background: var(--yellow); color: black; box-shadow: 0 0 30px var(--yellow); }
        .btn-autonomous { border-color: var(--pink); color: var(--pink); width: auto; margin-top: 0; }
        .btn-autonomous:hover { background: var(--pink); color: white; box-shadow: 0 0 35px var(--pink); }
        header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--cyan); padding-bottom: 20px; margin-bottom: 25px; }
        .brand { font-size: 28px; font-weight: bold; color: var(--green); text-shadow: 0 0 20px var(--green); }
        .license-tag { color: var(--pink); letter-spacing: 2px; }
        .session-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px,1fr)); gap: 15px; background: #090915; padding: 20px; border-left: 4px solid var(--pink); }
        .meta-item span { color: var(--cyan); font-weight: bold; }
        .stats-banner { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px,1fr)); gap: 20px; margin: 30px 0; }
        .stat-box { background: var(--panel); padding: 20px; text-align: center; border: 1px solid var(--border); }
        .stat-num { font-size: 40px; font-weight: bold; }
        .vuln-card { background: linear-gradient(145deg, #10101d, #070711); border: 1px solid var(--border); padding: 25px; margin-bottom: 25px; transition: .4s; }
        .vuln-card:hover { border-color: var(--green); box-shadow: 0 0 25px rgba(57,255,20,.35); transform: translateY(-3px); }
        .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .badge { padding: 6px 12px; font-weight: bold; text-transform: uppercase; }
        .badge.critical { color: var(--pink); border: 1px solid var(--pink); }
        .badge.high { color: var(--yellow); border: 1px solid var(--yellow); }
        .badge.medium { color: var(--cyan); border: 1px solid var(--cyan); }
        .badge.low { color: var(--green); border: 1px solid var(--green); }
        .data-label { color: #888; font-size: 12px; font-weight: bold; margin-bottom: 5px; }
        .terminal-block { background: #020205; border: 1px solid #1c1c35; padding: 12px; color: #a9a9b3; font-size: 13px; white-space: pre-wrap; overflow-x: auto; margin-top: 5px; }
        .cmd-block { color: var(--cyan); }
    </style>
</head>
<body>
    <div id="gatekeeper-overlay">
        <div>
            <div class="splash-title">FUSION-AI // MATRIX CONTROL</div>
            <div class="splash-phrase">"AND GOD SAID, LET THERE BE LIGHT!"</div>
            <div class="login-box">
                <label style="color:white; font-weight:bold; font-size:12px;">AUDITOR IDENTITY</label>
                <input id="input-analyst" class="form-input" value="Lead Cyber Operator">
                
                <label style="color:white; font-weight:bold; font-size:12px; margin-top:15px; display:block;">CORPORATE EMAIL</label>
                <input id="input-email" class="form-input" value="soc@fusion-ai.open">
                
                <label style="color:white; font-weight:bold; font-size:12px; margin-top:15px; display:block;">TARGET INFRASTRUCTURE (IP/HOST)</label>
                <input id="input-target" class="form-input" value="TARGET_IP_PLACEHOLDER">
                
                <label style="color:white; font-weight:bold; font-size:12px; margin-top:15px; display:block;">MEMBERSHIP LICENSE SELECTION</label>
                <select id="input-tier" class="form-input" style="background:#020205; color:white;">
                    <option value="FREEMIUM">FREEMIUM (Basic Auditing Logs Only)</option>
                    <option value="PREMIUM">PREMIUM (Manual Exploitation Access)</option>
                    <option value="ENTERPRISE">ENTERPRISE (Full Autonomous Remediation SOAR)</option>
                </select>
                <br><br>
                <button class="btn-neon btn-premium" style="width: 100%;" onclick="validateGatekeeperMatrix()">IGNITE & ENTER MATRIX</button>
            </div>
        </div>
    </div>

    <header>
        <div>
            <div class="brand">FUSION-AI // MATRIX CONTROL</div>
            <div class="license-tag">OPERATIONAL TIER: <span id="lbl-tier">FREEMIUM</span></div>
        </div>
        <div>
            <button id="btn-profile" class="btn-neon" style="width:auto; margin-top:0;" onclick="openProfileEditor()">⚙ PROFILE</button>
            <button id="btn-autonomous" class="btn-neon btn-autonomous">🤖 AUTONOMOUS FX</button>
        </div>
    </header>

    <main>
        <div class="session-grid">
            <div class="meta-item"><span>AUDITOR:</span> <span id="lbl-analyst">Pending Credentials</span></div>
            <div class="meta-item"><span>EMAIL:</span> <span id="lbl-email">Pending Credentials</span></div>
            <div class="meta-item"><span>TARGET HOST:</span> <span id="lbl-target-display">TARGET_IP_PLACEHOLDER</span></div>
            <div class="meta-item"><span>ATTACK PLATFORM:</span> HACKER_IP_PLACEHOLDER</div>
            <div class="meta-item"><span>FINGERPRINTED OS:</span> OS_TYPE_PLACEHOLDER</div>
            <div class="meta-item"><span>TIMESTAMP:</span> TIMESTAMP_PLACEHOLDER</div>
        </div>
        <br><br>

        <div class="stats-banner">
            <div class="stat-box" style="border-top: 3px solid var(--pink);">
                <div id="critical-count" class="stat-num" style="color: var(--pink);">CRITICAL_COUNT_PLACEHOLDER</div>
                <div class="data-label">CRITICAL IMPACTS</div>
            </div>
            <div class="stat-box" style="border-top: 3px solid var(--yellow);">
                <div id="high-count" class="stat-num" style="color: var(--yellow);">HIGH_COUNT_PLACEHOLDER</div>
                <div class="data-label">HIGH EXPLOITS</div>
            </div>
            <div class="stat-box" style="border-top: 3px solid var(--cyan);">
                <div id="medium-count" class="stat-num" style="color: var(--cyan);">MEDIUM_COUNT_PLACEHOLDER</div>
                <div class="data-label">MEDIUM BREACHES</div>
            </div>
            <div class="stat-box" style="border-top: 3px solid var(--green);">
                <div id="total-count" class="stat-num" style="color: var(--green);">TOTAL_EXPLOITS_PLACEHOLDER</div>
                <div class="data-label">TOTAL LIVE DISCOVERIES</div>
            </div>
        </div>

        <h2 style="color: var(--cyan); border-bottom: 1px solid var(--border); padding-bottom: 8px;">🛡️ SECURITY TARGET EXPLORATION REVELATIONS</h2>
        <div class="cards-container">CARDS_BUFFER_PLACEHOLDER</div>
    </main>
<script>

let currentTierMode = "FREEMIUM";
let isSessionAuthenticated = false;
let liveFindings = [];

// ==========================================================
// GATEKEEPER AUTHENTICATION
// ==========================================================

function validateGatekeeperMatrix() {

    const analyst = document.getElementById("input-analyst").value.trim();
    const email = document.getElementById("input-email").value.trim();
    const target = document.getElementById("input-target").value.trim();

    const tierSelect = document.getElementById("input-tier");
    currentTierMode = tierSelect ? tierSelect.value : "FREEMIUM";

    if (!analyst || !email || !target) {

        alert("IDENTITY MATRIX ERROR: Complete all fields.");

        return;

    }

    localStorage.setItem("fusion_analyst", analyst);
    localStorage.setItem("fusion_email", email);
    localStorage.setItem("fusion_target", target);
    localStorage.setItem("fusion_tier", currentTierMode);

    isSessionAuthenticated = true;

    applySessionUI(
        analyst,
        email,
        target,
        currentTierMode
    );

    document.getElementById("gatekeeper-overlay").style.display = "none";

}            
            // Sincronización asíncrona segura
            initializeLiveMatrix();
        }

        function applySessionUI(analyst, email, target, tier){
            document.getElementById("lbl-analyst").innerText = analyst;
            document.getElementById("lbl-email").innerText = email;
            document.getElementById("lbl-target-display").innerText = target;
            document.getElementById("lbl-tier").innerText = tier;
        }

        function openProfileEditor(){
            if(!isSessionAuthenticated){ alert("Authentication required"); return; }
            let newTarget = prompt("NEW TARGET INFRASTRUCTURE:");
            if(newTarget){
                document.getElementById("lbl-target-display").innerText = newTarget;
            }
        }

        async function initializeLiveMatrix() {
            console.log("🟢 FUSION-AI LIVE MEMORY ONLINE");
            syncDashboardMemory();
            setInterval(syncDashboardMemory, 10000);
        }

        async function syncDashboardMemory() {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 1500);
                const response = await fetch("http://192.168.56", { signal: controller.signal });
                clearTimeout(timeoutId);
                if (!response.ok) return;
                const data = await response.json();
                updateCounters(data);
                if (data.findings) { mergeFindings(data.findings); }
            } catch (error) {
                console.log("Fusion Memory API Standby Model Active.");
            }
        }

        function updateCounters(data){
            if(!data) return;
            if(document.getElementById("critical-count")) document.getElementById("critical-count").innerText = data.critical || 0;
            if(document.getElementById("high-count")) document.getElementById("high-count").innerText = data.high || 0;
            if(document.getElementById("medium-count")) document.getElementById("medium-count").innerText = data.medium || 0;
            if(document.getElementById("total-count")) document.getElementById("total-count").innerText = data.total_findings || 0;
        }

        function mergeFindings(incoming) {
            if (!incoming) return;
            incoming.forEach(item => {
                const exists = liveFindings.some(old => old.id === item.id);
                if (!exists) {
                    liveFindings.push(item);
                }
            });
        }

        function detonateExploitMatrix(severity, title, matchedUrl, exploitModule){
            if(severity.toLowerCase() === "info" || severity.toLowerCase() === "low"){
                alert("Informational risk vector. Verification bypassed.");
                return;
            }
            if(!isSessionAuthenticated){ alert("Authentication sequence required."); return; }
            if(currentTierMode === "FREEMIUM"){
                alert("🔒 ACCESS LOCKED\n\nManual verification requires a PREMIUM or ENTERPRISE license tier to run client verification sandboxes.");
                return;
            }
            const target = document.getElementById("lbl-target-display").innerText;
            const attacker = window.location.hostname || "127.0.0.1";
            const socket = new WebSocket("ws://" + attacker + ":8084/api/v1/detonate");
            socket.onopen = function(){
                socket.send(JSON.stringify({ target_ip: target, exploit_module: exploitModule, matched_url: matchedUrl, severity: severity, attacker_ip: attacker }));
            };
            socket.onmessage = function(event){
                alert("VERIFY ENGINE COMPLETE\n\n" + JSON.stringify(JSON.parse(event.data), null, 2));
                socket.close();
            };
        }

        function remediateVulnerabilityMatrix(severity, title, matchedUrl, exploitModule){
            if(!isSessionAuthenticated){ alert("Authentication required."); return; }
            if(currentTierMode !== "ENTERPRISE"){
                alert("🔒 FEATURE LOCKED\n\nAutomatic SOAR Remediation and patches require an ENTERPRISE membership level.");
                return;
            }
            const target = document.getElementById("lbl-target-display").innerText;
            const socket = new WebSocket("ws://" + (window.location.hostname || "127.0.0.1") + ":8085/api/v1/remediate");
            socket.onopen = function(){
                socket.send(JSON.stringify({ target_ip: target, exploit_module: exploitModule, target_url: matchedUrl, severity: severity }));
            };
            socket.onmessage = function(event){
                alert("AEGIS SOAR RESULT\n\n" + JSON.stringify(JSON.parse(event.data), null, 2));
                markAsFixed(exploitModule);
                socket.close();
            };
        }

        function markAsFixed(module){
            const cards = document.querySelectorAll(".vuln-card");
            cards.forEach(card => {
                if(card.innerHTML.includes(module)){
                    card.style.border = "2px solid #39ff14";
                    card.style.boxShadow = "0 0 30px #39ff14";
                }
            });
        }

        document.getElementById("btn-autonomous").onclick = function(){
            if(!isSessionAuthenticated){ alert("Authentication required."); return; }
            if(currentTierMode !== "ENTERPRISE"){
                alert("🔒 ACCESS LOCKED\n\nAutonomous defense architectures require ENTERPRISE mode.");
                return;
            }
            alert("🤖 AUTONOMOUS FX ENGINE ONLINE\n\nContinuous protection schedules active.");
        };

        window.onload = function(){
            console.log("FUSION-AI MATRIX SYSTEM READY");
        };
    </script>
</body>
</html>
"""
        # Unified clean replacement matrix mapping every contextual metric precisely
        html_template = html_template.replace("TARGET_IP_PLACEHOLDER", str(self.target_ip))
        html_template = html_template.replace("HACKER_IP_PLACEHOLDER", str(resolved_hacker_ip))
        html_template = html_template.replace("OS_TYPE_PLACEHOLDER", str(self.os_type))
        html_template = html_template.replace("TIMESTAMP_PLACEHOLDER", str(self.timestamp))
        html_template = html_template.replace("CRITICAL_COUNT_PLACEHOLDER", str(critical_count))
        html_template = html_template.replace("HIGH_COUNT_PLACEHOLDER", str(high_count))
        html_template = html_template.replace("MEDIUM_COUNT_PLACEHOLDER", str(medium_count))
        html_template = html_template.replace("TOTAL_EXPLOITS_PLACEHOLDER", str(total_exploits))
        html_template = html_template.replace("CARDS_BUFFER_PLACEHOLDER", cards_html_buffer)
        # Normalización de llaves para evitar conflictos de renderizado de strings literales
        html_template = html_template.replace("{{", "{")
        html_template = html_template.replace("}}", "}")

        # Proceso Único de escritura autorizado
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_template)
        return report_path

    def _compile_vulnerability_cards(self, findings: List[Any]) -> str:
        if not findings:
            return """
            <div class="stat-box" style="text-align:center; border-left:4px solid var(--cyan);">
                <div style="color:var(--cyan); font-weight:bold;">
                    NO ACTIVE VULNERABILITIES CONFIRMED IN SCAN RUNTIME LOGS
                </div>
            </div>
            """
        
        cards_buffer = []
        for idx, finding in enumerate(findings):
            title = getattr(finding, "title", "Security Flaw Vector")
            severity = str(getattr(finding, "severity", "medium")).split(".")[-1].lower()
            matched_url = getattr(finding, "url", self.target_ip)
            description = getattr(finding, "description", "No structural description metadata registered.")
            remed_strategy = getattr(finding, "remediation", "Review updates and apply patch cycles.")
            exploit_module = getattr(finding, "module", "core_exploit")
            
            card_html = f"""
            <div class="vuln-card">
                <div class="card-header">
                    <h3 style="margin:0; color:white;">[{idx + 1}] {title}</h3>
                    <span class="badge {severity}">{severity}</span>
                </div>
                <div>
                    <div class="data-label">TARGET ENTRYPOINT:</div>
                    <div style="color:var(--cyan); font-weight:bold; margin-bottom:15px;">{matched_url}</div>
                    <div class="data-label">VULNERABILITY DESCRIPTION:</div>
                    <div style="margin-bottom:15px;">{description}</div>
                    <div class="data-label">REMEDIATION STRATEGY:</div>
                    <div style="color:var(--green); background:rgba(57,255,20,0.02); padding:10px; border-left:3px solid var(--green); margin-bottom:15px;">{remed_strategy}</div>
                    <div class="action-panel" style="display:flex; gap:10px;">
                        <button class="btn-neon btn-remediate" onclick="detonateExploitMatrix('{severity}', '{title}', '{matched_url}', '{exploit_module}')">🔥 MANUAL VERIFY</button>
                        <button class="btn-neon btn-remediate" style="border-color:var(--green); color:var(--green);" onclick="remediateVulnerabilityMatrix('{severity}', '{title}', '{matched_url}', '{exploit_module}')">🛠️ AUTO FIX</button>
                    </div>
                </div>
            </div>
            """
            cards_buffer.append(card_html)
            
        footer_html = """
        <footer style="margin-top:60px; padding:30px 0; border-top:2px solid var(--green); text-align:center;">
            <div style="color:var(--green); font-size:1.3rem; font-weight:bold;">FUSION-AI // ARTIFICIAL INTELLIGENCE AT ITS FINEST</div>
            <div style="color:white; margin-top:15px; font-style:italic;">"AND GOD SAID, LET THERE BE LIGHT!"</div>
            <div style="color:var(--cyan); margin-top:15px;">PRINCIPAL OPERATIONS SIGNATURE: [ M.F.B ]</div>
        </footer>
        """
        cards_buffer.append(footer_html)
        return "\n".join(cards_buffer)




