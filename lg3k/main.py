"""Main module for log generation.

This module provides the core functionality for loading and executing log generation modules.
It handles dynamic module loading, configuration management, and the main execution flow.
"""

import concurrent.futures
import importlib
import json
import os
import shutil
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, Optional

import click

# Try to import Rich, but don't fail if it's not available
try:
    from rich.console import Console
    from rich.table import Table

    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None
    print("Rich library not available. Install 'rich' package for enhanced output.")

from .utils.config import get_default_config, load_config

# Global lock for progress updates
progress_lock = threading.Lock()
# Global progress state
module_progress = {}
# Track module status
module_status = {}
# Track module order
module_order = []
# Global state for exit handling
exit_event = threading.Event()
current_run_files = []


def get_terminal_width() -> int:
    """Get the terminal width, defaulting to 80 if not available."""
    try:
        return shutil.get_terminal_size().columns
    except (AttributeError, ValueError):
        return 80


def show_rich_help(ctx):
    """Display help using Rich formatting."""
    if not RICH_AVAILABLE:
        print("Rich library not available. Install 'rich' package for enhanced output.")
        click.echo(ctx.get_help())
        return

    if console is None:
        print("Rich library not available. Install 'rich' package for enhanced output.")
        click.echo(ctx.get_help())
        return

    console.print("\nLog Generator 3000\n")

    # Quick start examples
    console.print("Quick Start:")
    console.print("  lg3k --generate-config config.json  # Create config")
    console.print("  lg3k                                # Generate logs")
    console.print("  lg3k -c 1000 -t 4                   # Custom generation\n")

    # Show modules in columns
    console.print("Modules:")
    console.print("  api      - API endpoints    network - Traffic logs")
    console.print("  database - DB operations    os      - System logs")
    console.print("  firewall - Security logs    printer - Print jobs")
    console.print("  nas      - Storage logs     web     - HTTP access\n")

    # Show command table
    if Table is not None:
        table = Table(
            show_header=True,
            header_style="bold white",
            border_style="dim",
            padding=(0, 1),
        )
        table.add_column("Option", style="yellow", no_wrap=True)
        table.add_column("Description", style="bright_blue")

        table.add_row("--generate-config PATH", "Create config file")
        table.add_row("-c, --count N", "Logs per module (max: 1,000,000)")
        table.add_row("-t, --threads N", "Thread count (default: CPU count)")
        table.add_row("-f, --config PATH", "Config file path")
        table.add_row("-o, --output-dir PATH", "Output directory")

        console.print(table)
    else:
        # Fallback to plain text table
        console.print("\nOptions:")
        console.print("  --generate-config PATH  Create config file")
        console.print("  -c, --count N          Logs per module (max: 1,000,000)")
        console.print("  -t, --threads N        Thread count (default: CPU count)")
        console.print("  -f, --config PATH      Config file path")
        console.print("  -o, --output-dir PATH  Output directory")


def load_modules() -> Dict[str, callable]:
    """Load all log generation modules."""
    modules = {}
    module_dir = os.path.join(os.path.dirname(__file__), "modules")

    for file in os.listdir(module_dir):
        if file.endswith(".py") and not file.startswith("__"):
            module_name = file[:-3]
            try:
                module = importlib.import_module(
                    f".modules.{module_name}", package="lg3k"
                )
                if hasattr(module, "generate_log"):
                    modules[module_name] = module.generate_log
            except ImportError as e:
                if RICH_AVAILABLE:
                    console.print(
                        f"[yellow]Warning: Failed to load module {module_name}: {e}[/yellow]"
                    )
                else:
                    print(f"Warning: Failed to load module {module_name}: {e}")

    return modules


def format_progress_display() -> str:
    """Format progress display with each module on its own line."""
    lines = []
    # Use module_order instead of sorting by name
    for name in module_order:
        status = module_status.get(name, "Waiting")
        # Add hash to module name for Docker-like display
        module_id = f"{hash(name) & 0xFFFFFFFF:08x}"
        if status == "Running":
            progress = module_progress[name]
            lines.append(f"{module_id}: {name:<12} {progress}")
        elif status == "Complete":
            lines.append(f"{module_id}: {name:<12} Complete")
        else:
            lines.append(f"{module_id}: {name:<12} {status}")
    return "\n".join(lines)


def update_progress_display():
    """Update the progress display."""
    # Move cursor up by number of modules
    module_count = len(module_progress)
    if module_count > 0:
        # Clear previous display
        print(f"\033[{module_count}A\033[J", end="", flush=True)
        # Print new display
        print(format_progress_display(), flush=True)


