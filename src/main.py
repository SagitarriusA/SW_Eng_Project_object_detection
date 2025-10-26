#!/usr/bin/env python3

"""
file: main.py
description: Main file to read and process the input stream of a camera or a given image
author: Bauer Ryoya, Walter Julian, Willmann York
date: 2025-10-11
date: 2025-10-26
version: 1.1
changes: typo-changes according to Pylint
dependencies: argparse, os, sys, PyQt5.QtWidgets
classes: ImageProcessor, GeometricObjectsGui
"""

import argparse
import os
import sys
from PyQt5.QtWidgets import QApplication
from image_processing import ImageProcessor
from gui import GeometricObjectsGui


def main():
    """Entry point for the program.

    Parses command-line arguments to read from the camera or an image folder
    and starts the corresponding processing.
    """
    parser = argparse.ArgumentParser(description="Read from camera or image folder.")
    parser.add_argument("--camera", action="store_true", help="Use camera device 0")
    parser.add_argument(
        "--image", action="store_true", help="Process all images in /images/"
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "../images")

    app = QApplication(sys.argv)

    if args.camera:
        # Use camera device 0
        processor = ImageProcessor(cam_device=0, image_path=None)
        gui = GeometricObjectsGui(processor=processor, is_camera=True)
        gui.show()
        sys.exit(app.exec_())

    elif args.image:
        # Collect all image paths in the folder
        image_files = sorted(
            [
                os.path.join(images_dir, f)
                for f in os.listdir(images_dir)
                if f.lower().endswith(
                    (
                        ".png",
                        ".jpg",
                        ".jpeg",
                        ".bmp",
                    )
                )
            ]
        )

        if not image_files:
            print(f"[ERROR] No images found in {images_dir}")
            return

        # Initialize the GUI with the list of images
        gui = GeometricObjectsGui(
            processor=None, is_camera=False, image_list=image_files
        )
        gui.show()
        sys.exit(app.exec_())

    else:
        print("[ERROR] Please specify either --camera or --image")
        return


if __name__ == "__main__":
    main()
