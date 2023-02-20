import os
from pathlib import Path


def get_path(path: str | Path, file=True) -> Path:
    path = Path(path)
    if not path.exists:
        if file:
            path.touch()
        else:
            path.mkdir()

    return path


LEVEL: str = "CLUTTER"
APP_DATA_FOLDER = get_path(os.get("APPDATA") + "/logit")
CONFIG_FILE = get_path(APP_DATA_FOLDER / "config.json")
