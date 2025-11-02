#!/usr/bin/env python3

"""
file: main.py
description: Main file to read and process the input stream of a camera or a given image
author: Bauer Ryoya, Walter Julian, Willmann York
date: 2025-11-02
version: 1.2
changes: typo-changes according to Pylint, styling changes
dependencies: argparse, os, sys, PyQt5.QtWidgets, numpy
classes: ImageProcessor, GeometricObjectsGui
"""

import argparse
import os
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication
from image_processing import ImageProcessor
from gui import GeometricObjectsGui


def main() -> None:
    """
    Function to run the code

    args: None

    return: None
    """

    # Setup the argparser for the console input:
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
        try:
            processor = ImageProcessor(cam_device=0, image_path=None)
        except (RuntimeError, FileNotFoundError, ValueError, PermissionError) as e:
            print(f"[ERROR] {e}")

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

        try:
            processor = ImageProcessor(image_path=image_files[0])
        except (RuntimeError, FileNotFoundError, ValueError, PermissionError) as e:
            print(f"[ERROR] {e}")

        images: list[tuple[np.ndarray, dict[str, int]]] = []

        for path in image_files:
            image = processor.load_image(path)
            image, shapes_count = processor.process_frame(image)
            images.append((image, shapes_count))

        # Initialize the GUI with the list of images
        gui = GeometricObjectsGui(
            processor=processor, is_camera=False, image_list=images
        )
        gui.show()
        sys.exit(app.exec_())

    else:
        print("[ERROR] Please specify either --camera or --image")
        return


if __name__ == "__main__":
    main()