def cleanup_files(keep_files: bool = False):
    """Clean up generated files from the current run.

    Args:
        keep_files: If True, keep the partially generated files
    """
    if not keep_files:
        for file_path in current_run_files:
            try:
                Path(file_path).unlink()
            except OSError:
                pass  # Ignore errors during cleanup


def generate_analysis(name: str, log_entry: Dict) -> str:
    """Generate analysis for a log entry based on its type and content.

    Args:
        name: Module name
        log_entry: The log entry to analyze

    Returns:
        str: Analysis of the log entry
    """
    # Extract key information
    level = log_entry.get("level", "INFO")
    message = log_entry.get("message", "")
    timestamp = log_entry.get("timestamp", "")

    # Base analysis
    analysis = []

    # Add timestamp analysis
    if timestamp:
        analysis.append(f"Log generated at {timestamp}.")

    # Add severity analysis
    if level in ["ERROR", "CRITICAL"]:
        analysis.append(
            f"This is a {level.lower()} level event that requires immediate attention."
        )
    elif level == "WARNING":
        analysis.append("This is a warning that may require investigation.")

    # Module-specific analysis
    if name == "api":
        if "status" in log_entry:
            status = log_entry["status"]
            if status >= 500:
                analysis.append("Server-side error detected in API response.")
            elif status >= 400:
                analysis.append("Client-side error detected in API request.")
            elif status >= 300:
                analysis.append("API request resulted in a redirection.")
            elif status >= 200:
                analysis.append("API request completed successfully.")

    elif name == "database":
        if "query" in log_entry:
            analysis.append("Database query execution logged.")
            if "duration" in log_entry:
                duration = log_entry["duration"]
                if duration > 1000:
                    analysis.append("Query execution time is unusually high.")

    elif name == "web_server":
        if "method" in log_entry:
            analysis.append(f"Web server processed a {log_entry['method']} request.")
            if "path" in log_entry:
                analysis.append(f"Accessed path: {log_entry['path']}")

    # Add message analysis
    if message:
        analysis.append(f"Message details: {message}")

    # Combine analysis points
    return " ".join(analysis)


def generate_module_logs(
    name: str,
    func: Callable,
    count: int,
    output_path: Path,
    json_output: bool = False,
    llm_format: bool = False,
) -> None:
    """Generate logs for a specific module.

    Args:
        name: Module name
        func: Module function to generate logs
        count: Number of logs to generate
        output_path: Output directory path
        json_output: Whether to output JSON
        llm_format: Whether to format logs for LLM training
    """
    try:
        # Create output file
        output_file = output_path / f"{name}.jsonl"
        current_run_files.add(str(output_file))

        with open(output_file, "w") as f:
            for _ in range(count):
                if exit_event.is_set():
                    break

                # Generate log entry
                log_entry = func()

                if llm_format:
                    # Format for LLM training
                    training_entry = {
                        "instruction": f"Analyze this {name} log entry and identify any anomalies, patterns, or important information",
                        "input": log_entry,
                        "output": generate_analysis(name, log_entry),
                    }
                    json.dump(training_entry, f)
                else:
                    # Standard log format
                    json.dump(log_entry, f)
                f.write("\n")

        if not json_output and not exit_event.is_set():
            print(f"Generated {count} logs for {name}")

    except Exception as e:
        if not json_output:
            print(f"Error generating logs for {name}: {str(e)}")
        raise


def output_json(result: dict) -> None:
    """Output a single line of JSON with generation results.

    Args:
        result: Dictionary containing the result data
    """
    # Add timing information if not present
    if "success" in result and result["success"]:
        result.setdefault("time_taken", 0.0)
        result.setdefault(
            "stats",
            {
                "total_files": len(result.get("files", [])),
                "avg_logs_per_file": result.get("logs_generated", 0)
                / len(result.get("files", []))
                if result.get("files")
                else 0,
                "total_size_bytes": sum(
                    Path(f).stat().st_size for f in result.get("files", [])
                ),
            },
        )
        result.setdefault(
            "timing",
            {
                "start_time": datetime.now().isoformat(),
                "duration_seconds": result.get("time_taken", 0.0),
                "logs_per_second": result.get("logs_generated", 0)
                / result.get("time_taken", 1.0)
                if result.get("time_taken", 0.0) > 0
                else 0,
            },
        )
        result.setdefault(
            "config",
            {
                "output_directory": str(Path(result.get("files", [""])[0]).parent)
                if result.get("files")
                else None,
                "file_format": Path(result.get("files", [""])[0]).suffix[1:]
                if result.get("files")
                else None,
            },
        )
    elif "error" in result:
        if isinstance(result["error"], str):
            result["error"] = {"message": result["error"], "type": "str"}
        result.setdefault("logs_generated", 0)
        result.setdefault("time_taken", 0.0)
        result.setdefault("files", [])
        result.setdefault(
            "stats", {"total_files": 0, "avg_logs_per_file": 0, "total_size_bytes": 0}
        )
        result.setdefault("config", {"output_directory": None, "file_format": None})

    click.echo(json.dumps(result), nl=False)


