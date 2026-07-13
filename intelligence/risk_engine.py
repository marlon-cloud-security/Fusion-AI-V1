import logging
from typing import Dict, Any
from core.types import ScanContext, Severity

logger = logging.getLogger("FusionEngine.RiskEngine")

class RiskEngine:

    def __init__(self):
        self.severity_weights = {
            Severity.INFO: 1,
            Severity.LOW: 5,
            Severity.MEDIUM: 15,
            Severity.HIGH: 35,
            Severity.CRITICAL: 60
        }

        # servicios que elevan riesgo aunque no sean exploit directo
        self.high_risk_services = {
            "telnet", "ftp", "rsh", "rpcbind", "netbios-ssn",
            "vnc", "mysql", "postgresql"
        }

    def evaluate_context(self, context: ScanContext) -> Dict[str, Any]:

        if not context.findings:
            return {
                "risk_score": 0,
                "verdict": "SECURE",
                "highest_severity": "info",
                "business_impact": "No exposure detected."
            }

        base_score = 0
        highest = Severity.INFO
        service_risk_bonus = 0

        for f in context.findings:
            base_score += self.severity_weights.get(f.severity, 0)

            # track highest severity
            if f.severity.value in ["medium", "high", "critical"]:
                highest = f.severity

            # boost for dangerous services
            service = (f.data or {}).get("service", "").lower()
            if service in self.high_risk_services:
                service_risk_bonus += 8

        # attack surface multiplier
        surface_multiplier = 1 + (len(context.findings) / 50)

        raw_score = (base_score + service_risk_bonus) * surface_multiplier

        # clamp 0–100
        score = max(0, min(100, int(raw_score)))

        # verdict logic realista
        if score >= 75:
            verdict = "CRITICAL_RISK"
            impact = "Critical attack surface exposed. Immediate hardening required."
        elif score >= 45:
            verdict = "MEDIUM_RISK"
            impact = "Multiple exposed services detected. Attack surface non-trivial."
        else:
            verdict = "LOW_RISK"
            impact = "Limited exposure, but monitoring recommended."

        logger.info(f"Risk computed | score={score} | verdict={verdict}")

        return {
            "risk_score": score,
            "verdict": verdict,
            "highest_severity": highest.value,
            "business_impact": impact
        }
