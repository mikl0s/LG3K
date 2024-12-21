"""Progress tracking utility module for LG3K.

This module provides functionality for tracking and displaying progress
during log generation, including multi-threaded operations.
"""

from rich.progress import Progress, SpinnerColumn, TextColumn


def run_with_progress(total, callback):
    """Run a task with a progress bar.

    Args:
        total (int): Total number of items to process.
        callback (callable): Function to call for each progress update.

    Returns:
        list: Results from the callback function.
    """
    results = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Generating logs...", total=total)
        for _ in range(total):
            result = callback()
            results.append(result)
            progress.update(task, advance=1)
    return results
