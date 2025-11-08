#!/usr/bin/env python3

"""
file: load_sources.py
description: File to read the given sources (cam or images)
dependencies: os, typing, cv2, numpy
classes: customized_datatypes
"""

import os
from typing import Optional
import cv2
import numpy as np
from customized_datatypes import Sources, Frame


class LoadSources:
    """Setup the class for loading sources"""

    def __init__(
        self, valid_sources: Sources
    ) -> None:
        """
        Function to init the class
        
        Args: valid_sources.cam_device (Optional[int]), valid_sources.image_path (Optional[str])
        
        Return: None
        """

        self.cam_device: Optional[int] = valid_sources.cam_device
        self.image_path = Frame(path=valid_sources.image_path)
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

    def load_frame(self, data: Frame) -> Frame:
        """
        Function to load the current frame of the camera or to load the frame from the given path

        Args: data: Frame

        Return: Frame
        """

        # Get a single frame from camera or the loaded image:
        if self.is_camera:
            # Check if self.cap is not None to be sure that the camera is initalized:
            assert self.cap is not None, "Camera not initialized"
            ret, frame = self.cap.read()

            if not ret:
                # Raise an error if there is no frame from the camera:
                raise RuntimeError("Failed to capture frame from camera.")
            return Frame(frame=frame)

        if data.path:
            if not isinstance(data.path, str):
                raise TypeError(f"Expected 'path' to be a string, got {type(data.path).__name__}")

            if not os.path.exists(data.path):
                raise FileNotFoundError(f"Image not found: {data.path}")

            print(f"Loading image from {data.path}")

            # Read the image:
            self.image = cv2.imread(data.path)

            # Raise an error if the image exists, but the method failed to read it:
            if self.image is None:
                raise ValueError(f"Failed to read image: {data.path}")

            print("Image loaded successfully.")

            return Frame(frame=self.image, path=data.path)

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
