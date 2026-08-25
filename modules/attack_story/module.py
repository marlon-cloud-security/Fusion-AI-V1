# modules/attack_story/module.py
"""
Fusion-AI // Executive Attack Story Engine v3.0
Generates a boardroom-ready attack narrative from all module evidence.
"""

import os
import sys
import json
import logging
from datetime import datetime

logger = logging.getLogger("FusionEngine.Modules.AttackStory")


def run_story_pipeline(target: str):

    logger.info("[🛰️] Building executive attack narrative...")

    report_paths = [
        "outputs/json/report.json",
        "outputs/report.json"
    ]

    active_path = next((p for p in report_paths if os.path.exists(p)), None)

    if not active_path:
        return

    with open(active_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    findings = data.get("findings", [])

    ports = set()
    devices = 0
    hidden_routes = 0
    critical = 0
    http_ok = False
    httponly = False

    for f in findings:

        mod = f.get("module", "")
        desc = f.get("description", "").lower()

        port = f.get("port")
        if isinstance(port, int) and port > 0:
            ports.add(str(port))

        if mod == "iot_scan":
            devices += 1

        if mod == "ffuf":
            hidden_routes += f.get("data", {}).get("total_fuzz_hits", 0)

        if f.get("severity") in ["critical", "high"]:
            critical += 1

        if "status 200" in desc or "200 ok" in desc:
            http_ok = True

        if "httponly" in desc or "set-cookie" in desc:
            httponly = True

    ports_txt = ", ".join(sorted(ports, key=int)) if ports else "No exposed services"

    severity = "critical" if critical else "medium"

    # ------------------------------------------------------------------
    # Executive formatted report (this is what the dashboard will display)
    # ------------------------------------------------------------------

    description = f"""
═══════════════════════════════════════════════
🛰️ EXECUTIVE ATTACK STORY
Target: {target}
═══════════════════════════════════════════════

MISSION TIMELINE

① Initial Reconnaissance
• Active ports discovered: {ports_txt}

② Infrastructure Mapping
• {devices} network device(s) identified.

③ Access Validation
• {"Management interface responded successfully (HTTP 200)." if http_ok else "Management interfaces detected during validation."}

④ Surface Expansion
• {hidden_routes} hidden route(s) uncovered during web enumeration.

⑤ Final Assessment
• {critical} confirmed high-impact exposure(s).

BOARDROOM SUMMARY

Fusion-AI reconstructed the complete attack path using correlated evidence from every reconnaissance module.

The attacker was able to identify exposed network services, locate administrative interfaces, validate live responses, and expand visibility into hidden application resources.

{"Session protection mechanisms were observed during HTTP validation." if httponly else "Administrative services remain reachable from the scanned attack path."}

Immediate hardening is recommended before these exposure paths can be abused.
""".strip()

    remediation = """
PRIORITY ACTION PLAN

🔴 Immediate
• Restrict router administration access.
• Close unnecessary exposed services.

🟠 High
• Disable unused remote management features.
• Harden HTTP/HTTPS configurations.

🟢 Recommended
• Segment IoT devices.
• Rotate administrator credentials.
• Review hidden application resources discovered during enumeration.
""".strip()

    master_card = {
        "id": "fusion-master-attack-story",
        "module": "attack_story",
        "type": "executive_summary",
        "title": "🛰️ EXECUTIVE ATTACK STORY",
        "severity": severity,
        "description": description,
        "remediation": remediation,
        "port": 0,
        "url": None,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": {
            "ports": sorted(list(ports), key=int) if ports else [],
            "devices": devices,
            "hidden_routes": hidden_routes,
            "confirmed_exposures": critical
        }
    }

    for path in report_paths:

        try:

            if os.path.exists(path):

                with open(path, "r", encoding="utf-8") as f:
                    report = json.load(f)

            else:

                report = {
                    "target": target,
                    "findings": []
                }

            report.setdefault("findings", [])

            report["findings"] = [
                x for x in report["findings"]
                if x.get("id") != master_card["id"]
            ]

            report["findings"].insert(0, master_card)
            report["created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open(path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=4, ensure_ascii=False)

        except Exception as e:
            logger.error(str(e))

    print("\n" + "═"*70)
    print(" 🛰️ FUSION-AI EXECUTIVE ATTACK STORY GENERATED")
    print(f" Target: {target}")
    print("═"*70 + "\n")
    sys.stdout.flush()
