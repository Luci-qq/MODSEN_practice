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

    def display_image(self, file_path):
        if self.current_image:
            self.ids.image_layout.remove_widget(self.current_image)
        
        self.current_image = Image(
            source=file_path,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.ids.image_layout.add_widget(self.current_image)

        self.image_processor = ImageProcessor(file_path)

    def clear_changes(self):
        if self.image_processor:
            self.update_displayed_image(self.image_processor.image)
            
            functional_layout = self.ids.get('functional_layout')
            if functional_layout:
                functional_layout.clear_fields()

        if os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path)

    def save_image(self):
        if self.image_processor:
            if not os.path.exists('augmented'):
                os.makedirs('augmented')
            
            original_filename = os.path.basename(self.current_image.source)
            filename, ext = os.path.splitext(original_filename)
            
            new_filename = f"{filename}_augmented{ext}"
            
            save_path = os.path.join('augmented', new_filename)
            
            cv2.imwrite(save_path, self.image_processor.image)
            print(f"Image saved to {save_path}")

        if os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path)

    def crop_image(self, width, height):
        if self.image_processor:
            width = int(width)
            height = int(height)
            left = (self.image_processor.image.shape[1] - width) // 2
            top = (self.image_processor.image.shape[0] - height) // 2
            cropped_image = self.image_processor.crop(left, top, width, height)
            self.update_displayed_image(cropped_image)

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
        self.image_processor.image = cv2_image
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
            width = functional_layout.crop_width.text
            height = functional_layout.crop_height.text
            if width and height:
                self.crop_image(int(width), int(height))

            angle = functional_layout.rotate_angle.text
            if angle:
                self.rotate_image(float(angle))

            contrast = functional_layout.contrast_factor.text
            brightness = functional_layout.brightness_factor.text
            if contrast and brightness:
                self.adjust_contrast(float(contrast), float(brightness))