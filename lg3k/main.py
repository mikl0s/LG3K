"""Main module for log generation.

This module provides the core functionality for loading and executing log generation modules.
It handles dynamic module loading, configuration management, and the main execution flow.
"""

import concurrent.futures
import importlib
import json
import multiprocessing
import os
import shutil
import sys
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

import click

# Try to import Rich, but don't fail if it's not available
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Note: Install 'rich' package for enhanced display: pip install rich")
    Console = None
    Panel = None

from .utils.config import get_default_config, load_config
from .utils.progress import update_progress

console = Console() if RICH_AVAILABLE else None

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


def generate_module_logs(
    module_name: str,
    generator_func: callable,
    count: int,
    output_dir: Path,
    json_output: bool = False,
) -> None:
    """Generate logs for a specific module and write them to a file.

    Args:
        module_name: Name of the module generating logs
        generator_func: Function that generates individual log entries
        count: Number of log entries to generate
        output_dir: Directory to write log files to
        json_output: Whether to suppress progress output for JSON mode
    """
    output_file = (
        output_dir / f"{module_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )
    current_run_files.append(output_file)

    with progress_lock:
        module_status[module_name] = "Running"
        module_progress[module_name] = "0.0%"
        if not json_output:
            update_progress_display()

    try:
        with open(output_file, "w") as f:
            for i in range(count):
                if exit_event.is_set():
                    with progress_lock:
                        module_status[module_name] = "Cancelled"
                        if not json_output:
                            update_progress_display()
                    return

                log_entry = generator_func()
                f.write(f"{log_entry}\n")
                if (i + 1) % 100 == 0:
                    progress = update_progress(i + 1, count)
                    with progress_lock:
                        module_progress[module_name] = progress
                        if not json_output:
                            update_progress_display()

            # Update final progress
            with progress_lock:
                module_progress[module_name] = "100.0%"
                module_status[module_name] = "Complete"
                if not json_output:
                    update_progress_display()
    except Exception as e:
        with progress_lock:
            module_status[module_name] = f"Error: {str(e)}"
            if not json_output:
                update_progress_display()
        raise


def output_json(
    success: bool,
    logs_generated: int,
    time_taken: float,
    files: list,
    error: Optional[str] = None,
) -> None:
    """Output results in JSON format.

    Args:
        success: Whether the operation was successful
        logs_generated: Number of logs generated
        time_taken: Time taken in seconds
        files: List of generated file paths
        error: Optional error message
    """
    result = {
        "success": success,
        "logs_generated": logs_generated,
        "time_taken": round(time_taken, 2),
        "files": files,
        "stats": {
            "total_files": len(files),
            "avg_logs_per_file": logs_generated / len(files) if files else 0,
            "total_size_bytes": sum(Path(f).stat().st_size for f in files)
            if files
            else 0,
        },
        "timing": {
            "start_time": datetime.now().isoformat(),
            "duration_seconds": round(time_taken, 2),
            "logs_per_second": round(logs_generated / time_taken, 2)
            if time_taken > 0
            else 0,
        },
        "config": {
            "output_directory": str(Path(files[0]).parent) if files else None,
            "file_format": Path(files[0]).suffix if files else None,
        },
    }
    if error:
        result["error"] = {
            "message": str(error),
            "type": error.__class__.__name__ if isinstance(error, Exception) else "str",
        }
    print(json.dumps(result), end="", file=sys.stdout, flush=True)


@click.command()
@click.version_option(version="0.6.5", prog_name="Log Generator 3000")
@click.option(
    "--generate-config",
    type=click.Path(),
    help="Generate a full-featured configuration file",
)
@click.option(
    "--count",
    "-c",
    default=None,
    type=int,
    help="Number of log entries per module (default: 100, max: 1,000,000)",
)
@click.option(
    "--threads",
    "-t",
    default=None,
    type=int,
    help="Number of threads to use (default: system CPU count)",
)
@click.option(
    "--config",
    "-f",
    default=None,
    type=click.Path(exists=True),
    help="Path to config file (default: config.json)",
)
@click.option(
    "--output-dir",
    "-o",
    default="logs",
    type=click.Path(),
    help="Output directory for log files (default: logs/)",
)
@click.option(
    "--json-output",
    is_flag=True,
    help="Output a single line of JSON with generation results",
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
):
    """Multi-threaded log generator for testing and development.

    Start with: lg3k --generate-config config.json
    Press Ctrl+C to exit gracefully.
    """
    if not any(
        [generate_config, count, threads, config, output_dir != "logs", json_output]
    ):
        show_rich_help(ctx)
        return

    try:
        # Track timing for JSON output
        start_time = datetime.now()
        generated_files = []
        total_logs = 0
        error_message = None
        json_output_sent = False  # Flag to track if we've already output JSON

        # Clear any previous run files
        current_run_files.clear()

        try:
            # Handle config generation if requested
            if generate_config:
                config_path = Path(generate_config)
                if config_path.exists():
                    if RICH_AVAILABLE and not json_output:
                        console.print(
                            f"[yellow]Warning: {generate_config} already exists. Skipping.[/yellow]"
                        )
                    else:
                        print(f"Warning: {generate_config} already exists. Skipping.")
                    return

                with open(config_path, "w") as f:
                    json.dump(get_default_config(), f, indent=4)

                if json_output and not json_output_sent:
                    output_json(True, 0, 0, [str(config_path)])
                    json_output_sent = True
                    return

                if RICH_AVAILABLE:
                    console.print(
                        f"[green]Configuration file generated: {generate_config}[/green]"
                    )
                else:
                    print(f"Configuration file generated: {generate_config}")
                return

            # Load configuration
            cfg = load_config(config if config else "config.json")

            # Set parameters from config or command line
            log_count = min(count or cfg.get("count", 100), 1_000_000)
            thread_count = threads or cfg.get("threads", multiprocessing.cpu_count())

            # Create output directory
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)

            # Load modules
            modules = load_modules()
            if not modules:
                msg = "Error: No modules found. Please check your installation."
                if json_output and not json_output_sent:
                    output_json(False, 0, 0, [], msg)
                    json_output_sent = True
                    ctx.exit(1)
                if RICH_AVAILABLE:
                    console.print(f"[red]{msg}[/red]")
                else:
                    print(msg)
                ctx.exit(1)

            # Select active services from config
            active_services = cfg.get("services", list(modules.keys()))
            active_modules = {k: v for k, v in modules.items() if k in active_services}

            if not active_modules:
                msg = "No active modules found. Check your configuration."
                if json_output and not json_output_sent:
                    output_json(False, 0, 0, [], msg)
                    json_output_sent = True
                    ctx.exit(1)
                if RICH_AVAILABLE:
                    console.print(f"[yellow]{msg}[/yellow]")
                    console.print(f"Available modules: {', '.join(modules.keys())}")
                    console.print(
                        f"Active services in config: {', '.join(active_services)}"
                    )
                else:
                    print(msg)
                    print(f"Available modules: {', '.join(modules.keys())}")
                    print(f"Active services in config: {', '.join(active_services)}")
                ctx.exit(1)

            # Show configuration summary
            if not json_output:
                if RICH_AVAILABLE:
                    console.print(
                        Panel.fit(
                            f"[bold]Configuration[/bold]\n"
                            f"Logs per module: {log_count}\n"
                            f"Active modules: {len(active_modules)}\n"
                            f"Threads: {thread_count}\n"
                            f"Output directory: {output_path}",
                            title="[bold blue]Log Generator 3000[/bold blue]",
                            border_style="blue",
                        )
                    )
                else:
                    print("\nConfiguration:")
                    print(f"Logs per module: {log_count}")
                    print(f"Active modules: {len(active_modules)}")
                    print(f"Threads: {thread_count}")
                    print(f"Output directory: {output_path}\n")

            # Generate logs using thread pool
            if not json_output:
                msg = f"Generating logs using {thread_count} threads..."
                if RICH_AVAILABLE:
                    console.print(f"[blue]{msg}[/blue]")
                else:
                    print(msg)

            # Initialize progress display
            module_order.clear()  # Clear any previous order
            for name in active_modules:
                module_order.append(name)
                module_status[name] = "Waiting"
                module_progress[name] = "0.0%"
            if not json_output:
                print(format_progress_display())

            try:
                # Process modules sequentially if thread_count is 1
                if thread_count == 1:
                    for name, func in active_modules.items():
                        if exit_event.is_set():
                            break
                        generate_module_logs(
                            name, func, log_count, output_path, json_output
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
                            )
                            for name, func in active_modules.items()
                        ]
                        try:
                            concurrent.futures.wait(futures)
                        except KeyboardInterrupt:
                            exit_event.set()
                            # Wait for running tasks to finish gracefully
                            concurrent.futures.wait(futures, timeout=1)

                if exit_event.is_set():
                    error_message = "Generation cancelled"
                    if (
                        sys.stdin.isatty() and not json_output
                    ):  # Only ask if running in a terminal and not in JSON mode
                        keep = click.confirm(
                            "\nKeep partially generated files?", default=False
                        )
                        cleanup_files(keep)
                    if json_output and not json_output_sent:
                        time_taken = (datetime.now() - start_time).total_seconds()
                        output_json(False, 0, time_taken, [], error_message)
                        json_output_sent = True
                    elif not json_output:
                        print("\nExiting...")
                    ctx.exit(1)  # Exit after handling the interrupt
                else:
                    # Add final newline if not in JSON mode
                    if not json_output:
                        print()
                        msg = "Log generation complete!"
                        if RICH_AVAILABLE:
                            console.print(f"[green]{msg}[/green]")
                        else:
                            print(msg)

                # Calculate total logs and collect file paths
                for file_path in current_run_files:
                    if Path(file_path).exists():
                        generated_files.append(str(file_path))
                        total_logs += log_count

                # Output JSON if requested
                if json_output and not json_output_sent:
                    time_taken = (datetime.now() - start_time).total_seconds()
                    output_json(
                        error_message is None,
                        total_logs,  # Use actual total logs
                        time_taken,
                        generated_files,
                        error_message,
                    )
                    json_output_sent = True
                    return  # Let the function return normally for success

            except KeyboardInterrupt:
                exit_event.set()
                error_message = "Generation cancelled"
                if (
                    sys.stdin.isatty() and not json_output
                ):  # Only ask if running in a terminal and not in JSON mode
                    keep = click.confirm(
                        "\nKeep partially generated files?", default=False
                    )
                    cleanup_files(keep)
                if json_output and not json_output_sent:
                    time_taken = (datetime.now() - start_time).total_seconds()
                    output_json(False, 0, time_taken, [], error_message)
                    json_output_sent = True
                elif not json_output:
                    print("\nExiting...")
                ctx.exit(1)  # Exit after handling the interrupt

        except KeyboardInterrupt:
            exit_event.set()
            error_message = "Generation cancelled"
            if (
                sys.stdin.isatty() and not json_output
            ):  # Only ask if running in a terminal and not in JSON mode
                keep = click.confirm("\nKeep partially generated files?", default=False)
                cleanup_files(keep)
            if json_output and not json_output_sent:
                time_taken = (datetime.now() - start_time).total_seconds()
                output_json(False, 0, time_taken, [], error_message)
                json_output_sent = True
            elif not json_output:
                print("\nExiting...")
            ctx.exit(1)  # Exit after handling the interrupt

    except Exception as e:
        error_message = (
            str(e) if isinstance(e, click.exceptions.Exit) else e
        )  # Convert Exit object to string
        if json_output and not json_output_sent:
            output_json(False, 0, 0, [], error_message)
            json_output_sent = True
            ctx.exit(1)  # Exit after handling the error
        elif not json_output:
            msg = f"Error: {str(error_message)}"
            if RICH_AVAILABLE:
                console.print(f"[red]{msg}[/red]")
            else:
                print(msg)
            ctx.exit(1)  # Exit after handling the error


def main():
    """CLI entry point."""
    cli()
