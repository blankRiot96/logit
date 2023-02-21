"""To be ran to commit changes."""

import subprocess

subprocess.run("git add .", shell=True)
subprocess.run("pre-commit", shell=True)
subprocess.run("aicommits.cmd", shell=True)
