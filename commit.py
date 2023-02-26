"""To be ran to commit changes."""

import subprocess

subprocess.run("pre-commit")
subprocess.run("git add .", shell=True)
subprocess.run("aicommits.cmd", shell=True)
