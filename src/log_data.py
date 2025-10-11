#!/usr/bin/env python3

"""
file: log_data.py
description: File that logs the detected geometrys into the csv file
author: Bauer Ryoya, Walter Julian, Willmann York
date: 2025-10-11
version: 1.0
dependencies: os, datetime
"""

import os
from datetime import datetime


class DataLogger:
    def __init__(self):
        # Generate the dir for the logs if it's still missing:
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.log_dir = os.path.join(self.project_root, "logs")
        os.makedirs(self.log_dir, exist_ok=True)

        # Generate the filename with the current date:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_path = os.path.join(self.log_dir, f"detections_{timestamp}.csv")

        # Setup the header for the csv file:
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(f"{'timestamp':<30} {'shape':<15} {'color':<10}\n")
        except (PermissionError, OSError) as e:
            print(f"[LOG ERROR] Could not write to {self.log_path}: {e}")
        else:
            print(f'Started logging to {self.log_path}')

    def log(self, shape, color):
        # Write the current time, detected shape and color into the csv file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(f"{timestamp:<22} {color:<17} {shape:<10}\n")
        except (PermissionError, OSError) as e:
            print(f"[LOG ERROR] Could not write to {self.log_path}: {e}")


if __name__ == "__main__":
    try:
        logging = DataLogger()
    except PermissionError as e:
        print(f"[ERROR] {e}")
    
    else:
        # Test the logging with a few logs:
        logging.log("circle", "red")
        logging.log("Pentagon", "purple")
        logging.log("circle", "blue")
        logging.log("circle", "yellow")