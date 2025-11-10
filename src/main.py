#!/usr/bin/env python3

"""
file: main.py
description: Main file to read and process the input stream of a camera or given images
dependencies: argparse, os, sys, numpy, PyQt5
classes: ImageProcessor, LoadSources, GeometricObjectsGui, customized_datatypes
"""

import argparse
import os
import sys
import numpy as np
from PyQt5.QtWidgets import QApplication
from image_processing import ImageProcessor
from load_sources import LoadSources
from gui import GeometricObjectsGui
from customized_datatypes import Sources, Frame


def main() -> bool:  # pylint: disable=too-many-return-statements
    """
    Function to run the code

    args: None

    return: None
    """

    # Setup the argparser for the console input:
    parser = argparse.ArgumentParser(description="Read from camera or image folder.")
    parser.add_argument("--camera", action="store_true", help="Use camera device 0")
    parser.add_argument(
        "--camera_index", type=int, default=0, help="Camera index (default: 0)"
    )
    parser.add_argument(
        "--image", action="store_true", help="Process all images in /images/"
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "../images")

    app = QApplication(sys.argv)

    if args.camera:
        cam_device = args.camera_index
        # Use camera device 0
        try:
            source = LoadSources(Sources(cam_device, image_path=None))
        except (
            RuntimeError,
            FileNotFoundError,
            ValueError,
            PermissionError,
            TypeError,
        ) as e:
            print(f"[ERROR] {e}")
            return False
        try:
            processor = ImageProcessor(source)
        except PermissionError as e:
            print(f"[ERROR] {e}")
            return False

        gui = GeometricObjectsGui(processor=processor, is_camera=True)
        gui.show()
        app.exec_()

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
            return False

        try:
            source = LoadSources(Sources(image_path=image_files[0]))
        except (
            RuntimeError,
            FileNotFoundError,
            ValueError,
            PermissionError,
            TypeError,
        ) as e:
            print(f"[ERROR] {e}")
            return False
        try:
            processor = ImageProcessor(source)
        except PermissionError as e:
            print(f"[ERROR] {e}")
            return False

        images: list[tuple[np.ndarray, dict[str, int]]] = []

        for path in image_files:
            image = source.load_frame(Frame(path=path))
            result = processor.process_frame(image)
            images.append((result.image, result.shapes_count))

        # Initialize the GUI with the list of images
        gui = GeometricObjectsGui(
            processor=processor, is_camera=False, image_list=images
        )
        gui.show()
        app.exec_()

    else:
        print("[ERROR] Please specify either --camera or --image")
        return False

    return True


if __name__ == "__main__":
    success = main()

    print(
        f"[Info] The program executed {'successfully' if success else 'with an error'}."
    )
