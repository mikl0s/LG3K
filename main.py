"""Main entry point for the Log Generator 3000 (LG3K).

This module handles the initialization and execution of the log generation process,
including configuration loading and module management.
"""

import importlib
import os
import random

from utils.config import load_config
from utils.progress import run_with_progress
from utils.timestamp import generate_timestamp


# Dynamically load all modules in the 'modules' folder
def load_modules():
    """Load all modules from the 'modules' folder.

    Returns:
        dict: A dictionary containing module names as keys and their generate_log functions as values.
    """
    modules = {}
    module_folder = os.path.join(os.path.dirname(__file__), "modules")
    for filename in os.listdir(module_folder):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module = importlib.import_module(f"modules.{module_name}")
            if hasattr(module, "generate_log"):
                modules[module_name] = module.generate_log
    return modules


def generate_log():
    """Generate a single log entry with random severity level.

    Returns:
        dict: A log entry containing timestamp, level, component, and message.
    """
    timestamp = generate_timestamp()
    level = random.choice(["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"])
    return {
        "timestamp": timestamp,
        "level": level,
        "component": "Main",
        "message": "Log entry generated.",
    }


def main():
    """Execute the main log generation process.

    This function initializes the configuration, loads the appropriate modules,
    and coordinates the log generation process.
    """
    # Load configuration
    config = load_config("config.json")

    # Load all modules
    modules = load_modules()

    # Select active services from config
    active_services = config.get("services", [])
    active_modules = {k: v for k, v in modules.items() if k in active_services}

    if not active_modules:
        print("No active modules found. Check your configuration.")
        return

    # Generate logs for active modules
    run_with_progress(active_modules, config)


if __name__ == "__main__":
    main()
