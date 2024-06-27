from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import ObjectProperty


class ImageLayout(MDFloatLayout):
    height_label = ObjectProperty(None)
    width_label = ObjectProperty(None)
