"""
Creates a Transformer pipeline from a pre-trained model

    Returns:
        Pipeline: Image caption pipeline
"""
# pylint: disable=E0401

import warnings
from transformers import VisionEncoderDecoderModel
from transformers import ViTImageProcessor
from transformers import AutoTokenizer
from transformers import Pipeline
from transformers import pipeline

warnings.filterwarnings("ignore")
# pylint: disable=E1101
# pylint: disable=R0903


class ImageCaptionPipeLine:
    """
    A pipeline class for generating captions from images using the ViT-GPT2 image captioning model.
    """

    model = VisionEncoderDecoderModel.from_pretrained(
        "nlpconnect/vit-gpt2-image-captioning")
    feature_extractor = ViTImageProcessor.from_pretrained(
        "nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained(
        "nlpconnect/vit-gpt2-image-captioning")

    @staticmethod
    def get_image_caption_pipeline() -> Pipeline:
        """
        Returns a pipeline for generating captions from images.
        """

        image_caption_pipeline = pipeline(
            "image-to-text",
            model=ImageCaptionPipeLine.model,
            tokenizer=ImageCaptionPipeLine.tokenizer,
            feature_extractor=ImageCaptionPipeLine.feature_extractor,
            image_processor=ImageCaptionPipeLine.feature_extractor)
        return image_caption_pipeline
