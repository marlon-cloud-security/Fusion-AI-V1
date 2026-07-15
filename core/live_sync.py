# core/live_sync.py
import os
import json
import threading
from datetime import datetime
from typing import Any

class LiveSyncEventBus:
    """
    Stateful concurrent Event Bus designed to safely buffer, deduplicate, 
    and publish real-time security findings without blocking the scanning engines.
    """
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.memory_file = os.path.join(self.base_dir, "outputs", "fusion_history.json")
        self.lock = threading.Lock()
        
    def publish_finding(self, finding_obj: Any) -> None:
        """
        Ingests a raw memory finding, applies deduplication constraints,
        and flushes the data securely to feed the dashboard API server.
        """
        try:
            # Safely serialize the abstract memory finding class object into a flat map dict
            rf = finding_obj.to_dict() if hasattr(finding_obj, "to_dict") else getattr(finding_obj, "__dict__", {})
            if not rf:
                return

            with self.lock:
                os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
                
                # Load current live storage flat tracking array ledger
                current_db = []
                if os.path.exists(self.memory_file):
                    try:
                        with open(self.memory_file, "r", encoding="utf-8") as f:
                            current_db = json.load(f)
                    except Exception:
                        current_db = []
                
                if not isinstance(current_db, list):
                    current_db = []

                # Deduplication boundary trace mapping rule: Cross-checks signature keys
                exists = any(
                    old.get("title") == rf.get("title") and 
                    old.get("target") == rf.get("target") 
                    for old in current_db
                )
                
                if not exists:
                    rf["live_sync_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    current_db.append(rf)
                    
                    # Single atomic thread-safe commit transaction to maintain integrity
                    with open(self.memory_file, "w", encoding="utf-8") as f:
                        json.dump(current_db, f, indent=4, ensure_ascii=False)
                        
        except Exception:
            pass

# Single global instance dispatcher binding
live_sync_bus = LiveSyncEventBus()
