"""Handles all App Data for logit."""

import csv
import datetime
import json
import shutil
import time
from functools import lru_cache
from pathlib import Path
import xml.etree.ElementTree as ET

from ._common import APP_DATA_FOLDER, CONFIG_FILE


@lru_cache
def get_logit_config() -> dict:
    """Gets the logit configuration.

    Example:
    get_logit_config() -> {
        files: {
            "path/to/app.log": {
                "last_rotation": 1677050919.7114477,
            },
            ...
        }
    }
    """
    with open(CONFIG_FILE) as f:
        data = json.load(f)

    return data


def set_logit_config(config: dict) -> None:
    """Sets the logit configuration."""

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def save_last_rotation_time(log_file_path: Path) -> None:
    """Saves the last rotation time for log file to AppData."""

    config = get_logit_config()
    abs_path = str(log_file_path.absolute())
    config["files"][abs_path]["last_rotation"] = time.time()
    set_logit_config(config)


def get_last_rotation_time(log_file_path: Path) -> int:
    """Gets the last rotation time for log file in AppData."""

    config = get_logit_config()
    abs_path = str(log_file_path.absolute())

    if config["files"].get(abs_path) is None:
        print("why is this happening")
        config["files"][abs_path] = {"last_rotation": time.time()}
        set_logit_config(config)
    return config["files"][abs_path]["last_rotation"]


def _create_archive_logfile_name(log_file_path: Path) -> str:
    """Creates an archive logfile name."""
    now = datetime.datetime.now()
    archive_file_name = f"{now.date()}-archive-{log_file_path.name}"
    return (APP_DATA_FOLDER / Path(archive_file_name)).absolute()


def move_log_file(log_file_path: Path) -> None:
    """Moves the log file path and creates an archive."""
    shutil.move(log_file_path, _create_archive_logfile_name(log_file_path))
    log_file_path.touch()


def get_json_logs(file_path: Path) -> list:
    """Gets the structural logs in JSON format."""
    try:
        with open(file_path) as f:
            logs = json.load(f)
    except json.decoder.JSONDecodeError:
        with open(file_path, "w") as f:
            json.dump([], f, indent=2)
            return []

    return logs


def get_xml_logs(file_path: Path) -> list:
    """Gets the structural logs in XML format."""

    logs = []
    tree = ET.parse(file_path)
    root = tree.getroot()

    for log in root.findall("log"):
        true_log = {}
        for attr in log.iterfind("*"):
            true_log[attr.tag] = attr.text
        logs.append(true_log)

    return logs


def get_csv_logs(file_path: Path) -> list:
    """Gets the structural logs in CSV format."""

    with open(file_path) as f:
        reader = csv.reader(f)

        return list(reader)
