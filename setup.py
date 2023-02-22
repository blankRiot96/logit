from setuptools import find_packages, setup

# py -m build
# twine upload dist/*
VERSION = "0.1.1"
DESCRIPTION = "A logging library."
LONG_DESCRIPTION = """
A logging library.
"""

# Setup
setup(
    name="logit-axis",
    version=VERSION,
    author="Axis (blankRiot96)",
    email="blankRiot96@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    # install_requires=["typer"],
    python_requires=">=3.11",
    keywords=["logging"],
    # classifiers=[
    #     "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    #     "Programming Language :: Python :: 3.7",
    #     "Programming Language :: Python :: 3.8",
    #     "Programming Language :: Python :: 3.9",
    #     "Programming Language :: Python :: 3.10",
    #     "Topic :: Artistic Software",
    #     "Topic :: Multimedia :: Sound/Audio",
    #     "Intended Audience :: End Users/Desktop",
    # ],
    # entry_points={"console_scripts": ["bp=boilerplate:main"]},
    # include_package_data=True,
    # data_files=[
    #     "pyhb/typing_tester/assets/pyhb_icon.png",
    #     "pyhb/typing_tester/assets/retry_icon.png",
    #     "pyhb/typing_tester/assets/settings_icon.png",
    #     "pyhb/typing_tester/words.txt",
    # ],
)
