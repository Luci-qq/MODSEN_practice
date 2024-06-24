import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFont

class ImageProcessor:
    def __init__(self, image_path):
        # Инициализация класса с загрузкой изображения
        self.image = cv2.imread(image_path)
        self.pil_image = Image.open(image_path)

    def resize(self, width, height):
        # Изменение размера изображения до заданной ширины и высоты
        return cv2.resize(self.image, (width, height))

    def crop(self, x, y, width, height):
        # Обрезка изображения, начиная с координат (x, y) до заданной ширины и высоты
        return self.image[y:y+height, x:x+width]

    def rotate(self, angle):
        # Поворот изображения на заданный угол
        rows, cols = self.image.shape[:2]
        M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
        return cv2.warpAffine(self.image, M, (cols, rows))

    def flip(self, direction):
        # Отражение изображения (0 - по горизонтали, 1 - по вертикали, -1 - оба)
        return cv2.flip(self.image, direction)

    def adjust_brightness(self, factor):
        # Изменение яркости изображения (factor > 1 увеличивает, < 1 уменьшает)
        enhancer = ImageEnhance.Brightness(self.pil_image)
        return np.array(enhancer.enhance(factor))

    def adjust_contrast(self, factor):
        # Изменение контрастности изображения (factor > 1 увеличивает, < 1 уменьшает)
        enhancer = ImageEnhance.Contrast(self.pil_image)
        return np.array(enhancer.enhance(factor))

    def adjust_saturation(self, factor):
        # Изменение насыщенности изображения (factor > 1 увеличивает, < 1 уменьшает)
        enhancer = ImageEnhance.Color(self.pil_image)
        return np.array(enhancer.enhance(factor))

    def add_noise(self, mean=0, std=25):
        # Добавление гауссовского шума к изображению
        noise = np.random.normal(mean, std, self.image.shape).astype(np.uint8)
        return cv2.add(self.image, noise)

    def translate(self, x, y):
        # Сдвиг изображения на x пикселей по горизонтали и y по вертикали
        M = np.float32([[1, 0, x], [0, 1, y]])
        return cv2.warpAffine(self.image, M, (self.image.shape[1], self.image.shape[0]))

    def shear(self, shear_factor):
        # Наклон изображения на заданный коэффициент
        rows, cols = self.image.shape[:2]
        M = np.float32([[1, shear_factor, 0], [0, 1, 0]])
        return cv2.warpAffine(self.image, M, (int(cols+rows*shear_factor), rows))

    def stretch(self, x_factor, y_factor):
        # Растяжение изображения по горизонтали (x_factor) и вертикали (y_factor)
        return cv2.resize(self.image, None, fx=x_factor, fy=y_factor)

    def random_crop(self, crop_width, crop_height):
        # Случайная вырезка части изображения заданного размера
        height, width = self.image.shape[:2]
        x = np.random.randint(0, width - crop_width)
        y = np.random.randint(0, height - crop_height)
        return self.image[y:y+crop_height, x:x+crop_width]

    def add_text(self, text, position, font_size=32, color=(255, 255, 255)):
        # Наложение текста на изображение
        img_pil = Image.fromarray(self.image)
        draw = ImageDraw.Draw(img_pil)
        font = ImageFont.truetype("arial.ttf", font_size)
        draw.text(position, text, font=font, fill=color)
        return np.array(img_pil)