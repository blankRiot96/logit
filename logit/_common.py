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
CONFIG_FILE = get_path(APP_DATA_FOLDER / "config.json")
with open(CONFIG_FILE, "w") as f:
    json.dump({"files": {}}, f, indent=2)
