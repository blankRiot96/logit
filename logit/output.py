import datetime
import inspect
import os

import colorama

from . import _common
from .types_ import LogFormatDict

_LEVEL_COLORS = {
    "CLUTTER": "",
    "INFO": colorama.Fore.CYAN,
    "DEBUG": colorama.Fore.GREEN,
    "WARNING": colorama.Fore.YELLOW,
    "ERROR": colorama.Fore.RED,
    "CRITICAL": colorama.Fore.MAGENTA,
}


def _get_colored_str(text: str, color: colorama.Fore, /) -> str:
    """Get a colored string with resets."""

    return f"{color}{text}{colorama.Fore.RESET}"


def local_time() -> str:
    """Returns the local time."""
    now = datetime.datetime.now()
    return f"{now.hour}:{now.minute}:{now.second}"


def line_number() -> str:
    """Gets the line number and file name at which a function is called."""
    total_stack = inspect.stack()  # total complete stack
    frameinfo = total_stack[4][0]  # info on rel frame

    filename = os.path.basename(frameinfo.f_code.co_filename)
    line_number = frameinfo.f_lineno

    return _get_colored_str(f"{filename}:{line_number}", colorama.Fore.LIGHTCYAN_EX)


def level() -> str:
    """Returns the current level of logging."""

    colored_level = _get_colored_str(_common.LEVEL, _LEVEL_COLORS[_common.LEVEL])
    return f"[{colored_level}]"


def _output_builder(format: LogFormatDict, msg: object) -> str:
    """Builds the output from the given format."""

    output = ""
    for prefix_callable in format["msg-prefix"]:
        output += f"{prefix_callable()} | "

    output += msg

    for suffix_callable in format["msg-suffix"]:
        output += f" | {suffix_callable()}"

    return output
