"""
Fusion-AI // Executive Attack Replay
Live chronological event aggregator.

The replay layer does not perform scanning.
It consumes findings already produced by Fusion-AI modules.
"""

import os
import json
import hashlib
import logging
from datetime import datetime

logger = logging.getLogger("FusionEngine.Modules.AttackReplay")


HISTORY_PATHS = [
    "outputs/json/fusion_history.json",
    "outputs/fusion_history.json",
]

REPORT_PATHS = [
    "outputs/json/report.json",
    "outputs/report.json",
]


PHASE_MAP = {
    "nmap": 1,
    "iot_scan": 1,

    "httpx": 2,
    "whatweb": 2,

    "katana": 3,

    "gobuster": 4,
    "ffuf": 4,

    "nuclei": 5,
    "searchsploit": 5,

    "attack_story": 6,
}


PHASE_NAMES = {
    1: "RECONNAISSANCE",
    2: "SERVICE VALIDATION",
    3: "APPLICATION MAPPING",
    4: "RESOURCE ENUMERATION",
    5: "VULNERABILITY ANALYSIS",
    6: "CORRELATION",
}


def _find_history():
    for path in HISTORY_PATHS:
        if os.path.exists(path):
            return path
    return None


def _find_report():
    for path in REPORT_PATHS:
        if os.path.exists(path):
            return path
    return None


def _load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        logger.error("Unable to read %s: %s", path, exc)
        return None


def _event_id(event):
    raw = "|".join([
        str(event.get("timestamp", "")),
        str(event.get("module", "")),
        str(event.get("title", "")),
        str(event.get("target", "")),
        str(event.get("description", "")),
    ])

    return hashlib.sha1(
        raw.encode("utf-8")
    ).hexdigest()


def _phase_for_module(module):
    return PHASE_MAP.get(
        str(module).lower(),
        6
    )


def _severity(event):
    severity = str(
        event.get("severity", "info")
    ).lower()

    if severity not in {
        "info",
        "low",
        "medium",
        "high",
        "critical",
    }:
        return "info"

    return severity


def _build_event(raw):
    module = str(
        raw.get("module", "unknown")
    ).lower()

    phase = _phase_for_module(module)

    title = (
        raw.get("title")
        or raw.get("name")
        or raw.get("finding")
        or raw.get("description")
        or "Security event"
    )

    description = str(
        raw.get("description", "")
    )

    timestamp = (
        raw.get("timestamp")
        or raw.get("time")
        or raw.get("created_at")
        or datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    event = {
        "id": None,
        "timestamp": timestamp,
        "phase": phase,
        "phase_name": PHASE_NAMES[phase],
        "module": module.upper(),
        "severity": _severity(raw),
        "title": str(title),
        "summary": description,
        "target": raw.get("target"),
        "port": raw.get("port"),
        "evidence": raw.get("evidence"),
        "status": raw.get("status", "detected"),
    }

    event["id"] = _event_id(event)

    return event


def _extract_events(history):
    """
    Supports either:

        [
            {...},
            {...}
        ]

    or:

        {
            "events": [...]
        }

    or:

        {
            "history": [...]
        }
    """

    if isinstance(history, list):
        return history

    if not isinstance(history, dict):
        return []

    for key in (
        "events",
        "history",
        "findings",
        "timeline",
    ):
        value = history.get(key)

        if isinstance(value, list):
            return value

    return []


def build_attack_replay(context=None):

    history_path = _find_history()

    if not history_path:
        logger.debug(
            "fusion_history.json not available yet"
        )
        return

    history = _load_json(history_path)

    if history is None:
        return

    raw_events = _extract_events(history)

    events = []

    for raw in raw_events:

        if not isinstance(raw, dict):
            continue

        events.append(
            _build_event(raw)
        )

    # Chronological order.
    events.sort(
        key=lambda item: item["timestamp"]
    )

    # Remove duplicates.
    unique = {}
    for event in events:
        unique[event["id"]] = event

    events = list(unique.values())

    report_path = _find_report()

    if not report_path:
        return

    report = _load_json(report_path)

    if not isinstance(report, dict):
        return

    report["attack_replay"] = {
        "status": "LIVE",
        "generated_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "source": "fusion_history.json",
        "total_events": len(events),
        "events": events,
    }

    report["attack_story_phases"] = [
        {
            "phase": phase,
            "title": PHASE_NAMES[phase],
            "events": [
                event
                for event in events
                if event["phase"] == phase
            ],
        }
        for phase in sorted(PHASE_NAMES)
        if any(
            event["phase"] == phase
            for event in events
        )
    ]

    try:
        with open(
            report_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                report,
                f,
                indent=4,
                ensure_ascii=False
            )

    except Exception as exc:
        logger.error(
            "Unable to write replay: %s",
            exc
        )

    print(
        " 🎬 [FUSION-AI] -> "
        f"LIVE REPLAY UPDATED "
        f"({len(events)} events)"
    )
