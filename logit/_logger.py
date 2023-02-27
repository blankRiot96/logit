from __future__ import annotations

import os
import pathlib as _p
import json
import xml
import shutil
import time
import typing as _t
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, ElementTree

from . import _common
from ._data import (
    get_last_rotation_time,
    move_log_file,
    save_last_rotation_time,
    get_json_logs,
)
from ._enums import Level, OutputFormat
from ._time import parse_time_data
from ._space import parse_space_data
from .output import _output_builder, level, line_number, local_time
from .types_ import LogConfigDict, LogFormatDict
from ._helper import escape_ansi


class FormatNotSupported(Exception):
    """Invoked when a particular format is not supported."""


class StructualLogger:
    """A logger that handles structural logging."""

    def __init__(self, output_format: OutputFormat, logger: Logger) -> None:
        self.output_format = output_format
        self.logger = logger
        self._create_file()

    def _create_file(self) -> None:
        """Creates the structural log file."""
        self.file_name = (
            f"structured-{self.logger.log_file_path.stem}.{self.output_format.value}"
        )
        self.file_path = _common.get_path(self.file_name)

    def _build_log(self, msg: object) -> dict:
        """Builds the structured log."""
        log = {
            "msg": str(msg),
            "level": escape_ansi(level()),
            "line_number": escape_ansi(line_number()),
            "local_time": escape_ansi(local_time()),
        }
        output_callables = (
            self.logger.format["msg-prefix"] + self.logger.format["msg-suffix"]
        )
        for callable in output_callables:
            if callable in (local_time, line_number, level):
                continue
            log[callable.__name__] = escape_ansi(callable())

        return log

    def output_xml(self, msg: object) -> None:
        """Appends output to a structural XML file."""

        try:
            tree = ET.parse(self.file_path)
        except xml.etree.ElementTree.ParseError:
            data_tag = Element("data")
            tree = ElementTree(data_tag)

        log = self._build_log(msg)
        xml_log = Element("log")
        for key, value in log.items():
            sub_element = Element(key)
            sub_element.text = value
            xml_log.append(sub_element)
        root = tree.getroot()
        root.append(xml_log)
        tree.write(self.file_path)

    def output_json(self, msg: object) -> None:
        """Appends output to a structural JSON file."""

        logs = get_json_logs(self.file_path)
        log = self._build_log(msg)
        logs.append(log)
        with open(self.file_path, "w") as f:
            json.dump(logs, f, indent=2)

    def output(self, msg: object) -> None:
        """Outputs to relevant format."""
        if self.output_format == OutputFormat.JSON:
            self.output_json(msg)
        elif self.output_format == OutputFormat.XML:
            self.output_xml(msg)
        else:
            raise FormatNotSupported(f"{self.output_format} is not supported yet.")


class Logger:
    """A singleton logger class.

    Example:
        from logit import log
        log.clutter("Test!!")  # 19:30:1 | test.py:2 | Test!! | CLUTTER
    """

    def __init__(self) -> None:
        self.__level = Level.CLUTTER
        self.rank = self.level.get_level_value()
        self.log_file_path: _p.Path | str = _p.Path("app.log")
        self.log_rotation_time: int | None = None
        self.log_rotation_space: int | None = None
        self.format: LogFormatDict = {
            "msg-prefix": [level, line_number],
            "msg-suffix": [],
        }
        self.structural_loggers: set[StructualLogger] = set()
        self._rotate_time()
        self._rotate_space()

    @property
    def level(self) -> Level:
        return self.__level

    @level.setter
    def level(self, val: Level) -> None:
        self.__level = val
        self.rank = self.__level.get_level_value()

    def _rotate_time(self) -> None:
        """Rotates log files based on time duration."""
        if self.log_rotation_time is None:
            return

        last_rotation_time = get_last_rotation_time(self.log_file_path)

        if time.time() - last_rotation_time > self.log_rotation_time:
            move_log_file(self.log_file_path)
            save_last_rotation_time(self.log_file_path)

    def _rotate_space(self) -> None:
        """Rotates log files based on space consumed by log file."""
        if self.log_rotation_space is None:
            return

        if len(self.log_file_path.read_bytes()) * 1000 >= self.log_rotation_space:
            move_log_file(self.log_file_path)

    def _create_log_file(self):
        """Creates log file if it doesn't already exist."""
        if not os.path.exists(self.log_file_path):
            _p.Path(self.log_file_path).touch()

    def _output_structural_logs(self, msg: object):
        """Run the output of all the structural loggers."""
        for structural_logger in self.structural_loggers:
            structural_logger.output(msg)

    def _write_to_log_file(self, output: str) -> None:
        """Writes the output to the log file."""
        with open(self.log_file_path, "a") as f:
            f.write(output + "\n")

    def _output(self, msg: object) -> None:
        """Prints out log outputs to console and log file."""
        output = _output_builder(self.format, msg)
        self._output_structural_logs(msg)
        self._create_log_file()

        self._write_to_log_file(output)
        print(_output_builder(self.format, msg))

    def add_structural_logger(self, output_format: OutputFormat) -> None:
        self.structural_loggers.add(StructualLogger(output_format, self))

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
        if set(log_config_dict) != {"level", "log_file_path", "rotation_time"}:
            raise ValueError("Required keys missing from log configuration dictionary.")

        self.level = Level.get_from_value(log_config_dict["level"])
        self.log_file_path = _p.Path(log_config_dict["log_file_path"])
        self.log_rotation_time = parse_time_data(log_config_dict["rotation_time"])

    def config(
        self,
        level: Level = Level.CLUTTER,
        log_file_path: _p.Path | str = "app.log",
        rotation_time: None | str = None,
        rotation_space: None | str = None,
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
        if self.log_rotation_time is not None:
            self.log_rotation_time = parse_time_data(rotation_time)

        if self.log_rotation_space is not None:
            self.log_rotation_space = parse_space_data(rotation_space)

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

    def critical(self, msg: object = "") -> None:
        """Mention presence of error in logs.

        Arguments:
            msg: Critical application hazard
            alerts.
        """
        if self.rank > 5:
            return

        _common.LEVEL = "CRITICAL"
        self._output(msg)
