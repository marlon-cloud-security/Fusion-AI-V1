# core/types.py
import uuid
import logging
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional

logger = logging.getLogger("FusionEngine.Types")

class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Finding:
    """Represents a normalized technical security finding used as raw evidence."""
    def __init__(
        self,
        module: str,
        finding_type: str,
        title: str,
        severity: Severity,
        data: Dict[str, Any],
        description: str = "",
        remediation: str = "",
        port: Optional[int] = None,
        url: Optional[str] = None
    ):
        self.id = str(uuid.uuid4())
        self.module = module
        self.finding_type = finding_type
        self.title = title
        self.severity = severity
        self.data = data
        self.description = description
        self.remediation = remediation
        self.port = port
        self.url = url
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "module": self.module,
            "type": self.finding_type,
            "title": self.title,
            "severity": self.severity.value,
            "description": self.description,
            "remediation": self.remediation,
            "port": self.port,
            "url": self.url,
            "timestamp": self.timestamp,
            "data": self.data
        }

class AssetHost:
    """
    The Asset Model.
    Comprehensive knowledge graph representing the true state of a target host.
    """
    def __init__(self, ip_address: str):
        self.ip_address = ip_address
        self.hostname: str = "unknown"
        self.os: str = "unknown"
        
        # Structured operational buckets
        self.open_ports: List[Dict[str, Any]] = []      # Filled by Nmap / Protocol
        self.web_servers: List[Dict[str, Any]] = []     # Filled by Httpx / WhatWeb
        self.technologies: List[str] = []               # Filled by WhatWeb
        self.directories: List[str] = []                # Filled by Katana / Ffuf / Gobuster
        self.vulnerabilities: List[Dict[str, Any]] = []  # Filled by Nuclei / Sqlmap
        self.credentials: List[Dict[str, Any]] = []      # Filled by future brute-force/leak modules
        self.risk_metrics: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ip_address": self.ip_address,
            "hostname": self.hostname,
            "os": self.os,
            "open_ports": self.open_ports,
            "web_servers": self.web_servers,
            "technologies": self.technologies,
            "directories": self.directories,
            "vulnerabilities": self.vulnerabilities,
            "credentials": self.credentials,
            "risk_metrics": self.risk_metrics
        }

class ScanContext:
    """The central intelligence data bus traveling through the dynamic Fusion-AI pipeline."""
    def __init__(self, target: str):
        self.target = target
        self.findings: List[Finding] = []
        
        # Memory map signatures to prevent duplicate items per specific injection slot
        self.processed_signatures: set[str] = set()

        # self.processed_signatures = set()

        # The core Asset tracking structure
        self.asset = AssetHost(ip_address=target)

        # Cross-feeding internal control parameters
        self.open_ports: List[int] = []
        self.web_targets: List[str] = []
        self.vulnerable_urls: List[str] = []
        self.metadata: Dict[str, Any] = {}

    def add_finding(self, finding: Finding) -> bool:
        """
        Robust Contextual Deduplication Engine.
        Generates uniquely isolated target signatures utilizing technical asset footprints.
        Triggers real-time asynchronous publishing bounds toward the centralized API Event Bus.
        """
        # Contextual identifier mapping sequence scope_location
        scope_location = finding.url if finding.url else (f"{self.target}:{finding.port}" if finding.port else self.target)
        
        # Absolute uniqueness mapping tuple footprint signature
        signature = f"{finding.module}:{finding.finding_type}:{scope_location}:{finding.title}"
        
        if signature in self.processed_signatures:
            logger.debug(f"Deduplication engine filtered duplicate finding: {signature}")
            return False
            
        self.processed_signatures.add(signature)
        self.findings.append(finding)
        
        # -----------------------------------------------------------------
        # AUTONOMOUS EVENT BUS INTERCEPTION LAYER (REAL-TIME LIVE SYNC)
        # -----------------------------------------------------------------
        try:
            from core.live_sync import live_sync_bus
            live_sync_bus.publish_finding(finding)
        except Exception:
            # Silent safety passthrough fallback to preserve primary engine execution stability
            pass

        return True
