from typing import Optional


def write_file(path: str, content: str) -> Optional[str]:
    """Write content to a file and return the path."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path
    except Exception:
        return None

