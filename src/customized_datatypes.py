#!/usr/bin/env python3

"""
file: customized_datatypes.py
description: File to define all used dataclasses
dependencies: typing, dataclasses, numpy
classes: None
"""

from dataclasses import dataclass
from typing import Optional, Dict
import numpy as np


@dataclass
class LogMessage:
    shape: str
    color: str


@dataclass
class Frame:
    frame: Optional[np.ndarray] = None
    path: Optional[str] = None


@dataclass
class ProcessedFrame:
    image: np.ndarray
    shapes_count: Dict[str, int]


@dataclass
class Sources:
    cam_device: Optional[int] = None
    image_path: Optional[str] = None
