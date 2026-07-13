# main.py
"""
Fusion-AI // Central Autonomous Orchestrator Core.
Open-Source Enterprise Freemium Pipeline Infrastructure.
Coordinates sequential high-velocity asset mapping & vulnerability discovery.
"""

import json
import sys
import logging
from core.engine import FusionEngine
from core.plugin_loader import PluginLoader
from intelligence.risk_engine import RiskEngine
from core.types import ScanContext, Finding, Severity
from reporting.report import archive_pipeline_report

def main():
    print("\n" + "=" * 60)
    print("      🛡️  FUSION-AI SECURITY INTELLIGENCE ENGINE v1.0  🛡️")
    print("=" * 60)

    # Initialize core autonomous orchestrator and intelligence engines
    engine = FusionEngine()
    loader = PluginLoader()
    risk_engine = RiskEngine()

    # Automatically discover and register all plugin modules from the modules tree
    loader.load_plugins(engine)

    # Capture the operational target via a clean unattended-ready input stream
    target = input("\nEnter target infrastructure (IP or Domain): ").strip()
    if not target:
        target = "192.168.56.102"
        print(f"Using default infrastructure sandbox target: {target}")

    # FULL INTERCONNECTED EXPLOITATION WORKFLOW (Katana -> Gobuster -> Ffuf -> Nuclei -> SQLMap)
    scan_report = engine.run_pipeline(target)

    # RECONSTRUCT MEMORY LOG GRAPH MATRIX TO COMPILING STRUCTURAL RISK COEFFICIENTS
    reconstructed = ScanContext(target)

    # Map discovered tool findings directly into consolidated ScanContext structures
    for f in scan_report.get("findings", []):
        reconstructed.add_finding(
            Finding(
                module=f["module"],
                finding_type=f["type"],
                title=f["title"],
                severity=Severity(f["severity"]),
                data=f["data"],
                description=f["description"],
                remediation=f["remediation"]
            )
        )

    # Synchronize raw dynamic vulnerabilities captured down-stream into asset memory lists
    if "vulnerabilities" in scan_report:
        reconstructed.asset.vulnerabilities = scan_report["vulnerabilities"]
    else:
        # Emergency pipeline parser backup loop
        for f in scan_report.get("findings", []):
            if f["type"] in ["vulnerability", "sql_injection"]:
                reconstructed.asset.vulnerabilities.append({
                    "name": f["title"].replace("Nuclei: ", ""),
                    "severity": str(f["severity"]).split(".")[-1].lower(),
                    "matched_at": f.get("url", target),
                    "template": f.get("data", {}).get("template_id", "unknown")
                })

    # Trigger centralized risk triage evaluation models
    risk = risk_engine.evaluate_context(reconstructed)
    scan_report["risk_intelligence"] = risk

    # Commit the fully parsed data report to local json database logs
    try:
        archive_pipeline_report(scan_report)
        print("\n" + "═" * 60)
        print(" 🎉 [✔] FUSION-AI PIPELINE WORKFLOW COMPLETE")
        print(" [🎯] Cyberpunk Real-Time HTML Dashboard Initialized: outputs/")
        print(" [📊] Global JSON Ledger successfully committed to database logs.")
        print("═" * 60 + "\n")
    except Exception:
        pass

    # Clean JSON object dump to standard output for upstream monitoring tools
    print("\n" + "=" * 60)
    print(json.dumps(scan_report, indent=4, ensure_ascii=False))
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
