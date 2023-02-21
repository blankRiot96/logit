"""Handles all App Data for logit."""

import datetime
import json
import shutil
import time
from functools import lru_cache
from pathlib import Path

from ._common import APP_DATA_FOLDER, CONFIG_FILE


@lru_cache
def get_logit_config() -> dict:
    """Gets the logit configuration.

    Example:
    get_logit_config() -> {
        files: {
            "path/to/app.log": {
                "last_rotation": 120981923091,
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
    config["files"][log_file_path]["last_rotation"] = time.time()
    set_logit_config(config)


def get_last_rotation_time(log_file_path: Path) -> int:
    """Gets the last rotation time for log file in AppData."""

    config = get_logit_config()

    if config["files"].get(log_file_path) is None:
        config["files"][log_file_path] = {"last_rotation": time.time()}
        print("baby")
        set_logit_config(config)
    return config["files"][log_file_path]["last_rotation"]


def _create_archive_logfile_name(log_file_path: Path) -> str:
    """Creates an archive logfile name."""
    now = datetime.datetime.now()
    return f"{now.date()}-archive-{log_file_path.name}"


def move_log_file(log_file_path: Path) -> None:
    """Moves the log file path and creates an archive."""
    shutil.move(log_file_path, _create_archive_logfile_name(log_file_path))
    log_file_path.touch()
