#!/usr/bin/env python3

"""
file: gui.py
description: GUI to display the processed frame in the GUI and the amount of detected shapes
author: Bauer Ryoya, Walter Julian, Willmann York
date: 2025-11-1
version: 1.2
changes: typo-changes according to Pylint
dependencies: OpenCV (cv2), os, sys, PyQt5.QtWidgets, PyQt5.QtGui, PyQt5.QtCore, argparse
classes: ImageProcessor
"""

import os
import sys
import argparse
from typing import Optional, List, Dict
import numpy as np
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QImage, QPixmap, QKeyEvent
from PyQt5.QtCore import QTimer, Qt
from image_processing import ImageProcessor
from shape_speaker import ShapeSpeaker


class ImageDisplayWidget(QWidget):
    """Displays processed images and shape labels."""

    def __init__(self) -> None:
        """
        Init function for the class to display the widget

        Args: None

        Return: None
        """

        super().__init__()
        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignCenter)  # type: ignore
        self.shapes_label = QLabel("Detected shapes: N/A")
        self.shapes_label.setAlignment(Qt.AlignCenter)  # type: ignore
        self.current_pixmap: Optional[QPixmap] = None

        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        layout.addWidget(self.shapes_label)

    def display_image(self, frame: np.ndarray) -> None:
        """
        Displays an OpenCV image as QPixmap

        Args: frame (nDArray)

        Return: None
        """

        if frame is None:
            return
        try:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except cv2.error as e:  # pylint: disable=catching-non-exception
            print(f"[ERROR] cvtColor failed: {e}")
            return
        h, w, ch = rgb.shape
        qt_img = QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888)
        self.current_pixmap = QPixmap.fromImage(qt_img)
        self._update_pixmap()

    def _update_pixmap(self) -> None:
        """
        Private function to update the pixmap

        Args: None

        Return: None
        """

        if self.current_pixmap:
            self.image_label.setPixmap(
                self.current_pixmap.scaled(
                    self.image_label.width(),
                    self.image_label.height(),
                    Qt.KeepAspectRatio,  # type: ignore
                    Qt.SmoothTransformation,  # type: ignore
                )
            )

    def update_shapes_label(self, shapes_count: dict) -> None:
        """
        Function to update the label for the shapes

        Args: shapes_count ()"""
        if not shapes_count:
            self.shapes_label.setText("Detected shapes: None")
        else:
            text = "Detected shapes: " + ", ".join(
                f"{name}: {count}" for name, count in shapes_count.items()
            )
            self.shapes_label.setText(text)

    def resizeEvent(self, event) -> None:
        """
        Function for the resize event

        Args: event

        Return: None
        """

        self._update_pixmap()
        super().resizeEvent(event)


class ControlPanel(QWidget):
    """Class to setup the control panel for the GUI"""

    def __init__(self, gui_ref):
        """
        Init function to setup the class for the control panel

        Args: gui_ref

        Return: None
        """

        super().__init__()
        self.gui = gui_ref

        self.stop_button = QPushButton("Close application")
        self.stop_button.clicked.connect(self.gui.close)

        self.speak_button = QPushButton("Speak detected shapes")
        self.speak_button.clicked.connect(self._speak_shapes)

        self.next_button = QPushButton("Next Image")
        self.next_button.clicked.connect(self._next_image)

        layout = QVBoxLayout(self)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.speak_button)
        layout.addWidget(self.next_button)

        if not self.gui.image_list:
            self.next_button.hide()

    def _speak_shapes(self) -> None:
        """
        Private function to convert the detected shapes to speech
        with the class for the audio module

        Args: None

        Return: None
        """

        if self.gui.latest_shapes_count:
            self.gui.speaker.speak(self.gui.latest_shapes_count)
        else:
            print("[INFO] No shapes detected yet.")

    def _next_image(self):
        """
        Private function to call the next image

        Args: None

        Return: None
        """

        self.gui.next_image()


