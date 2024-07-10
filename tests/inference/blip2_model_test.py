import unittest
from unittest.mock import patch, MagicMock
import torch
class TestBlip2Model(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment by patching external dependencies and creating an instance of the Blip2Model class.

        This method initializes the `collection` attribute with the value 'test_collection'.
        It then creates a list of patches for external dependencies that the Blip2Model class might use.
        The patches are applied using the `patch.start()` method, and the patches are cleaned up using the `addCleanup()` method.

        After setting up the patches, the `Blip2Model` class is imported and an instance of the class is created using the `self.collection` attribute.
        The instance is assigned to the `self.blip2_model` attribute.

        This method is called before each test case is run, and it sets up the necessary environment for the tests.

        Parameters:
            self (TestBlip2Model): The current test case instance.

        Returns:
            None
        """
        self.collection = 'test_collection'
        patches = [
            patch('inference.impl.blip2_model.Blip2Pipeline'),
            patch('torch.cuda.is_available', return_value=True),
            patch('gc.collect'),
            patch('torch.cuda.empty_cache'),
            patch('torch.cuda.synchronize'),
            patch('vector_store.get_unique_image_id', return_value='unique123'),
            patch('vector_store.add_image_to_chroma')
        ]
        for patcher in patches:
            patcher.start()
            self.addCleanup(patcher.stop)

        # Import the class after setting up the patches to ensure it uses the mocked versions
        from inference.impl.blip2_model import Blip2Model
        self.blip2_model = Blip2Model(self.collection)

    def test_init(self):
        """Test the initialization of the Blip2Model class."""
        self.assertIsNotNone(self.blip2_model)
        self.assertEqual(self.blip2_model.collection, self.collection)

    @patch('inference.impl.blip2_model.Blip2Model.load_model')
    def test_load_model(self, mock_load_model):
        """Test loading the model correctly initializes model components."""
        self.blip2_model.load_model()
        mock_load_model.assert_called_once()

    @patch('inference.abstract.inference_abstract.InferenceAbstract.load_image', return_value='image')
    @patch('inference.impl.blip2_model.Blip2Model.BLIP2_PROCESSOR', create=True)
    @patch('inference.impl.blip2_model.Blip2Model.BLIP2_MODEL', create=True)
    def test_get_image_caption_pipeline(self, mock_model, mock_processor, mock_load_image):
        """Test the image captioning pipeline functionality."""
        mock_processor.return_value = MagicMock()
        mock_processor.return_value.return_tensors = "pt"
        mock_model.generate.return_value = torch.tensor([[101, 102, 103]])
        mock_processor.batch_decode.return_value = ['This is a test caption.']

        caption = self.blip2_model.get_image_caption_pipeline('dummy_path')

        mock_load_image.assert_called_once_with('dummy_path')
        self.assertEqual(caption, 'This is a test caption.')

if __name__ == '__main__':
    unittest.main()
