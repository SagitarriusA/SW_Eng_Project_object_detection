#!/usr/bin/env python3

"""
file: GUI.py
description: GUI to display the processed frame in the GUI and show the amount of different detected shapes
author: Bauer Ryoya, Walter Julian, Willmann York
date: 2025-10-12
version: 1.0
dependencies: OpenCV (cv2), os, sys, PyQt5.QtWidgets, PyQt5.QtGui, PyQt5.QtCore
classes: ImageProcessor
"""

import cv2
import os
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QImage, QPixmap, QKeyEvent
from PyQt5.QtCore import QTimer, Qt
from image_processing import ImageProcessor
from ShapeSpeaker import ShapeSpeaker


class GeometricObjectsGUI(QWidget):
    def __init__(self, processor=None, is_camera=False, image_list=None):
        super().__init__()
        self.processor = processor
        self.is_camera = is_camera
        self.image_list = image_list or []
        self.current_index = 0
        
        self.latest_shapes_count = {}
        self.speaker = ShapeSpeaker()

        # Window setup:
        self.setWindowTitle("Geometric Object Detection")
        self.resize(900, 700)
        self.setMinimumSize(300, 200)

        # Layout:
        layout = QVBoxLayout(self)
        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(0, 0)
        layout.addWidget(self.image_label)

        self.shapes_label = QLabel("Detected shapes: N/A")
        self.shapes_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.shapes_label)

        # Buttons:
        self.stop_button = QPushButton("Close application")
        self.stop_button.clicked.connect(self.close)
        layout.addWidget(self.stop_button)

        self.speak_button = QPushButton("Speak detected shapes")
        self.speak_button.clicked.connect(self.speak_detected_shapes)
        layout.addWidget(self.speak_button)

        self.next_button = QPushButton("Next Image")
        self.next_button.clicked.connect(self.next_image)
        if self.image_list:  # Show only if processing images
            layout.addWidget(self.next_button)

        # Timer for camera stream:
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Latest QPixmap:
        self.current_pixmap = None

        # Initialize first frame:
        if self.is_camera:
            if self.processor is None:
                self.processor = ImageProcessor(cam_device=0, image_path=None)
            self.timer.start(0)
            print("[INFO] Started camera stream.")
        elif self.image_list:
            self.load_image(self.image_list[self.current_index])

    # Core Methods:
    def load_image(self, path):
        try:
            processor = ImageProcessor(cam_device=None, image_path=path)
            frame, shapes_count = processor.process_frame(processor.get_frame())
            self.display_image(frame)
            self.update_shapes_label(shapes_count)
            self.latest_shapes_count = shapes_count
        except Exception as e:
            print(f"[ERROR] Failed to load {path}: {e}")

    def next_image(self):
        if not self.image_list:
            return
        self.current_index += 1
        if self.current_index >= len(self.image_list):
            print("[INFO] Reached end of images, looping back to first.")
            self.current_index = 0
        self.load_image(self.image_list[self.current_index])

    def speak_detected_shapes(self):
        if self.latest_shapes_count:
            self.speaker.speak(self.latest_shapes_count)
        else:
            print("[INFO] No shapes detected yet.")

    def update_frame(self):
        if not self.is_camera or self.processor is None:
            return
        self.timer.stop()
        frame = self.processor.get_frame()
        if frame is not None:
            processed, shapes_count = self.processor.process_frame(frame)
            self.display_image(processed)
            self.update_shapes_label(shapes_count)
            self.latest_shapes_count = shapes_count
        else:
            print("[WARN] No frame received from camera.")
        self.timer.start(0)

    # Display Methods:
    def display_image(self, frame):
        if frame is None:
            return
        try:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        except cv2.error as e:
            print(f"[ERROR] cvtColor failed: {e}")
            return
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.current_pixmap = QPixmap.fromImage(qt_image)
        self._update_label_pixmap()

    def _update_label_pixmap(self):
        if self.current_pixmap:
            self.image_label.setPixmap(
                self.current_pixmap.scaled(
                    self.image_label.width(),
                    self.image_label.height(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

    def update_shapes_label(self, shapes_count: dict):
        if not shapes_count:
            self.shapes_label.setText("Detected shapes: None")
        else:
            text = "Detected shapes: " + ", ".join(f"{name}: {count}" for name, count in shapes_count.items())
            self.shapes_label.setText(text)

    # Qt Event Overrides:
    def resizeEvent(self, event):
        self._update_label_pixmap()
        super().resizeEvent(event)

    def closeEvent(self, event):
        if self.is_camera and self.processor:
            self.timer.stop()
            self.processor.release()
        event.accept()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Q:
            self.close()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Geometric Objects Detection GUI")
    parser.add_argument("--camera", action="store_true", help="Use camera device 0")
    parser.add_argument("--images", action="store_true", help="Process all images in /images/")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "../images")
    app = QApplication(sys.argv)

    if args.camera:
        processor = ImageProcessor(cam_device=0, image_path=None)
        gui = GeometricObjectsGUI(processor=processor, is_camera=True)
    elif args.images:
        image_files = sorted([os.path.join(images_dir, f)
                              for f in os.listdir(images_dir)
                              if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))])
        if not image_files:
            print(f"[ERROR] No images found in {images_dir}")
            sys.exit(1)
        gui = GeometricObjectsGUI(image_list=image_files, is_camera=False)
    else:
        print("[ERROR] Please specify either --camera or --images")
        sys.exit(1)

    gui.show()
    sys.exit(app.exec_())
