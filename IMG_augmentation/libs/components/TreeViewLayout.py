from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.treeview import TreeView

class TreeViewHandleLayout(MDBoxLayout):
    add_file_button = ObjectProperty(None)
    add_folder_button = ObjectProperty(None)
    delete_entry_button = ObjectProperty(None)

class TreeViewImage(TreeView):
    pass

class TreeViewLayout(MDBoxLayout):
    treeview_buttons = ObjectProperty(None)
    treeview_image = ObjectProperty(None)