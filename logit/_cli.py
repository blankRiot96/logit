"""
All CLI related operations are contained in this file.
"""

import argparse
from ._common import ARCHIVES_FOLDER
import os


class CLI:
    """The CLI handler."""

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(
            "logit", description="Handle the logs for your application."
        )
        self.parser.add_argument(
            "directory",
            type=str,
            help="The project to handle.",
        )
        self.parser.add_argument(
            "--clear-archives",
            action="store_const",
            default=self.parser.print_help,
            const=self.clear_archives,
            help="Clears all archives for the project.",
        )

        self.args = self.parser.parse_args()

    def clear_archives(self) -> None:
        """
        $ logit clear-archives
        * Clearing all archives for {project}...
        * Removing {archive-file-name}
        ...

        Done ✅
        """

        print(f"* Clearing all archives for {os.getcwd()}...")

        for file in ARCHIVES_FOLDER.iterdir():
            print(f"* Removing {file.name}")
            os.remove(file)

        print("Done ✅")
