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
    # remove the PIP_USER env var to prevent the --user conflict
    env = os.environ.copy()
    env.pop("PIP_USER", None)

    if not requirements:
        print("No requirements found in config.ini [install] section.")
        return
    
    
    # build final pip command

    cmd = [sys.executable, "-m", "pip", "install","--no-user", "--upgrade", "--target", target_dir,*requirements]

    print(f"Installing{len(requirements)} dependencies into {target_dir}...")
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd, env=env)
    print("Installation complete!")


if __name__ == "__main__":
    install_local_requirements()