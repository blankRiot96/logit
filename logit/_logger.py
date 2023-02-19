from ._enums import Level
from .types_ import LogConfigDict

import typing as _t
import pathlib as _p


class Logger:
    """A singleton logger class."""

    def __init__(self) -> None:
        self.level = Level.CLUTTER
        self.log_file_path: _p.Path | str = "app.log"

    def config_from_dict(self, log_config_dict: LogConfigDict) -> None:
        """Configurate the logger from a dictionary.

        Arguments:
            log_config_dict: A dictionary containing
            the relevant logging information.

        Example:
        log_config_dict = {
            "level": "debug",
            "log_file_path": "user_keys.log"
        }
        """
        if "level" not in log_config_dict or "log_file_path" not in log_config_dict:
            raise ValueError("Required keys missing from log configuration dictionary.")

        self.level = Level.get_from_value(log_config_dict["level"])
        self.log_file_path = log_config_dict["log_file_path"]

    def config(
        self,
        level: Level = Level.CLUTTER,
        log_file_path: _p.Path | str = "app.log",
        /,
    ) -> LogConfigDict:
        """Configurates the logger.

        Arguments:
            level: The level of logging.
            log_file_path: The Location of the log file.

        Returns:
            A dictionary containing the releveant log config
        """
        self.level = level
        self.log_file_path = log_file_path

        return {"level": self.level.value, "log_file_path": str(log_file_path)}
