import re


def escape_ansi(string: str):
    """Strips ansi escape sequences from a string."""
    ansi_escape = re.compile(r"(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", string)
