"""
Creates a Transformer pipeline from a pre-trained model

    Returns:
        Pipeline: Image caption pipeline
"""
# pylint: disable=E0401

import warnings
import torch
from transformers import \
    VisionEncoderDecoderModel,\
    ViTImageProcessor,\
    AutoTokenizer,\
    Pipeline,\
    pipeline,\
    AutoProcessor,\
    Blip2ForConditionalGeneration,\
    BitsAndBytesConfig

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

    @staticmethod
    def get_blip2_image_caption_pipeline():
        """
        Returns a pipeline for generating captions from images
        using the BLIP2 model.
        """
        quantization_config = BitsAndBytesConfig(load_in_8bit=True)
        model = Blip2ForConditionalGeneration.from_pretrained(
            "Salesforce/blip2-opt-2.7b",
            torch_dtype=torch.float16,
            device_map="auto",
            quantization_config=quantization_config)
        return model

    @staticmethod
    def get_blip2_image_processor():
        """
        Returns Salesforce/blip2-opt-2.7b's image processor.
        """
        return AutoProcessor.from_pretrained("Salesforce/blip2-opt-2.7b")
