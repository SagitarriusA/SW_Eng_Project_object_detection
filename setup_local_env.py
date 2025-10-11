import configparser
import subprocess
import sys
import os

def install_local_requirements():
    config = configparser.ConfigParser()
    config.read('config.ini')

    target_dir = config.get('install', 'target_dir',fallback='libs')
    requirements = [
        pkg.strip() for pkg in config.get('install', 'requirements', fallback='').split(',')
        if pkg.strip()
    ]

    os.makedirs(target_dir, exist_ok= True)

    #build pip command
    cmd = [sys.executable, "-m", "pip", "install", "--target", target_dir] + requirements

    print(f"Installing{len(requirements)} dependencies into {target_dir}...")
    subprocess.check_call(cmd)
    print("Installation complete!")


if __name__ == "__main__":
    install_local_requirements()