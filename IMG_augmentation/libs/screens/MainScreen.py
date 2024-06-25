import os
import cv2
from kivymd.uix.screen import MDScreen
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.image import Image
from libs.components.TreeViewLabels import FileTreeViewLabel, FolderTreeViewLabel
from kivy.uix.tabbedpanel import TabbedPanel
from libs.components.ImageProcessor import ImageProcessor  # Импорт вашего класса ImageProcessor

class ImageToolbar(TabbedPanel):
    pass

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = None
        self.current_image = None
        self.image_processor = None
        self.temp_image_path = 'temp_image.png'
        self.original_image_path = None  
        self.bind_widgets()

    def bind_widgets(self):
        tree_view_layout = self.ids.get('treeview_layout')
        self.treeview = tree_view_layout.treeview_image

        if tree_view_layout and tree_view_layout.treeview_buttons:
            buttons = tree_view_layout.treeview_buttons
            buttons.add_file_button.on_release = self.add_file
            buttons.add_folder_button.on_release = self.add_folder
            buttons.delete_entry_button.on_release = self.delete_selected

        if not self.file_manager:
            self.file_manager = MDFileManager(
                exit_manager=self.exit_manager,
                select_path=self.select_path,
                ext=['.png', '.jpg', '.jpeg', '.gif', '.bmp']
            )

        self.treeview.bind(selected_node=self.on_treeview_select)

        functional_layout = self.ids.get('functional_layout')
        if functional_layout:
            functional_layout.crop_image = self.crop_image
            functional_layout.rotate_image = self.rotate_image
            functional_layout.adjust_contrast = self.adjust_contrast
            functional_layout.save_image = self.save_image
            functional_layout.apply_changes = self.apply_changes
            functional_layout.clear_changes = self.clear_changes

    def add_file(self):
        self.file_manager.show('/')
        self.file_manager.select_dir = False
        self.file_manager.selector = 'file'

    def add_folder(self):
        self.file_manager.show('/')
        self.file_manager.select_dir = True
        self.file_manager.selector = 'folder'

    def delete_selected(self):
        selected_node = self.treeview.selected_node
        if selected_node:
            self.treeview.remove_node(selected_node)
            if isinstance(selected_node, FileTreeViewLabel):
                if self.current_image and self.current_image.source == selected_node.file_path:
                    self.clear_displayed_image()

    def clear_displayed_image(self):
        if self.current_image:
            self.ids.image_layout.remove_widget(self.current_image)
            self.current_image = None
        self.image_processor = None
        if os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path)

    def select_path(self, path):
        self.exit_manager()

        if os.path.isdir(path):
            self.add_directory_to_tree(path, self.treeview.root)
        elif self.is_image(path):
            node = FileTreeViewLabel(text=os.path.basename(path), file_path=path)
            self.treeview.add_node(node)

    def add_directory_to_tree(self, path, parent_node):
        dir_node = self.treeview.add_node(FolderTreeViewLabel(text=os.path.basename(path)), parent_node)
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path) and self.is_image(item_path):
               self.treeview.add_node(FileTreeViewLabel(text=item, file_path=item_path), dir_node)
            elif os.path.isdir(item_path):
                self.add_directory_to_tree(item_path, dir_node)

    def is_image(self, file_path):
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        return any(file_path.lower().endswith(ext) for ext in image_extensions)

    def exit_manager(self, *args):
        self.file_manager.close()
    
    def on_treeview_select(self, instance, value):
        if isinstance(value, FileTreeViewLabel):
            file_path = value.file_path
            if self.is_image(file_path):
                self.display_image(file_path)
            else:
                self.clear_displayed_image()
        else:
            self.clear_displayed_image()

    def select_image_from_treeview(self):
        selected_node = self.treeview.selected_node
        if isinstance(selected_node, FileTreeViewLabel):
            file_path = selected_node.file_path
            if self.is_image(file_path):
                self.display_image(file_path)
                return True
        return False

    def display_image(self, file_path):
        self.original_image_path = file_path
        if self.current_image:
            self.ids.image_layout.remove_widget(self.current_image)
        
        self.current_image = Image(
            source=file_path,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.ids.image_layout.add_widget(self.current_image)

        self.image_processor = ImageProcessor(file_path)

    def clear_changes(self):
        if self.select_image_from_treeview():
            functional_layout = self.ids.get('functional_layout')
            if functional_layout:
                functional_layout.clear_fields()

            if os.path.exists(self.temp_image_path):
                os.remove(self.temp_image_path)
        else:
            print("No image selected in TreeView")

    def save_image(self):
        if self.image_processor and hasattr(self, 'original_image_path'):
            original_filename = os.path.basename(self.original_image_path)
            
            augmented_dir = os.path.join(os.getcwd(), 'augmented')
            if not os.path.exists(augmented_dir):
                os.makedirs(augmented_dir)
            
            save_path = os.path.join(augmented_dir, original_filename)
            
            base, ext = os.path.splitext(save_path)
            counter = 1
            while os.path.exists(save_path):
                save_path = f"{base}_{counter}{ext}"
                counter += 1
            
            cv2.imwrite(save_path, self.image_processor.image)
            
            print(f"Image saved as {save_path}")

            if self.current_image:
                self.current_image.source = save_path
                self.current_image.reload()

        else:
            print("No image to save or original image path not found")

        if os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path)

    def crop_image(self, width, height):
        if self.image_processor:
            width = int(width)
            height = int(height)
            left = (self.image_processor.image.shape[1] - width) // 2
            top = (self.image_processor.image.shape[0] - height) // 2
            self.image_processor.image = self.image_processor.crop(left, top, width, height)

    def rotate_image(self, angle):
        if self.image_processor:
            rotated_image = self.image_processor.rotate(float(angle))
            self.update_displayed_image(rotated_image)

    def adjust_contrast(self, contrast_factor=0, brightness_factor=0):
        if self.image_processor:
            image = self.image_processor.adjust_contrast(float(contrast_factor))
            image = self.image_processor.adjust_brightness(float(brightness_factor))
            self.update_displayed_image(image)

    def update_displayed_image(self, cv2_image):
        cv2.imwrite(self.temp_image_path, cv2_image)
        if self.current_image:
            self.current_image.source = self.temp_image_path
            self.current_image.reload()
        else:
            self.current_image = Image(source=self.temp_image_path, pos_hint={"center_x": 0.5, "center_y": 0.5})
            self.ids.image_layout.add_widget(self.current_image)

    def apply_changes(self):
        functional_layout = self.ids.get('functional_layout')
        if functional_layout and self.image_processor:
            # Crop
            width = functional_layout.crop_width.text
            height = functional_layout.crop_height.text
            if width and height:
                self.crop_image(int(width), int(height))

            # Rotate
            angle = functional_layout.rotate_angle.text
            if angle:
                self.image_processor.image = self.image_processor.rotate(float(angle))

            # Flip
            flip_direction = functional_layout.flip_direction.text
            if flip_direction:
                self.image_processor.image = self.image_processor.flip(int(flip_direction))

            # Adjust contrast, brightness, and saturation
            contrast = functional_layout.contrast_factor.text
            brightness = functional_layout.brightness_factor.text
            saturation = functional_layout.saturation_factor.text
            if contrast:
                self.image_processor.image = self.image_processor.adjust_contrast(float(contrast))
            if brightness:
                self.image_processor.image = self.image_processor.adjust_brightness(float(brightness))
            if saturation:
                self.image_processor.image = self.image_processor.adjust_saturation(float(saturation))

            # Add noise
            noise_mean = functional_layout.noise_mean.text
            noise_std = functional_layout.noise_std.text
            if noise_mean and noise_std:
                self.image_processor.image = self.image_processor.add_noise(float(noise_mean), float(noise_std))

            # Translate
            translate_x = functional_layout.translate_x.text
            translate_y = functional_layout.translate_y.text
            if translate_x and translate_y:
                self.image_processor.image = self.image_processor.translate(int(translate_x), int(translate_y))

            # Shear
            shear_factor = functional_layout.shear_factor.text
            if shear_factor:
                self.image_processor.image = self.image_processor.shear(float(shear_factor))

            # Stretch
            stretch_x = functional_layout.stretch_x.text
            stretch_y = functional_layout.stretch_y.text
            if stretch_x and stretch_y:
                self.image_processor.image = self.image_processor.stretch(float(stretch_x), float(stretch_y))

            # Random crop
            random_crop_width = functional_layout.random_crop_width.text
            random_crop_height = functional_layout.random_crop_height.text
            if random_crop_width and random_crop_height:
                self.image_processor.image = self.image_processor.random_crop(int(random_crop_width), int(random_crop_height))

            # Add text
            text_overlay = functional_layout.text_overlay.text
            text_position_x = functional_layout.text_position_x.text
            text_position_y = functional_layout.text_position_y.text
            if text_overlay and text_position_x and text_position_y:
                self.image_processor.image = self.image_processor.add_text(
                    text_overlay, 
                    (int(text_position_x), int(text_position_y))
                )

            # Update displayed image
            self.update_displayed_image(self.image_processor.image)