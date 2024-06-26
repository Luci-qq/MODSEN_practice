from kivy.uix.treeview import TreeViewLabel
from kivymd.icon_definitions import md_icons
from kivy.properties import StringProperty

class FolderTreeViewLabel(TreeViewLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = md_icons['folder']
        icon_size = "24sp"
        self.text = f"[color=#FFD700][font=Icons][size={icon_size}]{self.icon}[/size][/font][/color] {self.text}"
        self.markup = True
        self.valign = 'middle'

class FileTreeViewLabel(TreeViewLabel):
    file_path = StringProperty('')
    def __init__(self, **kwargs):
        self.file_path = kwargs.pop('file_path', '')
        super().__init__(**kwargs)
        self.icon = md_icons['file']
        icon_size = "24sp"
        self.text = f"[color=#4CAF50][font=Icons][size={icon_size}]{self.icon}[/size][/font][/color] {self.text}"
        self.markup = True
        self.valign = 'middle'