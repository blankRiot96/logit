import typing as _t
from enum import Enum, StrEnum, auto


class Level(StrEnum):
    """An enum to represent the different levels of the
    logging class.

    CLUTTER - For temporary clutter messages
    INFO - Information related to application
    DEBUG - Debug messages
    WARNING - Warnings
    ERROR - Error occured
    """

    CLUTTER = auto()
    INFO = auto()
    DEBUG = auto()
    WARNING = auto()
    ERROR = auto()

    def get_inversed_dict(self) -> dict:
        """Gets the inversed representation of the Level enum.

        Example:
        {
          "clutter": Level.CLUTTER,
          "info": Level.INFO,
          ...
        }
        """
        return {variant.value: variant for variant in Level}

    def get_from_value(value: str) -> None:
        """Gets the Enum variant from its value.

        Arguments:
            value: The value of the enum variant.
        """

        inversed_dict = Level.get_inversed_dict()
        variant = inversed_dict.get(value)

        if variant is None:
            raise ValueError(f"'{value}' is not a valid value of any variant.")

        return variant

    def get_level_value(level: Enum) -> int:
        """Gets the level ranking of the level."""

        return tuple(Level).index(level)
