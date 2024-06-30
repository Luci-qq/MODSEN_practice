# tests/test_main_screen_controller_file_operations.py
from tests.test_setup import *


class TestMainScreenControllerFileOperations(unittest.TestCase):
    def setUp(self):
        self.mock_view = Mock()
        self.controller = MainScreenController(self.mock_view)

    def test_add_file(self):
        with patch.object(self.controller, '_show_file_manager') as mock_show_file_manager:
            self.controller.add_file()
            mock_show_file_manager.assert_called_once_with(select_dir=False, selector='file')

    def test_add_folder(self):
        with patch.object(self.controller, '_show_file_manager') as mock_show_file_manager:
            self.controller.add_folder()
            mock_show_file_manager.assert_called_once_with(select_dir=True, selector='folder')

    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_select_path_directory(self, mock_isfile, mock_isdir):
        mock_isdir.return_value = True
        mock_isfile.return_value = False
        with patch.object(self.controller, 'add_directory_to_tree') as mock_add_directory:
            self.controller.select_path('/test/path')
            mock_add_directory.assert_called_once_with('/test/path', self.controller.view.treeview.root)

    @patch('os.path.isdir')
    @patch('os.path.isfile')
    def test_select_path_file(self, mock_isfile, mock_isdir):
        mock_isdir.return_value = False
        mock_isfile.return_value = True
        with patch.object(self.controller, '_is_image', return_value=True):
            self.controller.select_path('/test/image.jpg')
            self.controller.view.treeview.add_node.assert_called_once()

    def test_is_image(self):
        self.assertTrue(self.controller._is_image('test.jpg'))
        self.assertTrue(self.controller._is_image('test.PNG'))
        self.assertFalse(self.controller._is_image('test.txt'))

if __name__ == '__main__':
    unittest.main()