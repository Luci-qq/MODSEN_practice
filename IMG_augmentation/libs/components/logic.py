from PIL import Image, ImageEnhance
import numpy as np

class ImageAugmentor:
    def __init__(self):
        pass
    
    def resize(self, image, width, height):
        img = Image.fromarray(image)
        img_resized = img.resize((width, height))
        return np.array(img_resized)
    
    def rotate(self, image, angle):
        img = Image.fromarray(image)
        img_rotated = img.rotate(angle)
        return np.array(img_rotated)
    
    def flip(self, image, horizontal=True, vertical=False):
        img = Image.fromarray(image)
        if horizontal and vertical:
            img_flipped = img.transpose(Image.ROTATE_180)
        elif horizontal:
            img_flipped = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif vertical:
            img_flipped = img.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            img_flipped = img
        return np.array(img_flipped)
    
    def add_noise(self, image, noise_type="gaussian"):
        if noise_type == "gaussian":
            row, col, ch = image.shape
            mean = 0
            var = 0.01
            sigma = var**0.5
            gauss = np.random.normal(mean, sigma, (row, col, ch))
            noisy = image + gauss.reshape(row, col, ch)
            return np.clip(noisy, 0, 255).astype(np.uint8)
        elif noise_type == "salt_pepper":
            s_vs_p = 0.5
            amount = 0.04
            out = np.copy(image)

            num_salt = np.ceil(amount * image.size * s_vs_p)
            coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
            out[coords[0], coords[1], :] = 1
            
            num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
            coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
            out[coords[0], coords[1], :] = 0
            return out
        else:
            return image
    
    def adjust_brightness_contrast(self, image, brightness=0, contrast=0):
        img = Image.fromarray(image)
        enhancer = ImageEnhance.Brightness(img)
        img_brightness = enhancer.enhance(1 + brightness / 100.0)
        
        enhancer = ImageEnhance.Contrast(img_brightness)
        img_contrast = enhancer.enhance(1 + contrast / 100.0)
        
        return np.array(img_contrast)
    
    def augment(self, image, operations):
        for operation in operations:
            if operation['type'] == 'resize':
                image = self.resize(image, operation['width'], operation['height'])
            elif operation['type'] == 'rotate':
                image = self.rotate(image, operation['angle'])
            elif operation['type'] == 'flip':
                image = self.flip(image, operation.get('horizontal', True), operation.get('vertical', False))
            elif operation['type'] == 'noise':
                image = self.add_noise(image, operation['noise_type'])
            elif operation['type'] == 'brightness_contrast':
                image = self.adjust_brightness_contrast(image, operation.get('brightness', 0), operation.get('contrast', 0))
        return image

