# intelligence/adaptive_engine.py

import logging
import time
import requests
import statistics
from typing import Dict, Any

logger = logging.getLogger("FusionEngine.Intelligence.AdaptiveEngine")

class AdaptiveEngine:
    """
    Enterprise-Grade Adaptive Execution Engine.
    Profiles target network responses dynamically and alters pipeline velocity
    between micro-batches based on real-time feedback loops and telemetry data.
    """

    def __init__(self, context: Any):
        self.context = context
        base_url = context.web_targets if context.web_targets else context.target
        if isinstance(base_url, list) and base_url:
            base_url = base_url[0]
        if not str(base_url).startswith("http"):
            base_url = f"http://{base_url}"
        self.target_url = str(base_url)

    def calculate_adaptive_profile(self) -> Dict[str, Any]:
        """
        Executes a dynamic handshake sequence to analyze network throughput capabilities.
        Initializes the cache profile if not present.
        """
        if hasattr(self.context, "adaptive_profile_cache"):
            return self.context.adaptive_profile_cache

        logger.info(f"Adaptive Engine initializing calibration loop over host: {self.target_url}")
        
        latencies = []
        ssl_verify = True
        headers = {"User-Agent": "Fusion-AI/1.0-Enterprise"}

        for i in range(3):
            try:
                start_time = time.time()
                try:
                    response = requests.head(self.target_url, timeout=4.0, verify=ssl_verify, headers=headers)
                except requests.exceptions.SSLError:
                    ssl_verify = False
                    response = requests.head(self.target_url, timeout=4.0, verify=False, headers=headers)
                except Exception:
                    response = requests.get(self.target_url, timeout=4.0, verify=ssl_verify, headers=headers)

                latencies.append(time.time() - start_time)
            except Exception:
                latencies.append(4.0)

        median_latency = statistics.median(latencies)
        logger.info(f"Target profile response median finalized | Median Latency: {median_latency:.3f}s")

        # ARMORED SPEED PROFILES: Lowered concurrency and rates to strictly match lab RAM bounds
        if median_latency < 0.15:
            profile = {"concurrency": 20, "bulk_size": 1, "timeout": 4, "rate_limit": 25, "pacing": "aggressive"}
        elif median_latency < 0.50:
            profile = {"concurrency": 12, "bulk_size": 1, "timeout": 5, "rate_limit": 15, "pacing": "balanced"}
        else:
            profile = {"concurrency": 4, "bulk_size": 1, "timeout": 6, "rate_limit": 6, "pacing": "safe"}

        self.context.adaptive_profile_cache = profile
        logger.info(f"Dynamic Adaptive Profile committed | Selected Pacing: {profile['pacing'].upper()}")
        return profile

    def update_profile_from_telemetry(self, timeouts: int, errors: int, health_score: int) -> Dict[str, Any]:
        """
        Real-time telemetry correction engine. Acts as a strict TCP congestion loop.
        Drops velocities instantly if network degradation or SYN_SENT bottlenecks are caught.
        """
        profile = self.calculate_adaptive_profile()
        current_pacing = profile.get("pacing", "balanced")

        # REGLA 1: Caída de salud moderada o presencia incipiente de Timeouts
        if health_score < 90 or timeouts >= 1:
            if current_pacing == "aggressive":
                logger.warning("🚨 [ADAPTIVE CONTROL] SYN_SENT load or timeouts detected. Dropping down to BALANCED mode.")
                profile.update({"concurrency": 12, "bulk_size": 1, "timeout": 5, "rate_limit": 15, "pacing": "balanced"})
            elif current_pacing == "balanced":
                logger.warning("🚨 [ADAPTIVE CONTROL] Persistent network distress. Dropping down to SAFE MODE.")
                profile.update({"concurrency": 4, "bulk_size": 1, "timeout": 6, "rate_limit": 5, "pacing": "safe"})
        
        # REGLA 2: Caída crítica de salud (Hosts saturados por completo)
        elif health_score < 50 or timeouts > 5:
            logger.critical("🛑 [ADAPTIVE CONTROL] Target host in high-distress zone. Enforcing MAXIMUM throttling footprints.")
            profile.update({"concurrency": 2, "bulk_size": 1, "timeout": 7, "rate_limit": 3, "pacing": "safe"})

        # REGLA 3: Estabilización completa y limpia de la red
        elif health_score >= 98 and timeouts == 0 and errors == 0:
            if current_pacing == "safe":
                logger.info("📈 [ADAPTIVE CONTROL] Target network stabilized. Moving back up to BALANCED pacing.")
                profile.update({"concurrency": 12, "bulk_size": 1, "timeout": 5, "rate_limit": 15, "pacing": "balanced"})

        self.context.adaptive_profile_cache = profile
        return profile
