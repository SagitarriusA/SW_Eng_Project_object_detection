#!/usr/bin/env python3

"""
file: image_processing.py
description: File that contains the class for the processing of the frames
author: Bauer Ryoya, Walter Julian, Willmann York
date: 2025-10-11
version: 1.0
dependencies: OpenCV (cv2), os, numpy
classes: DataLogger
"""

import cv2
import os
import numpy as np
from log_data import DataLogger
import ShapeSpeaker


# Setup class:
class ImageProcessor:
    def __init__(self, cam_device=None, image_path=None):
        # Setup variables:
        self.cam_device = cam_device
        self.image_path = image_path
        self.cap = None
        self.image = None
        self.is_camera = False

        try:
            self.logging = DataLogger()
        except (PermissionError) as e:
            print(f"[ERROR] {e}")

        else:
            # Init the source:
            self._init_source()

    def _init_source(self):
        # Init the cam / read the image:
        if self.cam_device is not None:
            print(f'Initializing camera device {self.cam_device}')

            # For the build in web cam use the standard capture method:
            if self.cam_device == 0:
                self.cap = cv2.VideoCapture(self.cam_device)
            # For an external USB device use cv2.CAP_DSHOW in addition:
            else:
                self.cap = cv2.VideoCapture(self.cam_device, cv2.CAP_DSHOW)

            # Raise an error if the device couldn't be opened:
            if not self.cap.isOpened():
                raise RuntimeError(f"Could not open camera device {self.cam_device}")

            # Enable the bool variable for the camera:
            self.is_camera = True
            print("Camera initialized successfully.")

        elif self.image_path is not None:
            print(f'Loading image from {self.image_path}')

            # Raise an error if the path is invalide:
            if not os.path.exists(self.image_path):
                raise FileNotFoundError(f"Image not found: {self.image_path}")

            # Read the image:
            self.image = cv2.imread(self.image_path)

            # Raise an error if the image exists, but the method failed to read it:
            if self.image is None:
                raise ValueError(f"Failed to read image: {self.image_path}")

            print("Image loaded successfully.")

        else:
            # Raise an error if there was no input source (user didn't define the source / default failed):
            raise ValueError("No input source provided (camera or image).")

    def get_frame(self):
        # Get a single frame from camera or the loaded image:
        if self.is_camera:
            ret, frame = self.cap.read()

            if not ret:
                # Raise an error if there is no frame from the camera:
                raise RuntimeError("Failed to capture frame from camera.")
            return frame
        else:
            return self.image

    def process_frame(self, image):
        # If the user passes an invalide image / empty image raise an error:
        if image is None:
            raise RuntimeError("Error, no image found to process")

        # Preprocessing of the frame:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 220, 255, cv2.THRESH_BINARY)

        # Morphological cleanup:
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # Find contours:
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Define the boundarys for the required area:
        MIN_AREA = 5000
        MAX_AREA = 500000
        
    

        # Search for the valide detected contours:
        for _, contour in enumerate(contours):
            area = cv2.contourArea(contour)

            # Skip to small / large contours:
            if area < MIN_AREA or area > MAX_AREA:
                continue

            # Approximate and label:
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # Draw the detected contour onto the frame:
            cv2.drawContours(image, [contour], -1, (0, 0, 0), 2)

            # Compute centroid:
            M = cv2.moments(contour)
            if M['m00'] != 0:
                x_mid = int(M['m10'] / M['m00'])
                y_mid = int(M['m01'] / M['m00'])
            else:
                x_mid = 0
                y_mid = 0

            # Check if it's a circle:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * area / (perimeter ** 2)

            (x, y), radius = cv2.minEnclosingCircle(contour)
            circle_area = np.pi * radius**2
            area_ratio = area / circle_area

            if circularity > 0.8 and area_ratio > 0.8:
                shape_name = "Circle"
            else:
                # Check if it's an other known geometry; if not set the lable to unknown:
                shape_name = {
                    3: "Triangle",
                    4: "Quadrilateral",
                    5: "Pentagon",
                    6: "Hexagon"
                }.get(len(approx), "Unknown")
            
    

            # Compute average color inside contour:
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            cv2.drawContours(mask, [contour], -1, 255, -1)

            mean_color = cv2.mean(image, mask=mask)

            color_name = self.closest_color_name((mean_color[0], mean_color[1], mean_color[2]))

            # Draw label:
            cv2.putText(image, f"{color_name}, {shape_name}", (x_mid - 40, y_mid), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

            self.logging.log(shape_name, color_name)
        
        return image

    def closest_color_name(self, bgr):
        # Convert the BGR values to HSV:
        b, g, r = bgr
        color_bgr = np.uint8([[[b, g, r]]])
        hsv = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2HSV)[0][0]
        h, s, v = hsv

        # Define HSV ranges for basic colors:
        color_ranges = {
            "red":       [(0, 70, 50), (10, 255, 255)],
            "red2":      [(170, 70, 50), (180, 255, 255)],
            "orange":    [(11, 70, 50), (20, 255, 255)],
            "yellow":    [(21, 70, 50), (35, 255, 255)],
            "green":     [(36, 70, 50), (85, 255, 255)],
            "cyan":      [(86, 70, 50), (100, 255, 255)],
            "blue":      [(101, 70, 50), (130, 255, 255)],
            "violet":    [(131, 70, 50), (180, 255, 255)],
            "white":     [(0, 0, 200), (180, 40, 255)],
            "gray":      [(0, 0, 40), (180, 40, 200)],
            "black":     [(0, 0, 0), (180, 255, 40)]
        }

        # Search for the best match between the mean color value and the defined intervall for the HSV colors:
        for name, (lower, upper) in color_ranges.items():
            lower_np = np.array(lower, dtype=np.uint8)
            upper_np = np.array(upper, dtype=np.uint8)

            if (lower_np[0] <= h <= upper_np[0] and
                lower_np[1] <= s <= upper_np[1] and
                lower_np[2] <= v <= upper_np[2]):

                if name == "red2":
                    name = "red"
                return name

        return "unknown"

    def release(self):
        # Release camera resource if open:
        if self.cap:
            self.cap.release()
            print("Camera released.")


if __name__ == "__main__":
    # Test the class with device 0:
    cam_device = None
    # cam_device = 0

    # Test the class with the test image:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "../images", "test_image_00.png")

    try:
        processor = ImageProcessor(cam_device=cam_device, image_path=image_path)
    except (FileNotFoundError, ValueError, RuntimeError) as e:
        print(f"[ERROR] {e}")

    else:
        # Run the real time application for the cam:
        if processor.is_camera:
            print("Running real-time camera processing (press 'q' to quit)")
            while True:
                # Collect the current frame and start the processing:
                frame = processor.get_frame()
                processed, _ = processor.process_frame(frame)

                # Display the result:
                cv2.imshow("Processed Frame", processed)
                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break

            # Release all ressources:
            processor.release()
            cv2.destroyAllWindows()
        # Run the application once for the image:
        else:
            print("Processing static image (press any key to close)")
            # Collect the current frame and start the processing on the image:
            frame = processor.get_frame()
            processed, _ = processor.process_frame(frame)

            # Wait for the user to close the window:
            cv2.imshow("Processed Image", processed)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
