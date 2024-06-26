from kivymd.uix.screen import MDScreen
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.image import Image
from libs.components.ui.TreeViewLabels import FileTreeViewLabel, FolderTreeViewLabel
from libs.screens.controllers.MainScreenController import MainScreenController

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_manager = None
        self.current_image = None
        self.controller = MainScreenController(self)
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

        img_augmentation_layout = self.ids.get('img_augmentation_layout')
        if img_augmentation_layout:
            img_augmentation_layout.clear_changes = self.clear_changes
            img_augmentation_layout.apply_changes = self.apply_changes
            img_augmentation_layout.save_image = self.save_image

        if self.ids.get('image_layout'): 
            self.ids.image_layout.height_label.text = 'IMG_Height: [b]N/A[/b]'
            self.ids.image_layout.width_label.text = 'IMG_Width: [b]N/A[/b]'
            
            self.ids.image_layout.height_label.markup = True
            self.ids.image_layout.width_label.markup = True

    def add_file(self):
        self.controller.add_file()

    def add_folder(self):
        self.controller.add_folder()

    def delete_selected(self):
        self.controller.delete_selected()

    def clear_displayed_image(self):
        if self.current_image:
            self.ids.image_layout.remove_widget(self.current_image)
            self.current_image = None

    def select_path(self, path):
        self.controller.select_path(path)

    def exit_manager(self, *args):
        self.file_manager.close()

    def on_treeview_select(self, instance, value):
        self.controller.on_treeview_select(instance, value)

    def display_image(self, file_path):
        if self.current_image:
            self.ids.image_layout.remove_widget(self.current_image)
        
        self.current_image = Image(
            source=file_path,
            size_hint = (0.8,0.8), 
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.ids.image_layout.add_widget(self.current_image)

    def update_image_source(self, source):
        if self.current_image:
            self.current_image.source = source
            self.current_image.reload()

    def save_image(self):
        self.controller.save_image()

    def apply_changes(self):
        img_augmentation_layout = self.ids.get('img_augmentation_layout')
        self.controller.apply_changes(img_augmentation_layout)

    def clear_changes(self):
        self.controller.clear_changes()

    def select_image_from_treeview(self):
        return self.controller.select_image_from_treeview()