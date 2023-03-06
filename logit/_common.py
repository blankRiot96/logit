import json
import os
from pathlib import Path


def get_path(path: str | Path, file=True) -> Path:
    path = Path(path)
    if not path.exists():
        if file:
            path.touch()
        else:
            path.mkdir()

    return path


LEVEL: str = "CLUTTER"
APP_DATA_FOLDER = get_path(Path(os.getenv("APPDATA")) / "logit", file=False)
LOCAL_CONFIG_PATH = get_path(".logit/", file=False)
CONFIG_FILE = LOCAL_CONFIG_PATH / "config.json"
ARCHIVES_FOLDER = get_path(LOCAL_CONFIG_PATH / "archives", file=False)

if not CONFIG_FILE.exists():
    with open(CONFIG_FILE, "w") as f:
        json.dump({}, f, indent=2)
