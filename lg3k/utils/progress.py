"""Progress tracking utilities."""


def create_progress_bar(percentage: float, width: int = 20) -> str:
    """Create a progress bar string.

    Args:
        percentage: Progress percentage (0-100)
        width: Width of the progress bar in characters

    Returns:
        Progress bar string (e.g. "[===>    ]")
    """
    filled = int(width * percentage / 100)
    if filled < width:
        arrow = ">"
    else:
        arrow = "="
        filled -= 1
    bar = "=" * filled + arrow + " " * (width - filled - 1)
    return f"[{bar}]"


def update_progress(current: int, total: int) -> str:
    """Update progress bar and return progress string.

    Args:
        current: Current progress value
        total: Total progress value

    Returns:
        Progress string (e.g. "50.0%")
    """
    percentage = (current / total) * 100
    # Create progress bar and ensure consistent width for progress values
    progress_bar = create_progress_bar(percentage)
    return f"{progress_bar} {percentage:5.1f}%"
