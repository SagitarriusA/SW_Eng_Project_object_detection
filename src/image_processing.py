#!/usr/bin/env python3

"""
file: image_processing.py
description: File that contains the class for the processing the frames
dependencies: cv2, numpy, typing
classes: DataLogger, customized_datatypes, LoadSources
"""

from typing import Optional, Tuple, Dict, Sequence, cast
import cv2
import numpy as np
from log_data import DataLogger
from load_sources import LoadSources
from customized_datatypes import LogMessage, Sources, Frame, ProcessedFrame


class ImageProcessor:
    """Setup the class for the image processing with the input of the camera / the images"""

    def __init__(self, loaded_source: "LoadSources") -> None:
        """
        Init function for the class

        args: loaded_source (LoadSources)
        
        return: None
        """

        self.source: "LoadSources" = loaded_source
        self.cap: Optional[cv2.VideoCapture] = loaded_source.cap
        self.is_camera: bool = loaded_source.is_camera

        # Init the data logging:
        try:
            self.logging = DataLogger()
        except PermissionError as e:
            print(f"[ERROR] {e}")
            raise

    # pylint: disable=too-many-locals
    # Tuple anpassen (siehe customized_datatypes)
    def process_frame(self, image: Frame) -> ProcessedFrame:
        """
        Process a frame to detect shapes, label them with color, and count shapes.

        args: image (Frame)

        return: ProcessedFrame
        """

        # If the user passes an invalide image / empty image raise an error:
        if image.frame is None:
            raise RuntimeError("Error, no image found to process")

        # Preprocessing of the frame:
        gray = cv2.cvtColor(image.frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, binary = cv2.threshold(blurred, 220, 255, cv2.THRESH_BINARY)

        # Morphological cleanup:
        kernel = np.ones((5, 5), np.uint8)
        opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        cleaned = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

        # Find contours:
        contours, _ = cv2.findContours(cleaned, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Define the boundarys for the required area:
        MIN_AREA = 5000
        MAX_AREA = 500000

        shapes_count: Dict[str, int] = {}

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
            cv2.drawContours(image.frame, [contour], -1, (0, 0, 0), 2)

            # Compute centroid:
            M = cv2.moments(contour)

            if M["m00"] != 0:
                x_mid = int(M["m10"] / M["m00"])
                y_mid = int(M["m01"] / M["m00"])
            else:
                x_mid = 0
                y_mid = 0

            # Check if it's a circle:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            circularity = 4 * np.pi * area / (perimeter**2)

            (_, _), radius = cv2.minEnclosingCircle(contour)
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
                    6: "Hexagon",
                }.get(len(approx), "Unknown")

            # Update the dict with the shape count:
            shapes_count[shape_name] = shapes_count.get(shape_name, 0) + 1

            # Compute average color inside contour:
            mask = np.zeros(image.frame.shape[:2], dtype=np.uint8)
            cv2.drawContours(mask, [contour], -1, 255, -1)  # type: ignore

            mean_color = cast(
                Tuple[float, float, float, float], cv2.mean(image.frame, mask=mask)
            )
            b_f, g_f, r_f, _ = mean_color
            b, g, r = int(b_f), int(g_f), int(r_f)
            color_name = self._closest_color_name((b, g, r))

            # Draw label:
            cv2.putText(
                image.frame,
                f"{color_name}, {shape_name}",
                (x_mid - 40, y_mid),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2,
            )

            self.logging.log(LogMessage(shape_name, color_name))

        return ProcessedFrame(image=image.frame, shapes_count=shapes_count)

    def _closest_color_name(self, bgr: Sequence[int]) -> str:
        """
        Function to calculate the mean color of the shape

        args: bgr (Tuple[int, int, int])

        return: color (str)
        """

        # Convert the BGR values to HSV:
        b, g, r = bgr
        color_bgr: np.ndarray = np.array([[[b, g, r]]], dtype=np.uint8)
        hsv: np.ndarray = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2HSV)[0][0]

        # Define HSV ranges for basic colors:
        color_ranges = {
            "red": [(0, 70, 50), (10, 255, 255)],
            "red2": [(170, 70, 50), (180, 255, 255)],
            "orange": [(11, 70, 50), (20, 255, 255)],
            "yellow": [(21, 70, 50), (35, 255, 255)],
            "green": [(36, 70, 50), (85, 255, 255)],
            "cyan": [(86, 70, 50), (100, 255, 255)],
            "blue": [(101, 70, 50), (130, 255, 255)],
            "violet": [(131, 70, 50), (180, 255, 255)],
            "white": [(0, 0, 200), (180, 40, 255)],
            "gray": [(0, 0, 40), (180, 40, 200)],
            "black": [(0, 0, 0), (180, 255, 40)],
        }

        # Search for the best matching color:
        for name, (lower, upper) in color_ranges.items():
            lower_np = np.array(lower, dtype=np.uint8)
            upper_np = np.array(upper, dtype=np.uint8)

            if np.all(lower_np <= hsv) and np.all(hsv <= upper_np):
                return "red" if name == "red2" else name

        return "unknown"

    def load_frame(self, data: Optional[Frame] = None) -> Frame:
        """
        Function to delegate frame loading to the LoadSources instance
        
        Args: data (Optional[Frame])
        
        Return: Frame
        """

        if data is None:
            data = Frame()

        return self.source.load_frame(data)

    def release(self) -> None:
        """
        Function to release the source resources
        
        Args: None
        
        Return: None
        """

        self.source.release()


if __name__ == "__main__":
    # First, set up the LoadSource
    source = LoadSources(Sources(cam_device=0))
    # OR source = LoadSource(image_path="images/test.jpg")

    # Then, pass that object to ImageProcessor
    processor = ImageProcessor(source)

    # You can now access attributes in ImageProcessor:
    print(processor.is_camera)
    print(processor.cap)
