"""Main module for log generation.

This module provides the core functionality for loading and executing log generation modules.
It handles dynamic module loading, configuration management, and the main execution flow.

Functions:
    load_modules: Load all available log generation modules.
    generate_log: Generate a random log entry from available modules.
    main: Execute the main log generation process.
"""

import importlib
import os
import random
import sys
from typing import Dict

from rich.console import Console

from .utils.config import load_config
from .utils.progress import update_progress

console = Console()


def load_modules() -> Dict[str, callable]:
    """Load all log generation modules."""
    modules = {}
    module_dir = os.path.join(os.path.dirname(__file__), "modules")
    sys.path.insert(0, module_dir)

    for file in os.listdir(module_dir):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = file[:-3]
            module = importlib.import_module(f".modules.{module_name}", package="lg3k")
            if hasattr(module, "generate_log"):
                modules[module_name] = module.generate_log

    return modules


def generate_log() -> str:
    """Generate a random log entry."""
    modules = load_modules()
    if not modules:
        raise RuntimeError("No log generation modules found")

    module_name = random.choice(list(modules.keys()))
    return modules[module_name]()


def main():
    """Execute the main log generation process."""
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
    update_progress(active_modules, config)


if __name__ == "__main__":  # pragma: no cover
    main()
