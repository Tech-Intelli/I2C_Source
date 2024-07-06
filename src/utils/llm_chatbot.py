import ollama
from configuration_manager import ConfigManager

class LLMChatbot:
    """
    A class representing a chatbot that interacts with the OpenAI Chat API.
    """

    def __init__(self):
        """
        Initializes a new Chatbot instance.
        """
        self.app_config = ConfigManager.get_config_manager().get_app_config()
        self.model = self.app_config.ollama.variants.phi3
        self.temperature = self.app_config.ollama.temperature
        self.top_p = self.app_config.ollama.top_p
 
    def get_response(self, content, stream=False):
        """Sends a message to the Ollama llama-3 or phi-3 chat model and returns its
        response as a stream.

        Args:
            content (str): The content of the message to be sent.
            stream (bool): Whether to stream the response.
        Returns:
            dict: A dictionary containing the response from the chat model.
        """
        stream_caption = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": content}],
            stream=stream,
            options={"temperature": self.temperature, "top_p": self.top_p},
        )
        return stream_caption
