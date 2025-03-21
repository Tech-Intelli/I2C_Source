from captioning.abstract.generate_caption_abstract import CaptionGenerator
from inference.abstract.inference_abstract import InferenceAbstract


class ImageCaptionGenerator(CaptionGenerator):
    """
    A class that generates captions for images using a chatbot.
    """

    def generate_caption(
        self,
        image_path,
        caption_size,
        context,
        style,
        content_type,
        influencer,
        num_hashtags,
        tone,
        social_media,
        inference: InferenceAbstract = None,
    ):
        """
        Generates a caption for an image using the chatbot object.

        Args:
        - image_path (str): The path of the image for which the caption is to be generated.
        - caption_size (str): The size of the caption to be generated.
        - context (str): The context in which the caption is to be written.
        - style (str): The style in which the caption is to be written.
        - num_hashtags (int): The number of hashtags to be included in the caption.

        Returns:
        - response_json (JSON object): The JSON object containing the generated caption.
        - compressed_image_path (str): The path of the compressed image used for generating the caption.
        """
        compressed_image_path = image_path
        imagetotext = inference.get_image_caption_pipeline(image_path)
        content = self.generate_content_new(
            imagetotext,
            caption_size,
            context,
            style,
            tone,
            content_type,
            influencer,
            num_hashtags,
            social_media,
        )
        stream_caption = self._generate_caption_with_hashtags(content, num_hashtags)
        return stream_caption, compressed_image_path
