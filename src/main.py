#!/usr/bin/env python3

"""
file: main.py
description: Main file to read and process the input stream of a camera or a given image
author: Bauer Ryoya, Walter Julian, Willmann York
date: 2025-10-11
version: 1.0
dependencies: argparse, os, OpenCV (cv2)
classes: ImageProcessor
"""

import argparse
import os
import cv2
from image_processing import ImageProcessor


def main():
    # Setup parser:
    parser = argparse.ArgumentParser(description="Read from camera or image.")
    parser.add_argument("--camera", type=int, help="Camera device index")
    parser.add_argument("--image", type=str, help="Image file name in /images/")
    args = parser.parse_args()

    # Construct image path:
    image_path = None
    if args.image:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "../images", args.image)

        print(f'image path: {image_path}')

        cam_device = None

    elif args.camera:
        cam_device = args.camera
        print(f'Reading from cam device: {cam_device}')
        image_path = None

        print(f"Camera device: {cam_device}")

    else:
        # Default setup:
        cam_device = 0
        image_path = None

    # Initialize class:
    try:
        processor = ImageProcessor(cam_device=cam_device, image_path=image_path)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"[ERROR] {e}")

    else:
        # Real time processing for the camera device:
        if processor.is_camera:
            print("Running real-time camera processing (press 'q' to quit)")

            while True:
                # Get the current frame for processing:
                frame = processor.get_frame()
                processed = processor.process_frame(frame)

                cv2.imshow("Processed Frame", processed)

                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break

            processor.release()
            cv2.destroyAllWindows()
        # Process the image:
        else:
            print("Processing static image (press any key to close)")
            frame = processor.get_frame()
            processed = processor.process_frame(frame)

            cv2.imshow("Processed Image", processed)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
