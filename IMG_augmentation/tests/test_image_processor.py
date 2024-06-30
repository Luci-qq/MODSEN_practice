import os
import sys
import io
import numpy as np
import cv2
import unittest
from unittest.mock import Mock, patch

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from libs.components.logic.ImageProcessor import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        # Создаем тестовое изображение как массив NumPy
        self.test_image = np.ones((100, 100, 3), dtype=np.uint8) * 255
        self.processor = ImageProcessor(self.test_image)

    def test_resize(self):
        resized = self.processor.resize(50, 50)
        self.assertEqual(resized.shape, (50, 50, 3))

    def test_crop(self):
        cropped = self.processor.crop(10, 10, 50, 50)
        self.assertEqual(cropped.shape, (50, 50, 3))

    def test_rotate(self):
        rotated = self.processor.rotate(45)
        self.assertEqual(rotated.shape, self.processor.image.shape)

    def test_flip(self):
        flipped = self.processor.flip(1)
        self.assertEqual(flipped.shape, self.processor.image.shape)

    def test_adjust_brightness(self):
        brightened = self.processor.adjust_brightness(1.5)
        self.assertEqual(brightened.shape, self.processor.image.shape)

    def test_adjust_contrast(self):
        contrasted = self.processor.adjust_contrast(1.5)
        self.assertEqual(contrasted.shape, self.processor.image.shape)

    def test_adjust_saturation(self):
        saturated = self.processor.adjust_saturation(1.5)
        self.assertEqual(saturated.shape, self.processor.image.shape)

    def test_add_noise(self):
        noisy = self.processor.add_noise()
        self.assertEqual(noisy.shape, self.processor.image.shape)

    def test_translate(self):
        translated = self.processor.translate(10, 10)
        self.assertEqual(translated.shape, self.processor.image.shape)

    def test_shear(self):
        sheared = self.processor.shear(0.5)
        self.assertNotEqual(sheared.shape, self.processor.image.shape)

    def test_stretch(self):
        stretched = self.processor.stretch(1.5, 1.5)
        self.assertNotEqual(stretched.shape, self.processor.image.shape)

    def test_random_crop(self):
        random_cropped = self.processor.random_crop(50, 50)
        self.assertEqual(random_cropped.shape, (50, 50, 3))

    def test_add_text(self):
        with_text = self.processor.add_text("Test", (10, 10))
        self.assertEqual(with_text.shape, self.processor.image.shape)

    def test_get_size(self):
        size = self.processor.get_size()
        self.assertEqual(size, (100, 100))

    def test_get_dimensions(self):
        dimensions = self.processor.get_dimensions()
        self.assertEqual(dimensions, {'width': 100, 'height': 100, 'channels': 3})

    def test_save_image(self):
        # Создаем буфер в памяти для сохранения изображения
        buffer = io.BytesIO()
        self.processor.save_image(buffer)
        buffer.seek(0)
        
        # Проверяем, что изображение было сохранено корректно
        saved_image = cv2.imdecode(np.frombuffer(buffer.getvalue(), np.uint8), cv2.IMREAD_UNCHANGED)
        self.assertEqual(saved_image.shape, self.test_image.shape)

if __name__ == '__main__':
    unittest.main()

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        # Создаем тестовое изображение как массив NumPy
        self.test_image = np.ones((100, 100, 3), dtype=np.uint8) * 255
        self.processor = ImageProcessor(self.test_image)

    def test_resize(self):
        resized = self.processor.resize(50, 50)
        self.assertEqual(resized.shape, (50, 50, 3))

    def test_crop(self):
        cropped = self.processor.crop(10, 10, 50, 50)
        self.assertEqual(cropped.shape, (50, 50, 3))

    def test_rotate(self):
        rotated = self.processor.rotate(45)
        self.assertEqual(rotated.shape, self.processor.image.shape)

    def test_flip(self):
        flipped = self.processor.flip(1)
        self.assertEqual(flipped.shape, self.processor.image.shape)

    def test_adjust_brightness(self):
        brightened = self.processor.adjust_brightness(1.5)
        self.assertEqual(brightened.shape, self.processor.image.shape)

    def test_adjust_contrast(self):
        contrasted = self.processor.adjust_contrast(1.5)
        self.assertEqual(contrasted.shape, self.processor.image.shape)

    def test_adjust_saturation(self):
        saturated = self.processor.adjust_saturation(1.5)
        self.assertEqual(saturated.shape, self.processor.image.shape)

    def test_add_noise(self):
        noisy = self.processor.add_noise()
        self.assertEqual(noisy.shape, self.processor.image.shape)

    def test_translate(self):
        translated = self.processor.translate(10, 10)
        self.assertEqual(translated.shape, self.processor.image.shape)

    def test_shear(self):
        sheared = self.processor.shear(0.5)
        self.assertNotEqual(sheared.shape, self.processor.image.shape)

    def test_stretch(self):
        stretched = self.processor.stretch(1.5, 1.5)
        self.assertNotEqual(stretched.shape, self.processor.image.shape)

    def test_random_crop(self):
        random_cropped = self.processor.random_crop(50, 50)
        self.assertEqual(random_cropped.shape, (50, 50, 3))

    def test_add_text(self):
        with_text = self.processor.add_text("Test", (10, 10))
        self.assertEqual(with_text.shape, self.processor.image.shape)

    def test_get_size(self):
        size = self.processor.get_size()
        self.assertEqual(size, (100, 100))

    def test_get_dimensions(self):
        dimensions = self.processor.get_dimensions()
        self.assertEqual(dimensions, {'width': 100, 'height': 100, 'channels': 3})

    def test_save_image(self):
        # Создаем буфер в памяти для сохранения изображения
        buffer = io.BytesIO()
        self.processor.save_image(buffer)
        buffer.seek(0)
        
        # Проверяем, что изображение было сохранено корректно
        saved_image = cv2.imdecode(np.frombuffer(buffer.getvalue(), np.uint8), cv2.IMREAD_UNCHANGED)
        self.assertEqual(saved_image.shape, self.test_image.shape)

if __name__ == '__main__':
    unittest.main()