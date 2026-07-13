# modules/nmap/module.py

import logging
import subprocess
import shutil
import xml.etree.ElementTree as ET
from core.types import ScanContext, Finding, Severity

logger = logging.getLogger("FusionEngine.Modules.Nmap")

def run(context: ScanContext) -> None:
    """
    Executes a real native Nmap scan using subprocess, parses its XML output,
    and populates the global ScanContext with open ports and network findings.
    """
    logger.info(f"Initiating live network reconnaissance over: {context.target}")

    # Dynamic binary discovery to ensure multi-environment porting stability
    nmap_path = shutil.which("nmap")
    if not nmap_path:
        logger.error("Nmap binary not found in the system PATH. Verify installation.")
        raise FileNotFoundError("Critical dependency missing: nmap execution binary.")

    # Native optimized command line arguments:
    # -F (Fast top 100 ports scan), -sV (Service analysis), -oX - (Stream XML directly to stdout)
    command = [nmap_path, "-F", "-sV", "-oX", "-", context.target]
    
    try:
        logger.info(f"Running native command: {' '.join(command)}")
        process_result = subprocess.run(command, capture_output=True, text=True, check=True)
        xml_data = process_result.stdout
        
        if not xml_data.strip():
            logger.warning("Nmap executed successfully but returned an empty XML output stream.")
            return

        # Trigger dynamic XML digestion loop
        parse_nmap_xml(xml_data, context)

    except subprocess.CalledProcessError as e:
        logger.error(f"Nmap execution subprocess thread crashed: {e.stderr}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected processing breakdown inside Nmap module: {str(e)}")
        raise e

def parse_nmap_xml(xml_content: str, context: ScanContext) -> None:
    """
    Parses raw Nmap XML data, extracts open ports, and maps them to 
    standard Findings AND the new structural AssetHost blueprint.
    """
    import xml.etree.ElementTree as ET
    try:
        root = ET.fromstring(xml_content)
        discovered_ports = []

        for host in root.findall("host"):
            for port_element in host.findall(".//port"):
                state_element = port_element.find("state")
                
                if state_element is not None and state_element.attrib.get("state") == "open":
                    port_id = int(port_element.attrib["portid"])
                    discovered_ports.append(port_id)

                    service_element = port_element.find("service")
                    service_name = "unknown"
                    product_name = "unknown"
                    
                    if service_element is not None:
                        service_name = service_element.attrib.get("name", "unknown")
                        product_name = service_element.attrib.get("product", "unknown")

                    critical_infra_ports = {22, 21, 445, 3389, 8080}
                    severity = Severity.MEDIUM if port_id in critical_infra_ports else Severity.INFO

                    # 1. FEED THE ASSET DIRECTLY (Knowledge Model Building)
                    context.asset.open_ports.append({
                        "port": port_id,
                        "service": service_name,
                        "product": product_name,
                        "protocol": "tcp"
                    })

                    # 2. Generate finding evidence with context parameters
                    finding = Finding(
                        module="nmap",
                        finding_type="open_port",
                        title=f"Open Network Port Discovered: {port_id}/TCP",
                        severity=severity,
                        data={
                            "port": port_id,
                            "protocol": "tcp",
                            "service": service_name,
                            "product": product_name
                        },
                        description=f"Port {port_id} running service '{service_name}' ({product_name}) is exposed.",
                        remediation="Enforce strict firewall zoning policies. Close ports that are not business-critical.",
                        port=port_id
                    )
                    context.add_finding(finding)

        context.open_ports.extend(discovered_ports)
        logger.info(f"Nmap pipeline stage finalized | Asset open_ports populated: {len(context.asset.open_ports)}")

    except ET.ParseError as e:
        logger.error(f"Failed to parse Nmap XML structured stream: {str(e)}")
        raise e
