import datetime
import inspect
import os

import colorama

from . import _common
from .types_ import LogFormatDict, LogFormatCallable

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


def line_number(abstraction: int = 4, color: bool = False) -> str:
    """Gets the line number and file name at which a function is called."""
    total_stack = inspect.stack()  # total complete stack
    frameinfo = total_stack[abstraction][0]  # info on rel frame

    filename = os.path.basename(frameinfo.f_code.co_filename)
    line_number = frameinfo.f_lineno

    if color:
        return _get_colored_str(f"{filename}:{line_number}", colorama.Fore.LIGHTCYAN_EX)
    return f"{filename}:{line_number}"


def level(color: bool = False) -> str:
    """Returns the current level of logging."""

    if color:
        level = _get_colored_str(_common.LEVEL, _LEVEL_COLORS[_common.LEVEL])
        level = f"[{level}]"
    else:
        level = f"[{_common.LEVEL}]"

    return level


def _merge_output(
    output: str, format_: str, callables: list[LogFormatCallable], color: bool
) -> str:
    """Merges the output for the given callable."""

    for callable in callables:
        if color and "color" in inspect.getfullargspec(callable).args:
            s = format_.format(output=callable(color=True))
        else:
            s = format_.format(output=callable())

        output += s

    return output


def _output_builder(format: LogFormatDict, msg: object, color: bool = False) -> str:
    """Builds the output from the given format."""

    output = ""
    output = _merge_output(output, "{output} | ", format["msg-prefix"], color)
    output += msg
    output = _merge_output(output, " | {output}", format["msg-suffix"], color)

    return output
