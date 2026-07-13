# database/storage.py

import sqlite3
import json
import logging
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger("FusionEngine.Database")

class LocalStorage:
    """
    Industrial SQLite persistence layer for Fusion-AI.
    Manages historical scan records with active automatic data rotation to safeguard disk storage.
    """

    def __init__(self, db_path: str = "database/fusion_records.db"):
        self.db_path = db_path
        # Strict restriction: Only keep the latest 30 scans in the free ledger to avoid disk saturation
        self.max_historical_records = 1
        self._initialize_database()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _initialize_database(self) -> None:
        """Creates target storage schema architecture if non-existent."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS scans (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        target TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        total_findings INTEGER NOT NULL,
                        risk_score INTEGER NOT NULL,
                        verdict TEXT NOT NULL,
                        raw_json_payload TEXT NOT NULL
                    )
                """)
                conn.commit()
                logger.info(f"Database core storage synchronized successfully at: '{self.db_path}'")
        except Exception as e:
            logger.critical(f"Fatal disruption inside database initialization: {str(e)}")

    def save_scan_report(self, scan_report: Dict[str, Any]) -> int:
        """
        Serializes and commits the JSON report mapping to SQLite history,
        and automatically triggers the data rotation cleanup loop.
        """
        target = scan_report.get("target", "unknown")
        total_findings = scan_report.get("total_findings", 0)
        
        risk_intel = scan_report.get("risk_intelligence", {})
        risk_score = risk_intel.get("risk_score", 0)
        verdict = risk_intel.get("verdict", "UNKNOWN")
        
        timestamp = datetime.utcnow().isoformat()
        serialized_payload = json.dumps(scan_report, ensure_ascii=False)

        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO scans (target, timestamp, total_findings, risk_score, verdict, raw_json_payload)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (target, timestamp, total_findings, risk_score, verdict, serialized_payload))
                conn.commit()
                inserted_id = cursor.lastrowid
                
                # TRIGGER DATA ROTATION CLEANUP ENGINE
                self._enforce_data_rotation(cursor)
                conn.commit()
                
                return inserted_id
        except Exception as e:
            logger.error(f"Failed to persist scan payload into the local DB cache: {str(e)}")
            return -1

    def _enforce_data_rotation(self, cursor: sqlite3.Cursor) -> None:
        """
        NASA-Style Storage Safeguard.
        Counts rows and purges the oldest chronological records if threshold boundaries are breached.
        """
        try:
            cursor.execute("SELECT COUNT(*) FROM scans")
            current_records_count = cursor.fetchone()[0]

            if current_records_count > self.max_historical_records:
                records_to_delete = current_records_count - self.max_historical_records
                logger.warning(f"Database retention boundary limit reached ({current_records_count}/{self.max_historical_records}). Initiating automated data rotation...")
                
                # Fetch the IDs of the oldest records to clear space
                cursor.execute("SELECT id FROM scans ORDER BY timestamp ASC LIMIT ?", (records_to_delete,))
                old_ids = [row[0] for row in cursor.fetchall()]
                
                if old_ids:
                    # Execute atomic deletion query
                    cursor.execute(f"DELETE FROM scans WHERE id IN ({','.join(['?']*len(old_ids))})", old_ids)
                    logger.info(f"Storage cleanup complete. Successfully purged {len(old_ids)} obsolete legacy scan payloads.")
                    
        except Exception as e:
            logger.error(f"Error executing data rotation storage sweep loop: {str(e)}")
