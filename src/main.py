"""
Console input:
python src/main.py --camera 0
python src/main.py --image image_001.png
"""


import argparse
import os
import cv2
from BV_script import ImageProcessor  # Julian's part

def main():
    parser = argparse.ArgumentParser(description="Read from camera or image.")
    # Default: Laptop-camera
    parser.add_argument("--camera", type=int, help="Camera device index")
    parser.add_argument("--image", type=str, help="Image file name in /images/")
    args = parser.parse_args()

    # Construct image path if relative
    image_path = None
    if args.image:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "../images", args.image)

    # Initialize class
    processor = ImageProcessor(cam_device=args.camera, image_path=image_path)


if __name__ == "__main__":
    main()
