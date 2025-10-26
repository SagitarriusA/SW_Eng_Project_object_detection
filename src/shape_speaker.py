#!/usr/bin/env python3

"""
file: shape_speaker.py
description: a file to convert the shape and color name to TTS and play it if recomended
author: Bauer Ryoya, Walter Julian, Willmann York
date: 2025-10-12
version: 1.0
dependencies: os, sys, gtts, playsound
"""

import os
import sys
from gtts import gTTS
from playsound import playsound


# Converts detected shapes and colors into spoken audio using gTTS:
class ShapeSpeaker:
    def __init__(self, output_dir="sounds", lang="en"):
        # Get absolute path to the script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Move one level up (project root)
        project_root = os.path.dirname(script_dir)
        # Place sounds folder inside project root
        self.output_dir = os.path.join(project_root, output_dir)
        self.lang = lang
        os.makedirs(self.output_dir, exist_ok=True)

    def describe_shapes(self, shapes_count: dict) -> str:
        # Takes a dict like and creates a descriptive sentence:
        if not shapes_count:
            return None

        descriptions = []
        for shape, count in shapes_count.items():
            descriptions.append(f"{count} {shape.lower()}")

        if len(descriptions) == 1:
            text = f"Detected {descriptions[0]}."
        else:
            text = (
                "Detected " + ", ".join(descriptions[:-1]) + f" and {descriptions[-1]}."
            )
        return text

    def generate_speech(self, shapes_colors: dict, filename="detected_shapes.mp3"):
        # Generates an mp3 file describing the shapes and colors:
        text = self.describe_shapes(shapes_colors)

        if text is None:
            return None

        output_path = os.path.join(self.output_dir, filename)
        tts = gTTS(text=text, lang=self.lang)
        tts.save(output_path)
        print(f"[INFO] Audio saved to: {output_path}")
        return output_path

    def play_audio(self, filepath: str):
        # Play the generated audio file:
        if not os.path.exists(filepath):
            print(f"[ERROR] File not found: {filepath}")
            return

        playsound(filepath)

    def speak(self, shapes_count: dict):
        # Generate and play audio for the shapes and colors:
        path = self.generate_speech(shapes_count)
        print(f"path: {path}")
        self.play_audio(path)


if __name__ == "__main__":
    # Example usage:
    detected = {"Triangle": 3, "Square": 1, "Circle": 5}

    speaker = ShapeSpeaker()
    speaker.speak(detected)
