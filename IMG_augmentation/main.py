from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from libs.screens.MainScreen import MainScreen


class ImageAugmentationApp(MDApp):
    def build(self):
        Window.maximize()

        self.load_kv_files()
        return MainScreen()
    
    def load_kv_files(self):
        Builder.load_file('libs/components/ui/Buttons.kv')

        #TreeViewLayout
        Builder.load_file('libs/components/ui/TreeViewLayout.kv')

        #ImageLayout
        Builder.load_file('libs/components/ui/ImageLayout.kv')
    
        #MainScreen
        Builder.load_file('libs/screens/MainScreen.kv')



if __name__ == '__main__':
    ImageAugmentationApp().run()