_UNIT_MULTIPLIERS = {"kb": 1, "mb": 1e3, "gb": 1e6, "tb": 1e9}


def _premature_split_space_data(text: str) -> tuple[str, str]:
    """Prematurely splits the space data into
    its constituent time period and unit (may not
    be correct)."""

    digit_index = 0
    for char in text:
        if char.isdigit():
            digit_index += 1
        else:
            break

    return text[:digit_index], text[digit_index:]


def _check_valid_space_syntax(text: str) -> bool:
    """Checks if the given text is valid."""

    n_alpha = len(c for c in text if c.isalpha())
    is_alnum = text.isalnum()
    is_safe_split = not any(
        char.isdigit() for char in _premature_split_space_data(text)[1]
    )

    return (n_alpha == 1) and is_alnum and is_safe_split


def _split_space_data(text: str) -> tuple[int, str]:
    """Splits the given text into its constituent
    quantity and unit."""

    quantity, unit = _premature_split_space_data(text)
    return int(quantity), unit


def parse_space_data(text: str) -> int:
    """Gets the number of kilobytes mentioned
    in a string specifying a certain amount
    of space.

    Arguments:
        text: The text to parse.

    Example:
        parse_space_data("5mb") -> 5000
    """

    if not _check_valid_space_syntax(text):
        raise ValueError(f"'{text}' is not a valid string literal for the space data.")

    quantity, unit = _split_space_data(text)
    return quantity * _UNIT_MULTIPLIERS[unit]
