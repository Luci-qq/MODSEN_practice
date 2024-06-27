import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageDraw, ImageFont

class ImageProcessor:
    """
    A class to process images using OpenCV and PIL libraries.
    
    Attributes:
    -----------
    image : numpy.ndarray
        The image loaded into the class, stored in OpenCV format.
    pil_image : PIL.Image.Image
        The image loaded into the class, stored in PIL format.
    
    Methods:
    --------
    __init__(image):
        Initializes the class with an image file path or a numpy array.
    _update_pil_image():
        Updates the PIL image from the OpenCV image.
    resize(width, height):
        Resizes the image to the given width and height.
    crop(x, y, width, height):
        Crops the image from the given (x, y) position with the specified width and height.
    rotate(angle):
        Rotates the image by the given angle in degrees.
    flip(direction):
        Flips the image in the specified direction (0 - horizontal, 1 - vertical, -1 - both).
    adjust_brightness(factor):
        Adjusts the brightness of the image by the given factor.
    adjust_contrast(factor):
        Adjusts the contrast of the image by the given factor.
    adjust_saturation(factor):
        Adjusts the saturation of the image by the given factor.
    add_noise(mean=0, std=25):
        Adds Gaussian noise to the image with the specified mean and standard deviation.
    translate(x, y):
        Translates the image by the given x and y offsets.
    shear(shear_factor):
        Shears the image by the given shear factor.
    stretch(x_factor, y_factor):
        Stretches the image by the given factors along the x and y axes.
    random_crop(crop_width, crop_height):
        Crops a random portion of the image with the given width and height.
    add_text(text, position, font_size=32, color=(255, 255, 255)):
        Adds the specified text to the image at the given position with the specified font size and color.
    get_size():
        Returns a tuple (width, height) representing the size of the image.
    get_dimensions():
        Returns a dictionary containing the width, height, and number of channels of the image.
    save_image(file_or_buffer):
        Saves the image to a file or buffer.
    """
    
    def __init__(self, image):
        """
        Initializes the ImageProcessor with an image.
        
        Parameters:
        -----------
        image : str or numpy.ndarray
            If a string is provided, it is treated as the file path of the image to be loaded.
            If a numpy.ndarray is provided, it is treated as the image itself.
        """
        if isinstance(image, str):
            self.image = cv2.imread(image)
            self.pil_image = Image.open(image)
        else:
            self.image = image
            self.pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    def _update_pil_image(self):
        """
        Updates the PIL image from the current OpenCV image.
        """
        self.pil_image = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))

    def resize(self, width, height):
        """
        Resizes the image to the specified width and height.
        
        Parameters:
        -----------
        width : int
            The desired width of the resized image.
        height : int
            The desired height of the resized image.
        
        Returns:
        --------
        numpy.ndarray
            The resized image.
        """
        return cv2.resize(self.image, (width, height))

    def crop(self, x, y, width, height):
        """
        Crops the image from the specified (x, y) position with the given width and height.
        
        Parameters:
        -----------
        x : int
            The x-coordinate of the top-left corner of the crop rectangle.
        y : int
            The y-coordinate of the top-left corner of the crop rectangle.
        width : int
            The width of the crop rectangle.
        height : int
            The height of the crop rectangle.
        
        Returns:
        --------
        numpy.ndarray
            The cropped image.
        """
        return self.image[y:y+height, x:x+width]

    def rotate(self, angle):
        """
        Rotates the image by the specified angle.
        
        Parameters:
        -----------
        angle : float
            The angle by which to rotate the image in degrees.
        
        Returns:
        --------
        numpy.ndarray
            The rotated image.
        """
        rows, cols = self.image.shape[:2]
        M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
        return cv2.warpAffine(self.image, M, (cols, rows))

    def flip(self, direction):
        """
        Flips the image in the specified direction.
        
        Parameters:
        -----------
        direction : int
            The direction in which to flip the image (0 - horizontal, 1 - vertical, -1 - both).
        
        Returns:
        --------
        numpy.ndarray
            The flipped image.
        """
        return cv2.flip(self.image, direction)

    def adjust_brightness(self, factor):
        """
        Adjusts the brightness of the image by the given factor.
        
        Parameters:
        -----------
        factor : float
            The factor by which to adjust the brightness (1.0 - no change, <1.0 - darker, >1.0 - brighter).
        
        Returns:
        --------
        numpy.ndarray
            The brightness-adjusted image.
        """
        self._update_pil_image()
        enhancer = ImageEnhance.Brightness(self.pil_image)
        enhanced_image = enhancer.enhance(factor)
        self.image = cv2.cvtColor(np.array(enhanced_image), cv2.COLOR_RGB2BGR)
        return self.image

    def adjust_contrast(self, factor):
        """
        Adjusts the contrast of the image by the given factor.
        
        Parameters:
        -----------
        factor : float
            The factor by which to adjust the contrast (1.0 - no change, <1.0 - less contrast, >1.0 - more contrast).
        
        Returns:
        --------
        numpy.ndarray
            The contrast-adjusted image.
        """
        self._update_pil_image()
        enhancer = ImageEnhance.Contrast(self.pil_image)
        enhanced_image = enhancer.enhance(factor)
        self.image = cv2.cvtColor(np.array(enhanced_image), cv2.COLOR_RGB2BGR)
        return self.image

    def adjust_saturation(self, factor):
        """
        Adjusts the saturation of the image by the given factor.
        
        Parameters:
        -----------
        factor : float
            The factor by which to adjust the saturation (1.0 - no change, <1.0 - less saturation, >1.0 - more saturation).
        
        Returns:
        --------
        numpy.ndarray
            The saturation-adjusted image.
        """
        self._update_pil_image()
        enhancer = ImageEnhance.Color(self.pil_image)
        enhanced_image = enhancer.enhance(factor)
        self.image = cv2.cvtColor(np.array(enhanced_image), cv2.COLOR_RGB2BGR)
        return self.image

    def add_noise(self, mean=0, std=25):
        """
        Adds Gaussian noise to the image.
        
        Parameters:
        -----------
        mean : float, optional
            The mean of the Gaussian noise (default is 0).
        std : float, optional
            The standard deviation of the Gaussian noise (default is 25).
        
        Returns:
        --------
        numpy.ndarray
            The image with added Gaussian noise.
        """
        noise = np.random.normal(mean, std, self.image.shape).astype(np.uint8)
        return cv2.add(self.image, noise)

    def translate(self, x, y):
        """
        Translates the image by the specified x and y offsets.
        
        Parameters:
        -----------
        x : int
            The number of pixels to shift the image along the x-axis.
        y : int
            The number of pixels to shift the image along the y-axis.
        
        Returns:
        --------
        numpy.ndarray
            The translated image.
        """
        M = np.float32([[1, 0, x], [0, 1, y]])
        return cv2.warpAffine(self.image, M, (self.image.shape[1], self.image.shape[0]))

    def shear(self, shear_factor):
        """
        Shears the image by the specified shear factor.
        
        Parameters:
        -----------
        shear_factor : float
            The factor by which to shear the image.
        
        Returns:
        --------
        numpy.ndarray
            The sheared image.
        """
        rows, cols = self.image.shape[:2]
        M = np.float32([[1, shear_factor, 0], [0, 1, 0]])
        return cv2.warpAffine(self.image, M, (int(cols+rows*shear_factor), rows))

    def stretch(self, x_factor, y_factor):
        """
        Stretches the image by the specified factors along the x and y axes.
        
        Parameters:
        -----------
        x_factor : float
            The factor by which to stretch the image along the x-axis.
        y_factor : float
            The factor by which to stretch the image along the y-axis.
        
        Returns:
        --------
        numpy.ndarray
            The stretched image.
        """
        return cv2.resize(self.image, None, fx=x_factor, fy=y_factor)

    def random_crop(self, crop_width, crop_height):
        """
        Crops a random portion of the image with the specified width and height.
        
        Parameters:
        -----------
        crop_width : int
            The width of the crop rectangle.
        crop_height : int
            The height of the crop rectangle.
        
        Returns:
        --------
        numpy.ndarray
            The randomly cropped image.
        """
        height, width = self.image.shape[:2]
        x = np.random.randint(0, width - crop_width)
        y = np.random.randint(0, height - crop_height)
        return self.image[y:y+crop_height, x:x+crop_width]

    def add_text(self, text, position, font_size=32, color=(255, 255, 255)):
        """
        Adds the specified text to the image.
        
        Parameters:
        -----------
        text : str
            The text to add to the image.
        position : tuple
            The (x, y) position at which to add the text.
        font_size : int, optional
            The font size of the text (default is 32).
        color : tuple, optional
            The color of the text in (R, G, B) format (default is white).
        
        Returns:
        --------
        numpy.ndarray
            The image with the added text.
        """
        img_pil = Image.fromarray(self.image)
        draw = ImageDraw.Draw(img_pil)
        font = ImageFont.truetype("arial.ttf", font_size)
        draw.text(position, text, font=font, fill=color)
        return np.array(img_pil)

    def get_size(self):
        """
        Returns the size of the image.
        
        Returns:
        --------
        tuple
            A tuple (width, height) representing the size of the image.
        """
        return self.image.shape[1], self.image.shape[0]

    def get_dimensions(self):
        """
        Returns the dimensions of the image.
        
        Returns:
        --------
        dict
            A dictionary containing the width, height, and number of channels of the image.
        """
        height, width = self.image.shape[:2]
        return {
            'width': width,
            'height': height,
            'channels': self.image.shape[2] if len(self.image.shape) > 2 else 1
        }

    def save_image(self, file_or_buffer):
        """
        Saves the image to a file or buffer.
        
        Parameters:
        -----------
        file_or_buffer : str or file-like object
            If a string is provided, it is treated as the file path to save the image.
            If a file-like object is provided, the image is saved to the buffer.
        """
        if isinstance(file_or_buffer, str):
            cv2.imwrite(file_or_buffer, self.image)
        else:
            _, buffer = cv2.imencode('.jpg', self.image)
            file_or_buffer.write(buffer)
