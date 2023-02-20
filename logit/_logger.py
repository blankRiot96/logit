import os
import pathlib as _p
import typing as _t

from . import _common
from ._enums import Level
from .output import _output_builder, level, line_number
from .types_ import LogConfigDict


class Logger:
    """A singleton logger class.

    Example:
        from logit import log
        log.clutter("Test!!")  # 19:30:1 | test.py:2 | Test!! | CLUTTER
    """

    def __init__(self) -> None:
        self.__level = Level.CLUTTER
        self.rank = self.level.get_level_value()
        self.log_file_path: _p.Path | str = "app.log"
        self.format = {"msg-prefix": [level, line_number], "msg-suffix": []}

    @property
    def level(self) -> Level:
        return self.__level

    @level.setter
    def level(self, val: Level) -> None:
        self.__level = val
        self.rank = self.__level.get_level_value()

    def _output(self, msg: object) -> None:
        """Prints out log outputs to console and log file."""
        output = _output_builder(self.format, msg)

        if not os.path.exists(self.log_file_path):
            _p.Path(self.log_file_path).touch()

        with open(self.log_file_path, "a") as f:
            f.write(output + "\n")
        print(_output_builder(self.format, msg))

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
    ) -> LogConfigDict:
        """Configurates the logger.

        Arguments:
            level: The level of logging.
            log_file_path: The Location of the log file.

        Returns:
            A dictionary containing the relevant log config
        """
        self.level = level
        self.log_file_path = log_file_path

        return {"level": self.level.value, "log_file_path": str(log_file_path)}

    def clutter(self, msg: object = "") -> None:
        """Clutter the terminal with temporary logs.

        Arguments:
            msg: A message to clutter the terminal with.
        """
        if self.rank > 0:
            return

        _common.LEVEL = "CLUTTER"
        self._output(msg)

    def info(self, msg: object = "") -> None:
        """Log some information.

        Arguments:
            msg: A message to clutter the terminal with.
        """
        if self.rank > 1:
            return

        _common.LEVEL = "INFO"
        self._output(msg)

    def debug(self, msg: object = "") -> None:
        """Log some debug messages.

        Arguments:
            msg: A message to clutter the terminal with.
        """
        if self.rank > 2:
            return

        _common.LEVEL = "DEBUG"
        self._output(msg)

    def warning(self, msg: object = "") -> None:
        """Warn user in logs.

        Arguments:
            msg: A message to clutter the terminal with.
        """
        if self.rank > 3:

            return

        _common.LEVEL = "WARNING"
        self._output(msg)

    def error(self, msg: object = "") -> None:
        """Mention presence of error in logs.

        Arguments:
            msg: A message to clutter the terminal with.
        """
        if self.rank > 4:
            return

        _common.LEVEL = "ERROR"
        self._output(msg)
