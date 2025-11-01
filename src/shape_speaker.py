#!/usr/bin/env python3

"""
file: shape_speaker.py
description: a file to convert the shape and color name to TTS and play it if recomended
author: Bauer Ryoya, Walter Julian, Willmann York
date: 2025-11-01
version: 1.2
changes: typo-changes according to Pylint, style changes
dependencies: __future__, os, sys, gtts, playsound, time
"""

from __future__ import annotations

import os
import warnings
from typing import Optional
from gtts import gTTS  # type: ignore

# Ignore the deprecation warning from pygame.pkgdata; no newer pygame version available till now:
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")

import pygame  # pylint: disable=wrong-import-position


# Converts detected shapes and colors into spoken audio using gTTS:
class ShapeSpeaker:
    """Class for the sound module"""

    def __init__(self, output_dir: str = "sounds", lang: str = "en") -> None:
        """
        Init function for the sound module

        arg: output_dir (str), lang str

        return: None
        """

        # Get absolute path to the script's directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Move one level up (project root)
        project_root = os.path.dirname(script_dir)
        # Place sounds folder inside project root
        self.output_dir = os.path.join(project_root, output_dir)
        self.lang = lang
        os.makedirs(self.output_dir, exist_ok=True)

    def _describe_shapes(self, shapes_count: dict) -> Optional[str]:
        """
        Private function to generate the string for the spoken output

        arg: shape_count (dict)

        return: text (str)
        """

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

    def _generate_speech(
        self, shapes_colors: dict, filename: str = "detected_shapes.mp3"
    ) -> Optional[str]:
        """
        Private function to convert the text to speech and save the file

        args: shape_colors (dict), filename (str)

        return: output_path (str)
        """

        # Generates an mp3 file describing the shapes and colors:
        text = self._describe_shapes(shapes_colors)

        if text is None:
            return None

        output_path = os.path.join(self.output_dir, filename)
        tts = gTTS(text=text, lang=self.lang)
        tts.save(output_path)
        print(f"[INFO] Audio saved to: {output_path}")
        return output_path

    def play_audio(self, filepath: Optional[str] = None) -> None:
        """
        Function to play the audio file

        args: filepath (str)

        return: None
        """

        # Check if the path is a string:
        assert isinstance(
            filepath, str
        ), f"Filepath must be a string, got {type(filepath)}"

        if not os.path.exists(filepath):
            print(f"[ERROR] File not found: {filepath}")
            return

        pygame.mixer.init()
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()

        # Wait until done
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()

    def speak(self, shapes_count: dict) -> None:
        """
        Function to handle the input, concvert it to speech and play it

        Args: shapes_count (dict)

        Return: None
        """

        # Generate and play audio for the shapes and colors:
        path = self._generate_speech(shapes_count)

        self.play_audio(path)


if __name__ == "__main__":
    # Example usage:
    detected = {"Triangle": 3, "Square": 1, "Circle": 5}

    speaker = ShapeSpeaker()
    speaker.speak(detected)
