"""
Console input:
python src/main.py --camera 0
python src/main.py --image image_001.png
"""

import argparse
import os
import cv2
from image_processing import ImageProcessor


def main():
    parser = argparse.ArgumentParser(description="Read from camera or image.")
    # Default: Laptop-camera
    parser.add_argument("--camera", type=int, help="Camera device index")
    parser.add_argument("--image", type=str, help="Image file name in /images/")
    args = parser.parse_args()

    # Construct image path if relative
    image_path = None
    
    if args.image:
        cam_device = None
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "../images", args.image)
        print(f'image path: {image_path}')

    elif args.camera:
        cam_device = args.camera
        image_path = None
        print(f'cam device: {cam_device}')
        
    else:
        cam_device = 0
        image_path = None


    # Initialize class
    processor = ImageProcessor(cam_device=cam_device, image_path=image_path)
    
    if processor.is_camera:
        print("Running real-time camera processing (press 'q' to quit)")
        while True:
            frame = processor.get_frame()
            processed = processor.process_frame(frame)

            cv2.imshow("Processed Frame", processed)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        processor.release()
        cv2.destroyAllWindows()

    else:
        print("Processing static image (press any key to close)")
        frame = processor.get_frame()
        processed = processor.process_frame(frame)

        cv2.imshow("Processed Image", processed)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
