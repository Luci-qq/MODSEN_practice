# tests/test_setup.py

import unittest
from unittest.mock import Mock, patch
import sys
import os
import cv2
import numpy as np
from PIL import Image
import io


# Adding root dir to the sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from libs.components.logic.ImageProcessor import ImageProcessor
from libs.screens.controllers.MainScreenController import MainScreenController, IMAGE_EXTENSIONS, TEMP_IMAGE_PATH, AUGMENTED_DIR
from libs.components.ui.TreeViewLabels import FileTreeViewLabel, FolderTreeViewLabel

