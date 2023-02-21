_UNIT_MULTIPLIERS = {
    "d": 24 * 60 * 60,
    "w": 7 * 24 * 60 * 60,
    "m": 30 * 24 * 60 * 60,
    "y": 365 * 24 * 60 * 60,
}


def _premature_split_time_data(text: str) -> tuple[str, str]:
    """Prematurely splits the time data into
    its constituent time period and unit (may not
    be correct)."""

    digit_index = 0
    for char in text:
        if char.isdigit():
            digit_index += 1
        else:
            break

    return text[:digit_index], text[digit_index:]


def _check_valid_time_syntax(text: str) -> bool:
    """Checks if the given text is valid."""

    n_alpha = len(c for c in text if c.isalpha())
    is_alnum = text.isalnum()
    is_safe_split = not any(char.isdigit() for char in _premature_split_time_data()[1])

    return (n_alpha == 1) and is_alnum and is_safe_split


def _split_time_data(text: str) -> tuple[int, str]:
    """Splits the given text into its constituent
    time period and unit."""

    quantity, unit = _premature_split_time_data()
    return int(quantity), unit


def parse_time_data(text: str) -> int:
    """Parses time data from given text.

    Arguments:
        text: Text to parse data from.
        Supports days, weeks, months and years.
        day -> "d"
        week -> "w"
        month -> "m"
        year -> "y"

    Example:
        parse_time_data("5d") -> 24 * 5 * 60 * 60
        parse_time_data("3y") -> 24 * 365 * 60 * 60
    """

    if not _check_valid_time_syntax(text):
        raise ValueError(f"'{text}' is not a valid string literal for the time data.")

    quantity, unit = _split_time_data(text)
    return quantity * _UNIT_MULTIPLIERS[unit]
