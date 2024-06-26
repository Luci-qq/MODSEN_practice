import os
import logging
from typing import Optional
from libs.components.logic.ImageProcessor import ImageProcessor
from libs.components.ui.TreeViewLabels import FileTreeViewLabel, FolderTreeViewLabel

# Настройка логгера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
TEMP_IMAGE_PATH = 'temp_image.png'
AUGMENTED_DIR = 'augmented'

class MainScreenController:
    def __init__(self, view):
        self.view = view
        self.image_processor: Optional[ImageProcessor] = None
        self.original_image_path: Optional[str] = None
        logger.info("MainScreenController initialized")

    def add_file(self):
        logger.debug("Adding file")
        self._show_file_manager(select_dir=False, selector='file')

    def add_folder(self):
        logger.debug("Adding folder")
        self._show_file_manager(select_dir=True, selector='folder')

    def _show_file_manager(self, select_dir: bool, selector: str):
        self.view.file_manager.show('/')
        self.view.file_manager.select_dir = select_dir
        self.view.file_manager.selector = selector
        logger.debug(f"File manager shown with select_dir={select_dir}, selector={selector}")

    def delete_selected(self):
        selected_node = self.view.treeview.selected_node
        if selected_node:
            self.view.treeview.remove_node(selected_node)
            logger.info(f"Deleted node: {selected_node}")
            if self.view.current_image and self.view.current_image.source == selected_node.file_path:
                self.clear_displayed_image()

    def clear_displayed_image(self):
        self.view.clear_displayed_image()
        self.image_processor = None
        if os.path.exists(TEMP_IMAGE_PATH):
            os.remove(TEMP_IMAGE_PATH)
        logger.info("Displayed image cleared")

    def select_path(self, path: str):
        self.view.exit_manager()
        if os.path.isdir(path):
            self.add_directory_to_tree(path, self.view.treeview.root)
            logger.info(f"Added directory to tree: {path}")
        elif self._is_image(path):
            node = FileTreeViewLabel(text=os.path.basename(path), file_path=path)
            self.view.treeview.add_node(node)
            logger.info(f"Added file to tree: {path}")

    def add_directory_to_tree(self, path: str, parent_node):
        dir_node = self.view.treeview.add_node(FolderTreeViewLabel(text=os.path.basename(path)), parent_node)
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path) and self._is_image(item_path):
                self.view.treeview.add_node(FileTreeViewLabel(text=item, file_path=item_path), dir_node)
            elif os.path.isdir(item_path):
                self.add_directory_to_tree(item_path, dir_node)
        logger.debug(f"Added directory contents to tree: {path}")

    @staticmethod
    def _is_image(file_path: str) -> bool:
        return any(file_path.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)

    def on_treeview_select(self, instance, value):
        if isinstance(value, FileTreeViewLabel) and self._is_image(value.file_path):
            self.display_image(value.file_path)
        else:
            self.clear_displayed_image()

    def display_image(self, file_path: str):
        self.original_image_path = file_path
        self.view.display_image(file_path)
        self.image_processor = ImageProcessor(file_path)
        logger.info(f"Displayed image: {file_path}")

    def save_image(self):
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

    @staticmethod
    def _get_unique_save_path(directory: str, filename: str) -> str:
        base, ext = os.path.splitext(filename)
        counter = 1
        save_path = os.path.join(directory, filename)
        while os.path.exists(save_path):
            save_path = os.path.join(directory, f"{base}_{counter}{ext}")
            counter += 1
        return save_path

    def crop_image(self, width: int, height: int):
        if self.image_processor:
            left = (self.image_processor.image.shape[1] - width) // 2
            top = (self.image_processor.image.shape[0] - height) // 2
            self.image_processor.image = self.image_processor.crop(left, top, width, height)
            logger.info(f"Image cropped to {width}x{height}")

    def rotate_image(self, angle: float):
        if self.image_processor:
            rotated_image = self.image_processor.rotate(angle)
            self._update_displayed_image(rotated_image)
            logger.info(f"Image rotated by {angle} degrees")

    def adjust_contrast(self, contrast_factor: float = 0, brightness_factor: float = 0):
        if self.image_processor:
            image = self.image_processor.adjust_contrast(contrast_factor)
            image = self.image_processor.adjust_brightness(brightness_factor)
            self._update_displayed_image(image)
            logger.info(f"Image contrast adjusted by {contrast_factor}, brightness by {brightness_factor}")

    def _update_displayed_image(self, image):
        self.image_processor.save_image(TEMP_IMAGE_PATH)
        self.view.update_image_source(TEMP_IMAGE_PATH)
        logger.debug("Displayed image updated")

    def apply_changes(self, functional_layout):
        if not self.image_processor:
            logger.warning("No image processor available to apply changes")
            return

        self._apply_crop(functional_layout)
        self._apply_rotate(functional_layout)
        self._apply_flip(functional_layout)
        self._apply_adjustments(functional_layout)
        self._apply_noise(functional_layout)
        self._apply_translate(functional_layout)
        self._apply_shear(functional_layout)
        self._apply_stretch(functional_layout)
        self._apply_random_crop(functional_layout)
        self._apply_text_overlay(functional_layout)

        self._update_displayed_image(self.image_processor.image)
        logger.info("All changes applied to the image")

    def _apply_crop(self, layout):
        width, height = layout.crop_width.text, layout.crop_height.text
        if width and height:
            self.crop_image(int(width), int(height))

    def _apply_rotate(self, layout):
        angle = layout.rotate_angle.text
        if angle:
            self.image_processor.image = self.image_processor.rotate(float(angle))

    def _apply_flip(self, layout):
        flip_direction = layout.flip_direction.text
        if flip_direction:
            self.image_processor.image = self.image_processor.flip(int(flip_direction))

    def _apply_adjustments(self, layout):
        contrast = layout.contrast_factor.text
        brightness = layout.brightness_factor.text
        saturation = layout.saturation_factor.text
        if contrast:
            self.image_processor.image = self.image_processor.adjust_contrast(float(contrast))
        if brightness:
            self.image_processor.image = self.image_processor.adjust_brightness(float(brightness))
        if saturation:
            self.image_processor.image = self.image_processor.adjust_saturation(float(saturation))

    def _apply_noise(self, layout):
        noise_mean, noise_std = layout.noise_mean.text, layout.noise_std.text
        if noise_mean and noise_std:
            self.image_processor.image = self.image_processor.add_noise(float(noise_mean), float(noise_std))

    def _apply_translate(self, layout):
        translate_x, translate_y = layout.translate_x.text, layout.translate_y.text
        if translate_x and translate_y:
            self.image_processor.image = self.image_processor.translate(int(translate_x), int(translate_y))

    def _apply_shear(self, layout):
        shear_factor = layout.shear_factor.text
        if shear_factor:
            self.image_processor.image = self.image_processor.shear(float(shear_factor))

    def _apply_stretch(self, layout):
        stretch_x, stretch_y = layout.stretch_x.text, layout.stretch_y.text
        if stretch_x and stretch_y:
            self.image_processor.image = self.image_processor.stretch(float(stretch_x), float(stretch_y))

    def _apply_random_crop(self, layout):
        random_crop_width, random_crop_height = layout.random_crop_width.text, layout.random_crop_height.text
        if random_crop_width and random_crop_height:
            self.image_processor.image = self.image_processor.random_crop(int(random_crop_width), int(random_crop_height))

    def _apply_text_overlay(self, layout):
        text_overlay = layout.text_overlay.text
        text_position_x, text_position_y = layout.text_position_x.text, layout.text_position_y.text
        if text_overlay and text_position_x and text_position_y:
            self.image_processor.image = self.image_processor.add_text(
                text_overlay, 
                (int(text_position_x), int(text_position_y))
            )

    def clear_changes(self):
        if self._select_image_from_treeview():
            functional_layout = self.view.ids.get('functional_layout')
            if functional_layout:
                functional_layout.clear_fields()

            if os.path.exists(TEMP_IMAGE_PATH):
                os.remove(TEMP_IMAGE_PATH)
            logger.info("Changes cleared")
        else:
            logger.warning("No image selected in TreeView")

    def _select_image_from_treeview(self) -> bool:
        selected_node = self.view.treeview.selected_node
        if isinstance(selected_node, FileTreeViewLabel) and self._is_image(selected_node.file_path):
            self.display_image(selected_node.file_path)
            return True
        return False