#!/usr/bin/env python3

"""
file: setup_local_env.py
description: Setup file to install the libraries (packages) into the .venv
author: Bauer Ryoya, Walter Julian, Willmann York
date: 2025-10-20
version: 1.0
dependencies: configparser, subprocess, os, sys
"""

import configparser
import subprocess
import sys
import os
import platform 


def install_local_requirements():
    """Installs local dependencies"""
    config = configparser.ConfigParser()
    config.read("config.ini")

    requirements = [
        pkg.strip()
        for pkg in config.get("install", "requirements", fallback="").split(",")
        if pkg.strip()
    ]

    if not requirements:
        print("No requirements found in config.ini [install] section.")
        return
    
    # If the script runs on lnux install PyQt5 with sudo and define the link to it

    is_linux = platform.system() == "Linux"
    
    if is_linux and "PyQt5" in requirements:
        print("Detected Linux -> Installing PyQt5 via apt (pip version is broken on Linux).")
        try:
            subprocess.check_call(["sudo", "apt", "update"])
            subprocess.check_call(["sudo", "apt", "-y", "install", "python3-pyqt5"])
            print("PyQt5 installed via apt successfully")
        except Exception as e:
            print(f"Error installing PyQt5 via apt: {e}")
            print("Please install manually: sudo apt install python3-pyqt5")

        requirements.remove("PyQt5")
    venv_site = next(
        p for p in sys.path if p.endswith("site-packages")
    )
    pth_file = os.path.join(venv_site, "pyqt5-system.pth")

    print(f"writing  .pth file so venv can use system PyQt5 => {pth_file}")

    with open(pth_file, "w", encoding="uft-8") as f:
        f.write("/usr/lib/python3/dist-packages\n")

    print("Venv is now linked to system PyQt5.")
    # remove the PIP_USER env var to prevent the --user conflict
    env = os.environ.copy()
    env.pop("PIP_USER", None)

    # build final pip command
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", *requirements]

    print(f"Installing {len(requirements)} libs...")
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd, env=env)
    print("Installation complete!")


def setup_pylint_config():
    """Creates .pylintrc if not available yet."""
    pylintrc_path = ".pylintrc"
    if not os.path.exists(pylintrc_path):
        print("Creating default .pylintrc for PyQt5 and project classes...")
        with open(pylintrc_path, "w", encoding="utf-8") as f:
            f.write(
                """[MASTER]
ignore=venv

[TYPECHECK]
ignored-modules=PyQt5,PyQt5.QtWidgets,PyQt5.QtGui,PyQt5.QtCore,image_processing,shape_speaker
ignored-classes=ImageProcessor,ShapeSpeaker,QWidget,QLabel,QPushButton,QTimer,QImage,QPixmap
generated-members=cv2.*,Qt.*

[MESSAGES CONTROL]
disable=
    C0103,  # variable name style
    C0114,  # missing module docstring
    C0115,  # missing class docstring
    C0116,  # missing function docstring
    E0611,  # no name in module
    E1101,  # no-member (PyQt5 dynamic attributes)
    R0903,  # too few public methods

"""
            )
    else:
        print(".pylintrc already exists – skipping creation.")


def setup_vscode_settings():
    """Creates VS Code Linting-Settings if not available."""
    vscode_dir = os.path.join(".vscode")
    os.makedirs(vscode_dir, exist_ok=True)
    settings_path = os.path.join(vscode_dir, "settings.json")

    settings_content = """{
    "python.linting.pylintArgs": [
        "--disable=C0103",
        "--ignored-modules=PyQt5"
    ]
}
"""
    if not os.path.exists(settings_path):
        print("Creating VS Code settings.json for Pylint...")
        with open(settings_path, "w", encoding="utf-8") as f:
            f.write(settings_content)
    else:
        print("VS Code settings.json already exists – skipping creation.")


if __name__ == "__main__":
    install_local_requirements()
    setup_pylint_config()
    setup_vscode_settings()
