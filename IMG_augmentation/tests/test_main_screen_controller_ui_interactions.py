# tests/test_main_screen_controller_ui_interactions.py
from test_setup import *


class TestMainScreenControllerUIInteractions(unittest.TestCase):
    def setUp(self):
        self.mock_view = Mock()
        self.controller = MainScreenController(self.mock_view)

    def test_on_treeview_select_file(self):
        # Создаем мок-объект FileTreeViewLabel
        mock_node = Mock(spec=FileTreeViewLabel)
        mock_node.file_path = '/test/image.jpg'
        
        # Патчим метод _is_image, чтобы он всегда возвращал True для нашего тестового файла
        with patch.object(self.controller, '_is_image', return_value=True) as mock_is_image, \
             patch.object(self.controller, 'display_image') as mock_display:
            
            # Вызываем тестируемый метод
            self.controller.on_treeview_select(None, mock_node)
            
            # Проверяем, что _is_image был вызван с правильным аргументом
            mock_is_image.assert_called_once_with('/test/image.jpg')
            
            # Проверяем, что display_image был вызван с правильным аргументом
            mock_display.assert_called_once_with('/test/image.jpg')

    def test_on_treeview_select_non_file(self):
        mock_node = Mock(spec=FileTreeViewLabel)
        mock_node.file_path = '/test/folder'
        with patch.object(self.controller, '_is_image', return_value=False), \
             patch.object(self.controller, 'clear_displayed_image') as mock_clear:
            self.controller.on_treeview_select(None, mock_node)
            mock_clear.assert_called_once()

    def test_update_image_size_labels(self):
        self.controller.image_processor = Mock()
        self.controller.image_processor.get_dimensions.return_value = {'width': 100, 'height': 200}
        self.controller.update_image_size_labels()
        self.assertEqual(self.mock_view.ids.image_layout.width_label.text, 'IMG_Width: 100')
        self.assertEqual(self.mock_view.ids.image_layout.height_label.text, 'IMG_Height: 200')

    def test_apply_changes(self):
        mock_layout = Mock()
        mock_layout.crop_width.text = '100'
        mock_layout.crop_height.text = '100'
        mock_layout.rotate_angle.text = '90'


        with patch.object(self.controller, '_update_displayed_image'):
            self.controller.apply_changes(mock_layout)


if __name__ == '__main__':
    unittest.main()