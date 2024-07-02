class Hashtag:

    def __init__(self, caption, chatbot):
        """
        Initializes a new Hashtag instance.
        """
        self.caption = caption
        self.chatbot = chatbot

    def parse_hashtags(self):
        """
        Parses hashtags from the caption and removes them from the original string.

        Args:
        caption (str): The caption containing hashtags.

        Returns:
        tuple: A tuple containing the cleaned caption and a list of hashtags.
        """
        # Split the caption into words
        words = self.caption.split()
        # Extract hashtags from the words
        hashtags = [word for word in words if word.startswith("#")]
        # Reconstruct the caption without hashtags
        cleaned_caption = " ".join(word for word in words if not word.startswith("#"))
        return cleaned_caption, hashtags

    def _find_synonyms(self, word):
        """
        Find synonyms for a given word using Ollama.

        Args:
        word (str): The word to find synonyms for.

        Returns:
        list: A list of synonyms for the given word.
        """
        response = self.chatbot.get_response(f"Find synonyms for the word '{word}'.")
        synonyms = response["choices"][0]["text"].strip().split(", ")
        return synonyms

    def generate_additional_hashtags(self, existing_hashtags, num_needed):
        """
        Generate additional hashtags if needed.

        Args:
        existing_hashtags (list): List of existing hashtags.
        num_needed (int): Number of additional hashtags needed.

        Returns:
        list: List of additional hashtags.
        """
        additional_hashtags = []
        # Extract words from existing hashtags (remove the '#')
        words = {hashtag[1:] for hashtag in existing_hashtags}

        for word in words:
            # Find synonyms for each word
            synonyms = self._find_synonyms(word)
            for synonym in synonyms:
                # Stop if the required number of additional hashtags is reached
                if len(additional_hashtags) >= num_needed:
                    break
                # Add the synonym as a hashtag if it's not already in the existing hashtags
                if f"#{synonym}" not in existing_hashtags:
                    additional_hashtags.append(f"#{synonym}")

        return additional_hashtags

    def generate_hashtagged_caption(self, num_tags):
        """
        Generate a string of hashtags from a caption.

        Parameters:
        caption (str): The caption from which to generate hashtags.
        num_tags (int): The desired number of hashtags to generate.

        Returns:
        str: A string containing the original caption and the generated hashtags.
        """
        MAX_HASHTAGS = 30
        if num_tags > MAX_HASHTAGS:
            num_tags = MAX_HASHTAGS

        # Parse hashtags from the caption
        cleaned_caption, hashtags = self.parse_hashtags()
        num_existing_tags = len(hashtags)

        # Generate additional hashtags if needed
        if num_existing_tags < num_tags:
            additional_hashtags = self.generate_additional_hashtags(
                hashtags, num_tags - num_existing_tags
            )
            hashtags.extend(additional_hashtags)

        # Ensure the number of hashtags does not exceed the maximum limit
        hashtags = hashtags[:num_tags]

        # Construct the result with a line break between the caption and hashtags
        return f"{cleaned_caption}\n\n{' '.join(hashtags)}"