class GeometricObjectsGui(QWidget):
    """Main application window"""

    def __init__(
        self,
        processor: Optional[ImageProcessor] = None,
        is_camera: bool = False,
        image_list: Optional[List[str]] = None,
    ) -> None:
        """
        Init function for the Geometric Objejcts GUI class

        Args: processor (ImageProcessor), is_camera (Bool), image_list (List[str])

        Return: None
        """

        super().__init__()

        self.processor = processor
        self.is_camera = is_camera
        self.image_list = image_list or []
        self.current_index = 0
        self.latest_shapes_count: Dict[str, int] = {}
        self.speaker = ShapeSpeaker()

        self.setWindowTitle("Geometric Object Detection")
        self.resize(900, 700)
        self.setMinimumSize(300, 200)

        self.display = ImageDisplayWidget()
        self.controls = ControlPanel(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.display)
        layout.addWidget(self.controls)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Initialization:
        if self.is_camera:
            self.timer.start(0)
            print("[INFO] Started camera stream.")
        elif self.image_list:
            self.load_image(self.image_list[self.current_index])

    def load_image(self, path: str) -> None:
        """
        Function to load the images from the path

        Args: path (str)

        Return: None
        """

        try:
            processor = ImageProcessor(cam_device=None, image_path=path)
            frame: Optional[np.ndarray] = processor.get_frame()
            assert isinstance(
                frame, np.ndarray
            ), f"Expected an ndarray, got {type(frame)}"

            frame, shapes_count = processor.process_frame(frame)
            self.display.display_image(frame)
            self.display.update_shapes_label(shapes_count)
            self.latest_shapes_count = shapes_count
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"[ERROR] Failed to load {path}: {e}")

    def next_image(self):
        """
        Function to select the next image if the botton get's hit

        Args: None

        Return: None
        """

        if not self.image_list:
            return

        self.current_index = (self.current_index + 1) % len(self.image_list)
        self.load_image(self.image_list[self.current_index])

    def update_frame(self) -> None:
        """
        Function to update the frame

        Args: None

        Return: None
        """

        if not self.is_camera or not self.processor:
            return

        self.timer.stop()
        frame = self.processor.get_frame()

        if frame is not None:
            processed, shapes_count = self.processor.process_frame(frame)
            self.display.display_image(processed)
            self.display.update_shapes_label(shapes_count)
            self.latest_shapes_count = shapes_count
        else:
            print("[WARN] No frame received from camera.")
        self.timer.start(0)

    def closeEvent(self, event) -> None:
        """
        Function to handle the close event

        Args: event

        Return: None
        """

        if self.is_camera and self.processor:
            self.timer.stop()
            self.processor.release()
        event.accept()

    def keyPressEvent(self, event: Optional[QKeyEvent]) -> None:
        """
        Function to hande the q key as close event

        Args: event (QKeyEvent)

        Return: None
        """

        if event and event.key() == Qt.Key_Q:  # type: ignore[attr-defined]
            self.close()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    # Setup the parser for the console input:
    parser = argparse.ArgumentParser(description="Geometric Objects Detection GUI")
    parser.add_argument("--camera", action="store_true", help="Use camera device 0")
    parser.add_argument(
        "--images", action="store_true", help="Process all images in /images/"
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "../images")
    app = QApplication(sys.argv)

    if args.camera:
        proc = ImageProcessor(cam_device=0, image_path=None)
        gui = GeometricObjectsGui(processor=proc, is_camera=True)
    elif args.images:
        image_files = sorted(
            [
                os.path.join(images_dir, f)
                for f in os.listdir(images_dir)
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))
            ]
        )
        if not image_files:
            print(f"[ERROR] No images found in {images_dir}")
            sys.exit(1)
        gui = GeometricObjectsGui(image_list=image_files, is_camera=False)
    else:
        print("[ERROR] Please specify either --camera or --images")
        sys.exit(1)

    gui.show()
    sys.exit(app.exec_())
