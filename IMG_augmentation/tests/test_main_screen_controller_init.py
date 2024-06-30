# tests/test_main_screen_controller_init.py
from tests.test_setup import *


class TestMainScreenControllerInit(unittest.TestCase):
    def setUp(self):
        self.mock_view = Mock()
        self.controller = MainScreenController(self.mock_view)

    def test_init(self):
        self.assertIsInstance(self.controller, MainScreenController)
        self.assertEqual(self.controller.view, self.mock_view)
        self.assertIsNone(self.controller.image_processor)
        self.assertIsNone(self.controller.original_image_path)

if __name__ == '__main__':
    unittest.main()