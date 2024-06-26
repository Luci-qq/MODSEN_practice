from kivymd.uix.boxlayout import MDBoxLayout

class ImageAugmentationLayout(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.apply_changes = lambda: None 
        self.clear_changes = lambda: None 

    def clear_fields(self):
        fields_to_clear = [
            'crop_width', 'crop_height', 'rotate_angle', 'flip_direction',
            'contrast_factor', 'brightness_factor', 'saturation_factor',
            'noise_mean', 'noise_std', 'translate_x', 'translate_y',
            'shear_factor', 'stretch_x', 'stretch_y',
            'random_crop_width', 'random_crop_height',
            'text_overlay', 'text_position_x', 'text_position_y'
        ]
        
        for field in fields_to_clear:
            if hasattr(self, field):
                getattr(self, field).text = ''
