
import os
import importlib
from utils.config import load_config
from utils.progress import run_with_progress

# Dynamically load all modules in the 'modules' folder
def load_modules():
    modules = {}
    module_folder = os.path.join(os.path.dirname(__file__), "modules")
    for filename in os.listdir(module_folder):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module = importlib.import_module(f"modules.{module_name}")
            if hasattr(module, "generate_log"):
                modules[module_name] = module.generate_log
    return modules

def main():
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
