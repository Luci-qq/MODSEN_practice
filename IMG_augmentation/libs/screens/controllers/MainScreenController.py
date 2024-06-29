import os
import logging
from typing import Optional
from libs.components.logic.ImageProcessor import ImageProcessor
from libs.components.ui.TreeViewLabels import FileTreeViewLabel, FolderTreeViewLabel

# Logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
TEMP_IMAGE_PATH = 'temp_image.png'
AUGMENTED_DIR = 'augmented'

class MainScreenController:
    """
    Controller class for managing the main screen functionality of the image processing application.

    This class handles user interactions, file management, image processing operations,
    and updates to the user interface.

    Attributes:
        view: The view object representing the main screen UI.
        image_processor (Optional[ImageProcessor]): An instance of ImageProcessor for image manipulations.
        original_image_path (Optional[str]): The file path of the original image being processed.
    """

    def __init__(self, view):
        """
        Initialize the MainScreenController.

        Args:
            view: The view object representing the main screen UI.
        """
        self.view = view
        self.image_processor: Optional[ImageProcessor] = None
        self.original_image_path: Optional[str] = None
        logger.info("MainScreenController initialized")

    def add_file(self):
        """
        Initiate the process of adding a single file to the application.
        """
        logger.debug("Adding file")
        self._show_file_manager(select_dir=False, selector='file')

    def add_folder(self):
        """
        Initiate the process of adding a folder to the application.
        """
        logger.debug("Adding folder")
        self._show_file_manager(select_dir=True, selector='folder')

    def _show_file_manager(self, select_dir: bool, selector: str):
        """
        Display the file manager for selecting files or folders.

        Args:
            select_dir (bool): If True, allows directory selection. If False, allows file selection.
            selector (str): The type of selection ('file' or 'folder').
        """
        try:
            self.view.file_manager.show('/')
            self.view.file_manager.select_dir = select_dir
            self.view.file_manager.selector = selector
            logger.debug(f"File manager shown with select_dir={select_dir}, selector={selector}")
        except Exception as e:
            logger.error(f"Error showing file manager: {str(e)}")

    def delete_selected(self):
        """
        Delete the currently selected node from the tree view.
        """
        try:
            selected_node = self.view.treeview.selected_node
            if selected_node:
                self.view.treeview.remove_node(selected_node)
                logger.info(f"Deleted node: {selected_node}")
                if self.view.current_image and self.view.current_image.source == selected_node.file_path:
                    self.clear_displayed_image()
            else:
                logger.warning("No node selected for deletion")
        except Exception as e:
            logger.error(f"Error deleting selected node: {str(e)}")

    def clear_displayed_image(self):
        """
        Clear the currently displayed image and reset related attributes.
        """
        try:
            self.view.clear_displayed_image()
            self.image_processor = None
            if os.path.exists(TEMP_IMAGE_PATH):
                os.remove(TEMP_IMAGE_PATH)
            self.update_image_size_labels()
            logger.info("Displayed image cleared")
        except Exception as e:
            logger.error(f"Error clearing displayed image: {str(e)}")

    def select_path(self, path: str):
        """
        Process the selected file or folder path.

        Args:
            path (str): The selected file or folder path.
        """
        try:
            self.view.exit_manager()
            if os.path.isdir(path):
                self.add_directory_to_tree(path, self.view.treeview.root)
                logger.info(f"Added directory to tree: {path}")
            elif self._is_image(path):
                node = FileTreeViewLabel(text=os.path.basename(path), file_path=path)
                self.view.treeview.add_node(node)
                logger.info(f"Added file to tree: {path}")
            else:
                logger.warning(f"Selected path is neither a directory nor an image: {path}")
        except Exception as e:
            logger.error(f"Error processing selected path: {str(e)}")

    def add_directory_to_tree(self, path: str, parent_node):
        """
        Recursively add a directory and its contents to the tree view.

        Args:
            path (str): The directory path to add.
            parent_node: The parent node in the tree view.
        """
        try:
            dir_node = self.view.treeview.add_node(FolderTreeViewLabel(text=os.path.basename(path)), parent_node)
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path) and self._is_image(item_path):
                    self.view.treeview.add_node(FileTreeViewLabel(text=item, file_path=item_path), dir_node)
                elif os.path.isdir(item_path):
                    self.add_directory_to_tree(item_path, dir_node)
            logger.debug(f"Added directory contents to tree: {path}")
        except Exception as e:
            logger.error(f"Error adding directory to tree: {str(e)}")

    @staticmethod
    def _is_image(file_path: str) -> bool:
        """
        Check if the given file path is an image.

        Args:
            file_path (str): The file path to check.

        Returns:
            bool: True if the file is an image, False otherwise.
        """
        return any(file_path.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)

    def on_treeview_select(self, instance, value):
        """
        Handle the selection of a node in the tree view.

        Args:
            instance: The instance of the tree view.
            value: The selected node.
        """
        try:
            if isinstance(value, FileTreeViewLabel) and self._is_image(value.file_path):
                self.display_image(value.file_path)
            else:
                self.clear_displayed_image()
        except Exception as e:
            logger.error(f"Error handling treeview selection: {str(e)}")

    def display_image(self, file_path: str):
        """
        Display the selected image and initialize the image processor.

        Args:
            file_path (str): The file path of the image to display.
        """
        try:
            self.original_image_path = file_path
            self.view.display_image(file_path)
            self.image_processor = ImageProcessor(file_path)
            self.update_image_size_labels()
            logger.info(f"Displayed image: {file_path}")
        except Exception as e:
            logger.error(f"Error displaying image: {str(e)}")

    def update_image_size_labels(self):
        """
        Update the image size labels in the UI.
        """
        try:
            if self.image_processor:
                dimensions = self.image_processor.get_dimensions()
                self.view.ids.image_layout.height_label.text = f"IMG_Height: {dimensions['height']}"
                self.view.ids.image_layout.width_label.text = f"IMG_Width: {dimensions['width']}"
            else:
                self.view.ids.image_layout.height_label.text = 'IMG_Height: N/A'
                self.view.ids.image_layout.width_label.text = 'IMG_Width: N/A'
        except Exception as e:
            logger.error(f"Error updating image size labels: {str(e)}")

    def save_image(self):
        """
        Save the processed image to a unique file in the augmented directory.
        """
        try:
            if not self.image_processor or not self.original_image_path:
                logger.warning("No image to save or original image path not found")
                return

            augmented_dir = os.path.join(os.getcwd(), AUGMENTED_DIR)
            os.makedirs(augmented_dir, exist_ok=True)
            
            original_filename = os.path.basename(self.original_image_path)
            save_path = self._get_unique_save_path(augmented_dir, original_filename)
            
            self.image_processor.save_image(save_path)
            logger.info(f"Image saved as {save_path}")
            self.view.update_image_source(save_path)

            if os.path.exists(TEMP_IMAGE_PATH):
                os.remove(TEMP_IMAGE_PATH)
        except Exception as e:
            logger.error(f"Error saving image: {str(e)}")

    @staticmethod
    def _get_unique_save_path(directory: str, filename: str) -> str:
        """
        Generate a unique file path for saving an image.

        Args:
            directory (str): The directory to save the file in.
            filename (str): The original filename.

        Returns:
            str: A unique file path for saving the image.
        """
        base, ext = os.path.splitext(filename)
        counter = 1
        save_path = os.path.join(directory, filename)
        while os.path.exists(save_path):
            save_path = os.path.join(directory, f"{base}_{counter}{ext}")
            counter += 1
        return save_path

    def crop_image(self, width: int, height: int):
        """
        Crop the image to the specified dimensions.

        Args:
            width (int): The desired width of the cropped image.
            height (int): The desired height of the cropped image.
        """
        try:
            if self.image_processor:
                left = (self.image_processor.image.shape[1] - width) // 2
                top = (self.image_processor.image.shape[0] - height) // 2
                self.image_processor.image = self.image_processor.crop(left, top, width, height)
                logger.info(f"Image cropped to {width}x{height}")
            else:
                logger.warning("No image processor available for cropping")
        except Exception as e:
            logger.error(f"Error cropping image: {str(e)}")

    def rotate_image(self, angle: float):
        """
        Rotate the image by the specified angle.

        Args:
            angle (float): The angle of rotation in degrees.
        """
        try:
            if self.image_processor:
                rotated_image = self.image_processor.rotate(angle)
                self._update_displayed_image(rotated_image)
                logger.info(f"Image rotated by {angle} degrees")
            else:
                logger.warning("No image processor available for rotation")
        except Exception as e:
            logger.error(f"Error rotating image: {str(e)}")

    def adjust_contrast(self, contrast_factor: float = 0, brightness_factor: float = 0):
        """
        Adjust the contrast and brightness of the image.

        Args:
            contrast_factor (float): The factor to adjust contrast. Default is 0.
            brightness_factor (float): The factor to adjust brightness. Default is 0.
        """
        try:
            if self.image_processor:
                image = self.image_processor.adjust_contrast(contrast_factor)
                image = self.image_processor.adjust_brightness(brightness_factor)
                self._update_displayed_image(image)
                logger.info(f"Image contrast adjusted by {contrast_factor}, brightness by {brightness_factor}")
            else:
                logger.warning("No image processor available for contrast adjustment")
        except Exception as e:
            logger.error(f"Error adjusting image contrast: {str(e)}")

    def _update_displayed_image(self, image):
        """
        Update the displayed image in the UI.

        Args:
            image: The new image to display.
        """
        try:
            self.image_processor.save_image(TEMP_IMAGE_PATH)
            self.view.update_image_source(TEMP_IMAGE_PATH)
            self.update_image_size_labels()
            logger.debug("Displayed image updated")
        except Exception as e:
            logger.error(f"Error updating displayed image: {str(e)}")

    def apply_changes(self, img_augmentation_layout):
        """
        Apply all specified image augmentations.

        Args:
            img_augmentation_layout: The layout containing augmentation parameters.
        """
        try:
            if not self.image_processor:
                logger.warning("No image processor available to apply changes")
                return

            self._apply_crop(img_augmentation_layout)
            self._apply_rotate(img_augmentation_layout)
            self._apply_flip(img_augmentation_layout)
            self._apply_adjustments(img_augmentation_layout)
            self._apply_noise(img_augmentation_layout)
            self._apply_translate(img_augmentation_layout)
            self._apply_shear(img_augmentation_layout)
            self._apply_stretch(img_augmentation_layout)
            self._apply_random_crop(img_augmentation_layout)
            self._apply_text_overlay(img_augmentation_layout)

            self._update_displayed_image(self.image_processor.image)
            self.update_image_size_labels()
            logger.info("All changes applied to the image")
        except Exception as e:
            logger.error(f"Error applying changes: {str(e)}")

    def clear_changes(self):
        """
        Clear all applied changes and reset the image to its original state.
        """
        try:
            img_augmentation_layout = self.view.ids.get('img_augmentation_layout')
            if img_augmentation_layout:
                    img_augmentation_layout.clear_fields()

            if self._select_image_from_treeview():
                if os.path.exists(TEMP_IMAGE_PATH):
                    os.remove(TEMP_IMAGE_PATH)
                logger.info("Changes cleared")
            else:
                logger.warning("No image selected in TreeView")
        except Exception as e:
            logger.error(f"Error clearing changes: {str(e)}")

    def _select_image_from_treeview(self) -> bool:
        """
        Select and display the image currently selected in the TreeView.

        Returns:
            bool: True if an image was selected and displayed, False otherwise.
        """
        try:
            selected_node = self.view.treeview.selected_node
            if isinstance(selected_node, FileTreeViewLabel) and self._is_image(selected_node.file_path):
                self.display_image(selected_node.file_path)
                return True
            return False
        except Exception as e:
            logger.error(f"Error selecting image from TreeView: {str(e)}")
            return False

    def _apply_crop(self, layout):
        """
        Apply crop operation to the image based on user input.

        Args:
            layout: The layout containing crop dimensions input fields.
        """
        try:
            width, height = layout.crop_width.text, layout.crop_height.text
            if width and height:
                self.crop_image(int(width), int(height))
            else:
                logger.warning("Crop dimensions not provided")
        except ValueError as e:
            logger.error(f"Invalid crop dimensions: {str(e)}")
        except Exception as e:
            logger.error(f"Error applying crop: {str(e)}")

    def _apply_rotate(self, layout):
        """
        Apply rotation to the image based on user input.

        Args:
            layout: The layout containing rotation angle input field.
        """
        try:
            angle = layout.rotate_angle.text
            if angle:
                self.image_processor.image = self.image_processor.rotate(float(angle))
                logger.info(f"Image rotated by {angle} degrees")
            else:
                logger.warning("Rotation angle not provided")
        except ValueError as e:
            logger.error(f"Invalid rotation angle: {str(e)}")
        except Exception as e:
            logger.error(f"Error applying rotation: {str(e)}")

    def _apply_flip(self, layout):
        """
        Apply flip operation to the image based on user input.

        Args:
            layout: The layout containing flip direction input field.
        """
        try:
            flip_direction = layout.flip_direction.text
            if flip_direction:
                self.image_processor.image = self.image_processor.flip(int(flip_direction))
                logger.info(f"Image flipped with direction {flip_direction}")
            else:
                logger.warning("Flip direction not provided")
        except ValueError as e:
            logger.error(f"Invalid flip direction: {str(e)}")
        except Exception as e:
            logger.error(f"Error applying flip: {str(e)}")

    def _apply_adjustments(self, layout):
        """
        Apply contrast, brightness, and saturation adjustments to the image based on user input.

        Args:
            layout: The layout containing adjustment factor input fields.
        """
        try:
            contrast = layout.contrast_factor.text
            brightness = layout.brightness_factor.text
            saturation = layout.saturation_factor.text
            
            if contrast:
                self.image_processor.image = self.image_processor.adjust_contrast(float(contrast))
                logger.info(f"Contrast adjusted by factor {contrast}")
            if brightness:
                self.image_processor.image = self.image_processor.adjust_brightness(float(brightness))
                logger.info(f"Brightness adjusted by factor {brightness}")
            if saturation:
                self.image_processor.image = self.image_processor.adjust_saturation(float(saturation))
                logger.info(f"Saturation adjusted by factor {saturation}")
        except ValueError as e:
            logger.error(f"Invalid adjustment factor: {str(e)}")
        except Exception as e:
            logger.error(f"Error applying adjustments: {str(e)}")

    def _apply_noise(self, layout):
        """
        Apply noise to the image based on user input.

        Args:
            layout: The layout containing noise parameters input fields.
        """
        try:
            noise_mean, noise_std = layout.noise_mean.text, layout.noise_std.text
            if noise_mean and noise_std:
                self.image_processor.image = self.image_processor.add_noise(float(noise_mean), float(noise_std))
                logger.info(f"Noise added with mean {noise_mean} and std {noise_std}")
            elif noise_mean:
                self.image_processor.image = self.image_processor.add_noise(float(noise_mean))
                logger.info(f"Noise added with mean {noise_mean} and std 25")
            else:
                logger.warning("Noise parameters not provided")
        except ValueError as e:
            logger.error(f"Invalid noise parameters: {str(e)}")
        except Exception as e:
            logger.error(f"Error applying noise: {str(e)}")

    def _apply_translate(self, layout):
        """
        Apply translation to the image based on user input.

        Args:
            layout: The layout containing translation parameters input fields.
        """
        try:
            translate_x, translate_y = layout.translate_x.text, layout.translate_y.text
            if translate_x and translate_y:
                self.image_processor.image = self.image_processor.translate(int(translate_x), int(translate_y))
                logger.info(f"Image translated by ({translate_x}, {translate_y})")
            else:
                logger.warning("Translation parameters not fully provided")
        except ValueError as e:
            logger.error(f"Invalid translation parameters: {str(e)}")
        except Exception as e:
            logger.error(f"Error applying translation: {str(e)}")

    def _apply_shear(self, layout):
        """
        Apply shear transformation to the image based on user input.

        Args:
            layout: The layout containing shear factor input field.
        """
        try:
            shear_factor = layout.shear_factor.text
            if shear_factor:
                self.image_processor.image = self.image_processor.shear(float(shear_factor))
                logger.info(f"Image sheared with factor {shear_factor}")
            else:
                logger.warning("Shear factor not provided")
        except ValueError as e:
            logger.error(f"Invalid shear factor: {str(e)}")
        except Exception as e:
            logger.error(f"Error applying shear: {str(e)}")

    def _apply_stretch(self, layout):
        """
        Apply stretch transformation to the image based on user input.

        Args:
            layout: The layout containing stretch factors input fields.
        """
        try:
            stretch_x, stretch_y = layout.stretch_x.text, layout.stretch_y.text
            if stretch_x and stretch_y:
                self.image_processor.image = self.image_processor.stretch(float(stretch_x), float(stretch_y))
                logger.info(f"Image stretched by factors ({stretch_x}, {stretch_y})")
            else:
                logger.warning("Stretch factors not fully provided")
        except ValueError as e:
            logger.error(f"Invalid stretch factors: {str(e)}")
        except Exception as e:
            logger.error(f"Error applying stretch: {str(e)}")

    def _apply_random_crop(self, layout):
        """
        Apply random crop to the image based on user input.

        Args:
            layout: The layout containing random crop dimensions input fields.
        """
        try:
            random_crop_width, random_crop_height = layout.random_crop_width.text, layout.random_crop_height.text
            if random_crop_width and random_crop_height:
                self.image_processor.image = self.image_processor.random_crop(int(random_crop_width), int(random_crop_height))
                logger.info(f"Random crop applied with dimensions {random_crop_width}x{random_crop_height}")
            else:
                logger.warning("Random crop dimensions not fully provided")
        except ValueError as e:
            logger.error(f"Invalid random crop dimensions: {str(e)}")
        except Exception as e:
            logger.error(f"Error applying random crop: {str(e)}")

    def _apply_text_overlay(self, layout):
        """
        Apply text overlay to the image based on user input.

        Args:
            layout: The layout containing text overlay parameters input fields.
        """
        try:
            text_overlay = layout.text_overlay.text
            text_position_x, text_position_y = layout.text_position_x.text, layout.text_position_y.text
            if text_overlay and text_position_x and text_position_y:
                self.image_processor.image = self.image_processor.add_text(
                    text_overlay, 
                    (int(text_position_x), int(text_position_y))
                )
                logger.info(f"Text overlay '{text_overlay}' applied at position ({text_position_x}, {text_position_y})")
            else:
                logger.warning("Text overlay parameters not fully provided")
        except ValueError as e:
            logger.error(f"Invalid text overlay parameters: {str(e)}")
        except Exception as e:
            logger.error(f"Error applying text overlay: {str(e)}")