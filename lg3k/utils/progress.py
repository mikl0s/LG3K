"""Progress tracking utilities."""


def update_progress(current: int, total: int) -> str:
    """Update progress bar and return progress string.

    Args:
        current: Current progress value
        total: Total progress value

    Returns:
        Progress string (e.g. "50%")
    """
    percentage = (current / total) * 100
    return f"{percentage:.1f}%"
