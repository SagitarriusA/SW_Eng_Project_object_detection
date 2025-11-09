#!/usr/bin/env python3

"""
file: log_data.py
description: File that logs detected shapes into csv file
dependencies: os, datetime
classes: customized_datatypes
"""

import os
from datetime import datetime
from customized_datatypes import LogMessage


class DataLogger:  # pylint: disable=too-few-public-methods
    """Class for the data logging"""

    def __init__(self) -> None:
        """
        Init function for the class

        Args: None

        Return: None
        """

        # Generate the dir for the logs if it's still missing:
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
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
            print(f"[Info] Started logging to {self.log_path}")

    def log(self, message: LogMessage) -> None:
        """
        Public function to log the shape name and mean color

        arg: message.shape (str), message.color (str)

        return: None
        """

        # Write the current time, detected shape and color into the csv file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(f"{timestamp:<22} {message.color:<17} {message.shape:<10}\n")
        except (PermissionError, OSError) as e:
            print(f"[LOG ERROR] Could not write to {self.log_path}: {e}")


if __name__ == "__main__":
    try:
        logging = DataLogger()
    except PermissionError as e:
        print(f"[ERROR] {e}")

    else:
        # Test the logging with a few logs:
        logging.log(LogMessage(shape="circle", color="red"))
        logging.log(LogMessage(shape="pentagon", color="purple"))
        logging.log(LogMessage(shape="circle", color="blue"))
        logging.log(LogMessage(shape="circle", color="yellow"))
