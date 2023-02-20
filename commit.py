"""To be ran to commit changes."""

import subprocess

subprocess.run("pre-commit")
subprocess.run("aicommits.cmd")
