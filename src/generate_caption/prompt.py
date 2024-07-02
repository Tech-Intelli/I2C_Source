class Prompt:
    def __init__(self):
        """
        Initializes a new Chatbot instance.
        """

    def _read_prompt_template(self, file_path):
        """
        Reads a prompt template from a file.
        """
        with open(file_path, "r") as file:
            return file.read()

    def _get_caption_size(self, caption_size="small"):
        """
        Get the description of the caption size.

        This function maps a given caption size to a corresponding description string.
        If the provided caption size is not recognized, it returns "Invalid caption size".

        Args:
            caption_size (str): The size of the caption. Can be one of 'small', 'medium',
                                'large', 'very large', or 'blog post'.

        Returns:
            str: The description corresponding to the caption size, or "Invalid caption size"
                if the caption size is not recognized.
        """
        # Dictionary to map caption sizes to their corresponding description
        caption_length_mapping = {
            "small": "Compose a concise 2 to 3 sentences",
            "medium": "Compose a concise 5 to 7 sentences",
            "large": "Compose a concise 10 to 15 sentences",
            "very large": "Compose an extensive 30 to 50 sentences",
            "blog post": "Craft an extensive 100 sentences",
        }

        return caption_length_mapping[caption_size]