@click.command()
@click.version_option(version="0.6.5", prog_name="Log Generator 3000")
@click.option(
    "--generate-config",
    type=click.Path(dir_okay=False),
    help="Generate a full-featured configuration file",
)
@click.option(
    "-c",
    "--count",
    type=click.IntRange(1, 1_000_000),
    help="Number of log entries per module (default: 100, max: 1,000,000)",
)
@click.option(
    "-t",
    "--threads",
    type=click.IntRange(1, None),
    help="Number of threads to use (default: system CPU count)",
)
@click.option(
    "-f",
    "--config",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to config file (default: config.json)",
)
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(file_okay=False),
    default="logs",
    help="Output directory for log files (default: logs/)",
)
@click.option(
    "--json-output",
    is_flag=True,
    help="Output a single line of JSON with generation results",
)
@click.option(
    "--llm-format",
    is_flag=True,
    help="Generate logs in LLM training format (instruction, input, output). Overrides other options for optimal training.",
)
@click.pass_context
def cli(
    ctx,
    generate_config: Optional[str],
    count: Optional[int],
    threads: Optional[int],
    config: Optional[str],
    output_dir: str,
    json_output: bool,
    llm_format: bool,
):
    """Multi-threaded log generator for testing and development.

    Start with: lg3k --generate-config config.json
    Press Ctrl+C to exit gracefully.
    """
    # Show help if no arguments or help requested
    if "--help" in sys.argv or len(sys.argv) == 1:
        show_rich_help(ctx)
        ctx.exit(0)

    try:
        if generate_config:
            if os.path.exists(generate_config):
                if not json_output:
                    print(f"Warning: {generate_config} already exists. Skipping.")
                else:
                    output_json(
                        {
                            "success": False,
                            "error": {
                                "message": f"Configuration file already exists: {generate_config}",
                                "type": "FileExistsError",
                            },
                        }
                    )
                ctx.exit(1)

            with open(generate_config, "w") as f:
                json.dump(get_default_config(), f, indent=2)
            if not json_output:
                print(f"Configuration file generated: {generate_config}")
            else:
                output_json({"success": True, "config_file": generate_config})
            ctx.exit(0)

        # If --llm-format is used, override other options for optimal training data
        if llm_format:
            if config or count or threads:
                if not json_output:
                    print(
                        "Warning: --llm-format overrides -c, -t, and -f options for optimal training data generation"
                    )

            # Calculate optimal batch size based on available memory
            try:
                import psutil
                import torch

                available_memory = psutil.virtual_memory().available
                if torch.cuda.is_available():
                    gpu_memory = torch.cuda.get_device_properties(0).total_memory
                    # Use 80% of GPU memory for safety
                    max_batch_size = min(
                        int((gpu_memory * 0.8) / (2 * 1024 * 1024)), 128
                    )  # 2MB per sample estimate
                else:
                    # Use 40% of system memory for CPU training
                    max_batch_size = min(
                        int((available_memory * 0.4) / (2 * 1024 * 1024)), 64
                    )  # More conservative for CPU
            except (ImportError, RuntimeError):
                # Fallback to conservative defaults if can't detect
                max_batch_size = 32

            # Calculate optimal number of threads based on CPU cores and memory
            optimal_threads = min(
                os.cpu_count() or 1,
                max(1, int(available_memory / (1024 * 1024 * 1024))),
            )  # 1 thread per GB

            config_data = {
                "services": ["api", "database", "web_server"],  # Focus on web stack
                "count": max_batch_size
                * 100,  # Generate enough samples for multiple epochs
                "threads": optimal_threads,
                "llm_format": True,
                "training": {
                    "batch_size": max_batch_size,
                    "sequence_length": 512,  # Standard for instruction tuning
                    "epochs": 10,  # Default number of epochs
                    "validation_split": 0.1,  # Hold out 10% for validation
                    "warmup_steps": max(
                        100, int(max_batch_size * 0.1)
                    ),  # Dynamic warmup
                    "save_steps": max(
                        50, int(max_batch_size * 0.05)
                    ),  # Checkpoint frequency
                    "eval_steps": max(
                        25, int(max_batch_size * 0.025)
                    ),  # Evaluation frequency
                },
            }

            if not json_output:
                print("Optimized training configuration:")
                print(
                    f"- Batch size: {max_batch_size} (based on available {'GPU' if torch.cuda.is_available() else 'CPU'} memory)"
                )
                print(f"- Threads: {optimal_threads} (based on CPU cores and memory)")
                print(f"- Samples per service: {config_data['count']}")
                print(
                    f"- Total samples: {config_data['count'] * len(config_data['services'])}"
                )
                print("Generating training data...")
        else:
            # Load configuration
            config_file = config or "config.json"
            config_data = {}
            if os.path.exists(config_file):
                try:
                    config_data = load_config(config_file)
                except Exception as e:
                    if not json_output:
                        print(f"Error loading configuration: {str(e)}")
                    else:
                        output_json(
                            {
                                "success": False,
                                "error": {"message": str(e), "type": type(e).__name__},
                            }
                        )
                    ctx.exit(1)
            elif not count:  # Only require config if count is not provided
                if not json_output:
                    print(f"Configuration file not found: {config_file}")
                    print("Run with --generate-config to create one.")
                else:
                    output_json(
                        {
                            "success": False,
                            "error": {
                                "message": f"Configuration file not found: {config_file}",
                                "type": "FileNotFoundError",
                            },
                        }
                    )
                ctx.exit(1)

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Load modules
        active_modules = load_modules()
        if not active_modules:
            if not json_output:
                print("Error: No modules found. Please check your installation.")
            else:
                output_json(
                    {
                        "success": False,
                        "error": {
                            "message": "No modules found. Please check your installation.",
                            "type": "ModuleNotFoundError",
                        },
                    }
                )
            ctx.exit(1)

        # Filter active modules based on config
        if config_data and "services" in config_data:
            active_modules = {
                k: v for k, v in active_modules.items() if k in config_data["services"]
            }
            if not active_modules:
                if not json_output:
                    print("No active services found in configuration.")
                else:
                    output_json(
                        {
                            "success": False,
                            "error": {
                                "message": "No active services found in configuration",
                                "type": "ValueError",
                            },
                        }
                    )
                ctx.exit(1)

        # Set up generation parameters
        log_count = count or config_data.get("count", 100)
        thread_count = threads or config_data.get("threads", os.cpu_count() or 1)

        # Track timing
        start_time = datetime.now()

        try:
            # Clear any previous run files
            current_run_files.clear()

            if thread_count == 1:
                for name, func in active_modules.items():
                    if exit_event.is_set():
                        break
                    generate_module_logs(
                        name, func, log_count, output_path, json_output, llm_format
                    )
            else:
                # Use thread pool for parallel processing
                with concurrent.futures.ThreadPoolExecutor(
                    max_workers=thread_count
                ) as executor:
                    futures = [
                        executor.submit(
                            generate_module_logs,
                            name,
                            func,
                            log_count,
                            output_path,
                            json_output,
                            llm_format,
                        )
                        for name, func in active_modules.items()
                    ]
                    concurrent.futures.wait(futures)

            time_taken = (datetime.now() - start_time).total_seconds()

            if json_output:
                output_json(
                    {
                        "success": True,
                        "logs_generated": log_count * len(active_modules),
                        "time_taken": time_taken,
                        "files": current_run_files,
                        "config": {
                            **config_data,
                            "output_directory": str(output_path),
                            "llm_format": llm_format,
                        },
                    }
                )
            elif llm_format:
                print(
                    f"\nGenerated {log_count * len(active_modules)} logs optimized for LLM training"
                )
                print(f"Output directory: {output_path}")
                print("\nNext steps:")
                print(
                    "1. Use these logs for training: ollama train llama3.2:1b-instruct-fp16 --training-data logs/*.jsonl"
                )
                print("2. Or run the automated training loop from the guide")
            ctx.exit(0)

        except KeyboardInterrupt:
            exit_event.set()
            if json_output:
                output_json(
                    {
                        "success": False,
                        "error": {
                            "message": "Generation cancelled",
                            "type": "KeyboardInterrupt",
                        },
                        "logs_generated": 0,
                        "time_taken": (datetime.now() - start_time).total_seconds(),
                        "files": current_run_files,
                    }
                )
            else:
                print("\nOperation cancelled by user.")
            cleanup_files()
            ctx.exit(1)

    except Exception as e:
        if json_output:
            output_json(
                {
                    "success": False,
                    "error": {"message": str(e), "type": type(e).__name__},
                    "logs_generated": 0,
                    "time_taken": 0.0,
                    "files": current_run_files,
                }
            )
        else:
            print(f"Error: {str(e)}")
        cleanup_files()
        ctx.exit(1)


def main():
    """CLI entry point."""
    cli()
