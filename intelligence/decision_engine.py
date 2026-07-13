# intelligence/decision_engine.py

import logging
from typing import List, Dict, Any
from urllib.parse import urlparse, parse_qs
import re
from core.types import ScanContext

logger = logging.getLogger("FusionEngine.Intelligence.DecisionEngine")

class DecisionEngine:
    """
    Universal Autonomous Attack Planner (Zero Fixed Technology Params).
    Dynamically maps living framework signatures discovered by WhatWeb/Httpx/Nmap 
    into strict localized scanning vectors to maximize speed across any platform 
    (Windows, Cloud, Containers, Node.js, etc.) without false positive overhead.
    """

    def __init__(self):
        # Base fallback vectors to guarantee operational pipeline continuity
        self.fallback_tags = ["cve", "rce", "lfi", "vuln", "misconfig"]

    # -------------------------------------------------------------------------
    # BRAIN 1: 100% DYNAMIC TECHNOLOGY SCORING ENGINE (NO MOCKS / NO FIXED LISTS)
    # -------------------------------------------------------------------------
    def _run_technology_engine(self, context: ScanContext) -> Dict[str, Any]:
        """
        Dynamically extracts software products and frameworks from the living memory graph.
        Converts live discovered tech strings into strict adaptive template constraints.
        """
        extracted_tech_tokens = set()

        # Gather real live signatures populated by asset fingerprinting plugins
        if context.asset.technologies:
            for tech in context.asset.technologies:
                # Clean strings to extract raw vendor tokens (e.g. 'Node.js', 'Docker', 'Windows')
                clean_tech = str(tech).lower().strip().split(":")[0]
                if clean_tech:
                    extracted_tech_tokens.add(clean_tech)

        # Gather real live services and application products discovered by Nmap
        if context.asset.open_ports:
            for port in context.asset.open_ports:
                service = port.get("service", "")
                product = port.get("product", "")
                if service:
                    extracted_tech_tokens.add(str(service).lower().strip())
                if product:
                    # Isolate primary product name before version indicators
                    clean_prod = str(product).lower().strip().split()[0] if str(product).strip() else ""
                    if clean_prod:
                        extracted_tech_tokens.add(clean_prod)

        # Build dynamic technology profiles mapping directly into Nuclei directory tracks
        dynamic_profile = {}
        for token in extracted_tech_tokens:
            if len(token) < 2:
                continue
            
            # Formulate dynamic execution parameters based strictly on what exists on the target
            dynamic_profile[token] = {
                "confidence": 100,
                "tag": token,
                # Direct folder projection: Maps 'tomcat' to 'http/vulnerabilities/tomcat', etc.
                "folder": f"http/vulnerabilities/{token}" if "http" in token or token not in ["smb", "ssh", "ftp", "rdp", "postgres", "mysql"] else f"network/vulnerabilities/{token}",
                "priority": 90  # Verified technology gets max execution preference
            }

        return dynamic_profile

    # -------------------------------------------------------------------------
    # BRAIN 2: SURFACE CLUSTERING ENGINE (COLLAPSES PARAMETER TRAILS)
    # -------------------------------------------------------------------------
    def _run_surface_engine(self, web_targets: List[str], vulnerable_urls: List[str]) -> List[str]:
        """
        Performs structural URL parameter clustering over high-volume entrypoints.
        Collapses thousands of redundant tracks into singular unique master targets.
        """
        raw_pool = set(web_targets if web_targets else [])
        if vulnerable_urls:
            for url in vulnerable_urls:
                if url and not any(ext in url.lower() for ext in [".png", ".jpg", ".jpeg", ".css", ".ico", ".svg", ".js", ".woff"]):
                    raw_pool.add(url)

        clustered_signatures = set()
        filtered_targets = []

        for url in raw_pool:
            if not url:
                continue
            parsed = urlparse(url)
            host = parsed.netloc if parsed.netloc else parsed.path
            
            # Extract dynamic query keys skeleton structures
            query_params = sorted(list(parse_qs(parsed.query).keys()))
            param_skeleton = ",".join(query_params) if query_params else "static-route"
            
            # Group numerical patterns together to abstract unique endpoints
            clean_path = re.sub(r'\d+', 'X', parsed.path)
            surface_signature = f"{host}::{clean_path}::{param_skeleton}"

            if surface_signature not in clustered_signatures:
                clustered_signatures.add(surface_signature)
                filtered_targets.append(url)

        return filtered_targets

    # -------------------------------------------------------------------------
    # BRAIN 3: RISK SCORING PRIORITY GRADIENT FILTER
    # -------------------------------------------------------------------------
    def _run_risk_engine(self, clustered_targets: List[str]) -> List[str]:
        """
        Grades structural routes and penalizes generic pathways (e.g. about, contact, faq)
        to prevent execution delays across non-vulnerable information pages.
        """
        high_risk_patterns = [r"dav", r"cgi", r"admin", r"config", r"login", r"sql", r"xml", r"php", r"api", r"v1", r"v2", r"rest"]
        low_risk_patterns = [r"about", r"credit", r"contact", r"faq", r"terms", r"license", r"legal", r"privacy"]

        prioritized_queue = []

        for url in clustered_targets:
            score = 50  # Operational baseline index
            url_lower = url.lower()

            if any(re.search(pat, url_lower) for pat in high_risk_patterns):
                score += 45
            if any(re.search(pat, url_lower) for pat in low_risk_patterns):
                score -= 40

            # Drop entries that do not present legitimate asset penetration parameters
            if score >= 25:
                prioritized_queue.append((url, score))

        # Re-order execution queue based on descending threat target weights
        prioritized_queue.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in prioritized_queue]

    # -------------------------------------------------------------------------
    # BRAIN 4: EXECUTION ENGINE ORCHESTRATOR (MAIN GATEWAY)
    # -------------------------------------------------------------------------
    def generate_attack_plan(self, context: ScanContext) -> Dict[str, Any]:
        """
        Orchestrates full contextual mapping sequences across live assets.
        Guarantees compatibility across Windows, Cloud, Docker, and customized endpoints
        by executing strictly on discovered asset ecosystem realities.
        """
        logger.info("Initiating dynamic universal planning sequence inside DecisionEngine...")

        # Step 1: Run Technology Engine to harvest 100% real live system signatures
        dynamic_profile = self._run_technology_engine(context)
        
        active_tags = set()
        active_folders = set()

        for tech_name, mapping in dynamic_profile.items():
            if mapping["confidence"] >= 70:
                active_tags.add(mapping["tag"])
                active_folders.add(mapping["folder"])

        # Step 2 & 3: Run target surface parameter clustering and risk triage filtering
        raw_web_targets = context.web_targets if context.web_targets else []
        raw_vuln_urls = context.vulnerable_urls if context.vulnerable_urls else []
        
        clustered_pool = self._run_surface_engine(raw_web_targets, raw_vuln_urls)
        optimized_targets_queue = self._run_risk_engine(clustered_pool)

        # Step 4: Secure emergency system fallbacks if no fingerprint tokens register
        if not active_tags:
            logger.warning("Target metrics isolated no structural vendors. Activating standard web profiles.")
            for fallback in self.fallback_tags:
                active_tags.add(fallback)
            active_folders.add("http/vulnerabilities")

        logger.info(f"Supersonic plan finalized | Targets consolidated from {len(raw_web_targets)} down to {len(optimized_targets_queue)}")
        logger.info(f"Dynamic targets mapped: Tags={list(active_tags)} | Target Paths={list(active_folders)}")

        return {
            "targets": optimized_targets_queue,
            "tags": list(active_tags),
            "folders": list(active_folders),
            "environment": "cloud" if "cloud" in str(active_tags) else "standard"
        }
