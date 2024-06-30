# tests/test_main_screen_controller_image_operations.py
from tests.test_setup import *


class TestMainScreenControllerImageOperations(unittest.TestCase):
    def setUp(self):
        self.mock_view = Mock()
        self.controller = MainScreenController(self.mock_view)
        self.controller.image_processor = Mock()
        # Создаем мок-изображение
        self.mock_image = np.zeros((200, 200, 3), dtype=np.uint8)
        self.controller.image_processor.image = self.mock_image

    def test_display_image(self):
        with patch.object(self.controller, 'update_image_size_labels'):
            self.controller.display_image('/test/image.jpg')
            self.assertEqual(self.controller.original_image_path, '/test/image.jpg')
            self.mock_view.display_image.assert_called_once_with('/test/image.jpg')

    def test_crop_image(self):
        self.controller.crop_image(100, 100)
        self.controller.image_processor.crop.assert_called_once_with(50, 50, 100, 100)

    def test_rotate_image(self):
        self.controller.rotate_image(90)
        self.controller.image_processor.rotate.assert_called_once_with(90)

    def test_adjust_contrast(self):
        self.controller.adjust_contrast(1.5, 1.2)
        self.controller.image_processor.adjust_contrast.assert_called_once_with(1.5)
        self.controller.image_processor.adjust_brightness.assert_called_once_with(1.2)

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_save_image(self, mock_makedirs, mock_exists):
        mock_exists.return_value = False
        self.controller.original_image_path = '/test/original.jpg'
        self.controller.save_image()
        mock_makedirs.assert_called_once()
        self.controller.image_processor.save_image.assert_called_once()

if __name__ == '__main__':
    unittest.main()