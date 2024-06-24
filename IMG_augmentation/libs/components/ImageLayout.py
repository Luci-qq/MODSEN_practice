from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivy.properties import ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel

class ResizeToolbar(MDBoxLayout):
    pass

class RotateToolbar(MDBoxLayout):
    pass

class ContrastToolbar(MDBoxLayout):
    pass

class ImageToolbar(TabbedPanel):
    pass


class FunctionalLayout(MDBoxLayout):
    crop_width = ObjectProperty(None)
    crop_height = ObjectProperty(None)
    rotate_angle = ObjectProperty(None)
    contrast_factor = ObjectProperty(None)
    brightness_factor = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apply_changes = lambda: None 
        self.clear_changes = lambda: None 

    def clear_fields(self):
        self.crop_width.text = ''
        self.crop_height.text = ''
        self.rotate_angle.text = ''
        self.contrast_factor.text = ''
        self.brightness_factor.text = ''

    # Методы crop_image, rotate_image, adjust_contrast и save_image
    # будут определены в MainScreen и привязаны к этому классу

class ImageTools(MDBoxLayout):
    crop_button = ObjectProperty(None)
    rotate_button = ObjectProperty(None)
    contrast_button = ObjectProperty(None)
    save_button = ObjectProperty(None)

class ImageLayout(MDFloatLayout):
    pass