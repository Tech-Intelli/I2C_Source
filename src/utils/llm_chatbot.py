import ollama


class LLMChatbot:
    """
    A class representing a chatbot that interacts with the OpenAI Chat API.
    """

    def __init__(self):
        """
        Initializes a new Chatbot instance.
        """

    def get_response(self, content):
        """
        Sends a message to the Ollama llama-3 or phi-3 chat model and returns its
        response.

        Args:
            content (str): The content of the message to be sent.

        Returns:
            dict: A dictionary containing the response from the chat model.
        """

        response = ollama.chat(
            model="phi3",
            messages=[{"role": "user", "content": content}],
            options={"temperature": 1, "top_p": 0.9},
        )
        return response

    def get_stream_response(self, content):
        """Sends a message to the Ollama llama-3 or phi-3 chat model and returns its
        response as a stream.

        Args:
            content (str): The content of the message to be sent.

        Returns:
            dict: A dictionary containing the response from the chat model.
        """
        stream_caption = ollama.chat(
            model="phi3",
            messages=[{"role": "user", "content": content}],
            stream=True,
            options={"temperature": 1, "top_p": 0.9},
        )
        return stream_caption
