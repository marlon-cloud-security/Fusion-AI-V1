# core/engine.py

import logging
import sys
from typing import List, Dict, Any

from core.types import ScanContext

# -----------------------------
# LOGGER CONFIGURATION
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("FusionEngine")


class FusionEngine:
    """
    Central orchestrator of Fusion-AI pipeline.
    Responsible for module execution, dependency control, and scan lifecycle.
    """

    def __init__(self):
        self.modules: Dict[str, Any] = {}

        # Strict pipeline execution order
        self.pipeline_order: List[str] = [
            "nmap",
            "iot_scan",
            "protocol",
            "httpx",
            "whatweb",
            "katana",
            "gobuster",
            "ffuf",
            "nuclei",
            "sqlmap"
        ]

    # -----------------------------
    # MODULE REGISTRATION
    # -----------------------------
    def register_module(self, name: str, module_instance: Any) -> None:
        """Register a module plugin into the engine."""
        self.modules[name] = module_instance
        logger.info(f"Module registered: {name}")

    # -----------------------------
    # DEPENDENCY VALIDATION
    # -----------------------------
    def evaluate_dependencies(self, module_name: str, context: ScanContext) -> bool:
        """
        Determines whether a module can safely execute based on ScanContext state.
        """
        web_modules = {"whatweb", "katana", "nuclei", "ffuf", "gobuster"}

        # Web pipeline dependency
        if module_name in web_modules:
            if not context.web_targets:
                logger.warning(
                    f"Skipping {module_name}: no web targets available"
                )
                return False

        # Exploitation dependency
        if module_name == "sqlmap":
            if not context.vulnerable_urls:
                logger.warning(
                    "Skipping sqlmap: no vulnerable URLs detected"
                )
                return False

        return True

# -----------------------------
# PIPELINE EXECUTION
# -----------------------------
    def run_pipeline(self, target: str) -> Dict[str, Any]:
        """
        Executes full Fusion-AI scanning pipeline with real-time reporting sync.
        """
        logger.info(f"Starting Fusion-AI pipeline on target: {target}")
        context = ScanContext(target=target)
        execution_path: List[str] = []

        for module_name in self.pipeline_order:
            module = self.modules.get(module_name)
            if not module:
                logger.debug(f"Module not loaded: {module_name}")
                continue

            if not self.evaluate_dependencies(module_name, context):
                continue

            try:
                logger.info(f"Executing module: {module_name}")
                # Each module must implement: run(context)
                module.run(context)
                execution_path.append(module_name)
                
                logger.info(
                    f"Completed module: {module_name} | Findings: {len(context.findings)}"
                )

                # -------------------------------------------------------------
                # HOT SYNC REPORTING LAYER (REAL-TIME DASHBOARD INJECTION)
                # -------------------------------------------------------------
                # -------------------------------------------------------------
                # EVENT STREAM SYNC LAYER (SPEED OPTIMIZATION)
                # -------------------------------------------------------------
                # Real-time event streaming is now managed seamlessly and 
                # concurrently by LiveSyncBus directly inside core/types.py!
                import sys
                sys.stdout.flush()
            except Exception as e:
                logger.error(
                    f"Module execution failed [{module_name}]: {str(e)}"
                )

        # Save execution trace for intelligence layer
        context.metadata["execution_path"] = execution_path
        
        return {
            "target": context.target,
            "total_findings": len(context.findings),
            "findings": [f.to_dict() for f in context.findings],
            "execution_metadata": context.metadata
        }

        # Save execution trace for intelligence layer
        context.metadata["execution_path"] = execution_path
        
        return {
            "target": context.target,
            "total_findings": len(context.findings),
            "findings": [f.to_dict() for f in context.findings],
            "execution_metadata": context.metadata
        }
