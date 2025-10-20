import configparser
import subprocess
import sys
import os

def install_local_requirements():
    config = configparser.ConfigParser()
    config.read('config.ini')

    requirements = [
        pkg.strip() for pkg in config.get('install', 'requirements', fallback='').split(',')
        if pkg.strip()
    ]

    if not requirements:
        print("No requirements found in config.ini [install] section.")
        return

    # remove the PIP_USER env var to prevent the --user conflict
    env = os.environ.copy()
    env.pop("PIP_USER", None)
    
    # build final pip command
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", *requirements]

    print(f"Installing {len(requirements)} libs...")
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd, env=env)
    print("Installation complete!")


if __name__ == "__main__":
    install_local_requirements()