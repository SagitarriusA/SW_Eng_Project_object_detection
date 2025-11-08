import os
from typing import Optional
import cv2
import numpy as np


class LoadSources:
    """Setup the class for loading sources"""

    def __init__(
        self, cam_device: Optional[int] = None, image_path: Optional[str] = None
    ) -> None:
        """
        Function to init the class
        
        Args: cam_device (int), image_path (str)
        
        Return: None
        """

        self.cam_device: Optional[int] = cam_device
        self.image_path: Optional[str] = image_path
        self.cap: Optional[cv2.VideoCapture] = None
        self.image: Optional[np.ndarray] = None
        self.is_camera: bool = False

        # Init the source:
        try:
            self._init_source()
        except (RuntimeError, FileNotFoundError, ValueError) as e:
            print(f"[ERROR] Failed to initialize source: {e}")
            raise

    def _init_source(self) -> None:
        """
        Private function to init the cam / read images from the given path

        args: None

        return: None
        """

        if self.cam_device is not None:
            print(f"Initializing camera device {self.cam_device}")

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
            _ = self.load_frame(self.image_path)
        else:
            # Raise an error if no input source (user didn't define the source / default failed):
            raise ValueError("No input source provided (camera or image).")

    def load_frame(self, path: Optional[str] = None) -> np.ndarray:
        """
        Function to load the current frame of the camera or to load the frame from the given path

        Args: optional path (str), for the camera no path needed, but bool set to true

        Return: image (ndarray)
        """

        # Get a single frame from camera or the loaded image:
        if self.is_camera:
            # Check if self.cap is not None to be sure that the camera is initalized:
            assert self.cap is not None, "Camera not initialized"
            ret, frame = self.cap.read()

            if not ret:
                # Raise an error if there is no frame from the camera:
                raise RuntimeError("Failed to capture frame from camera.")
            return frame

        if path:
            # Ensure path is a string
            if not isinstance(path, str):
                raise TypeError(
                    f"Expected path to be a string, got {type(path).__name__}"
                )

            print(f"Loading image from {path}")

            # Raise an error if the path is invalide:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Image not found: {path}")

            # Read the image:
            self.image = cv2.imread(path)

            # Raise an error if the image exists, but the method failed to read it:
            if self.image is None:
                raise ValueError(f"Failed to read image: {path}")

            print("Image loaded successfully.")

            return self.image

        # Neither camera nor path provided:
        raise RuntimeError(
            "No input source provided: enable camera or provide an image path."
        )

    def release(self) -> None:
        """
        Release function to shut the camera down

        args: None

        return: None
        """

        if self.cap:
            self.cap.release()
            print("Camera released.")
