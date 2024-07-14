import unittest
from unittest.mock import patch, MagicMock
from llm_chatbot import LLMChatbot


class TestLLMChatbot(unittest.TestCase):
    @patch("configuration_manager.config_manager.ConfigManager.get_config_manager")
    def test_initialization(self, mock_get_config_manager):
        """
        Test the initialization of the LLMChatbot class by mocking the configuration manager and app_config.

        This test case verifies that the LLMChatbot class correctly loads the configuration from the configuration manager and sets the appropriate attributes.

        Parameters:
            mock_get_config_manager (MagicMock): A mock object representing the get_config_manager method of the ConfigManager class.

        Returns:
            None

        Raises:
            AssertionError: If the model, temperature, or top_p attributes of the chatbot are not equal to the expected values.
        """
        # Mock configuration manager and app_config
        mock_config_manager = MagicMock()
        mock_app_config = MagicMock()
        mock_app_config.ollama.variants.phi3 = "phi-3-model"
        mock_app_config.ollama.temperature = 0.5
        mock_app_config.ollama.top_p = 0.9

        mock_config_manager.get_app_config.return_value = mock_app_config
        mock_get_config_manager.return_value = mock_config_manager

        # Initialize chatbot
        chatbot = LLMChatbot()

        # Assertions to verify that configuration is loaded correctly
        self.assertEqual(chatbot.model, "phi-3-model")
        self.assertEqual(chatbot.temperature, 0.5)
        self.assertEqual(chatbot.top_p, 0.9)

    @patch("ollama.chat")
    @patch("configuration_manager.config_manager.ConfigManager.get_config_manager")
    def test_get_response(self, mock_get_config_manager, mock_ollama_chat):
        """
        Test the get_response method by mocking the configuration manager and ollama chat.

        This test case sets up the configuration and return values for ollama chat, initializes the chatbot,
        tests the get_response method with a message 'Hello' and stream set to True,
        verifies the correct call to ollama chat, and checks the response.

        Parameters:
            mock_get_config_manager (MagicMock): A mock object representing the get_config_manager method of the ConfigManager class.
            mock_ollama_chat (MagicMock): A mock object for the ollama chat function.

        Returns:
            None
        """
        # Setup configuration as in the previous test
        mock_config_manager = MagicMock()
        mock_app_config = MagicMock()
        mock_app_config.ollama.variants.phi3 = "phi-3-model"
        mock_app_config.ollama.temperature = 0.5
        mock_app_config.ollama.top_p = 0.9

        mock_config_manager.get_app_config.return_value = mock_app_config
        mock_get_config_manager.return_value = mock_config_manager

        # Setup return value for ollama.chat
        mock_ollama_chat.return_value = {"response": "test response"}

        # Initialize chatbot
        chatbot = LLMChatbot()

        # Test get_response
        response = chatbot.get_response("Hello", stream=True)

        # Verify ollama.chat was called correctly
        mock_ollama_chat.assert_called_once_with(
            model="phi-3-model",
            messages=[{"role": "user", "content": "Hello"}],
            stream=True,
            options={"temperature": 0.5, "top_p": 0.9},
        )

        # Check the response
        self.assertEqual(response, {"response": "test response"})


if __name__ == "__main__":
    unittest.main()
