# core/plugin_loader.py

import os
import sys
import importlib
import logging
from typing import Any
from pathlib import Path

logger = logging.getLogger("FusionEngine.PluginLoader")


class PluginLoader:
    """
    Automated plugin discovery engine for Fusion-AI.
    Dynamically loads modules and registers them into the engine.
    """

    def __init__(self, modules_dir: str = "modules"):
        self.modules_dir = modules_dir

        # Ensure project root is in Python path
        base_path = Path(__file__).resolve().parent.parent
        sys.path.append(str(base_path))

    def load_plugins(self, engine: Any) -> None:
        """
        Scans modules directory and registers valid plugins.
        """

        if not os.path.exists(self.modules_dir):
            logger.error(f"Modules directory not found: {self.modules_dir}")
            return

        logger.info(f"Starting plugin discovery in: {self.modules_dir}")

        loaded_count = 0
        skipped_count = 0

        for folder_name in os.listdir(self.modules_dir):
            folder_path = os.path.join(self.modules_dir, folder_name)

            # Skip invalid entries
            if (
                folder_name.startswith("__")
                or folder_name.startswith(".")
                or not os.path.isdir(folder_path)
            ):
                continue

            module_file = os.path.join(folder_path, "module.py")

            if not os.path.exists(module_file):
                logger.debug(f"Skipping {folder_name}: no module.py found")
                skipped_count += 1
                continue

            # Avoid duplicate registration
            if folder_name in engine.modules:
                logger.debug(f"Module already loaded: {folder_name}")
                continue

            import_path = f"{self.modules_dir}.{folder_name}.module"

            try:
                loaded_module = importlib.import_module(import_path)

                # Validate interface
                if not hasattr(loaded_module, "run"):
                    logger.error(
                        f"Invalid plugin interface: {import_path} missing run(context)"
                    )
                    continue

                engine.register_module(folder_name, loaded_module)

                logger.info(f"Plugin loaded successfully: {folder_name}")

                loaded_count += 1

            except Exception as e:
                logger.error(
                    f"Failed to load plugin {import_path}: {str(e)}"
                )

        logger.info(
            f"Plugin loading completed | Loaded: {loaded_count} | Skipped: {skipped_count}"
        )
