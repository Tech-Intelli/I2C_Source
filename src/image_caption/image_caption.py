"""
Creates a Transformer pipeline from a pre-trained model

    Returns:
        Pipeline: Image caption pipeline
"""

# pylint: disable=E0401
# pylint: disable=E1101
# pylint: disable=R0903

import warnings
import torch
from transformers import (
    VisionEncoderDecoderModel,
    ViTImageProcessor,
    AutoTokenizer,
    Pipeline,
    pipeline,
    AutoProcessor,
    Blip2ForConditionalGeneration,
    BitsAndBytesConfig,
)

warnings.filterwarnings("ignore")


class ImageCaptionPipeLine:
    """
    A pipeline class for generating captions from images using the ViT-GPT2 image captioning model.
    """

    # Class variables to hold the pre-trained model, feature extractor, and tokenizer
    MODEL_NAME = "nlpconnect/vit-gpt2-image-captioning"
    BLIP2_MODEL_NAME = "Salesforce/blip2-opt-2.7b"

    # Lazy initialization for these attributes to avoid loading them unnecessarily
    _model = None
    _feature_extractor = None
    _tokenizer = None
    _blip2_model = None
    _blip2_processor = None

    @staticmethod
    def _initialize_vit_gpt2():
        """Initializes the ViT-GPT2 model, feature extractor, and tokenizer if not already initialized."""
        if ImageCaptionPipeLine._model is None:
            ImageCaptionPipeLine._model = VisionEncoderDecoderModel.from_pretrained(
                ImageCaptionPipeLine.MODEL_NAME
            )
            ImageCaptionPipeLine._feature_extractor = ViTImageProcessor.from_pretrained(
                ImageCaptionPipeLine.MODEL_NAME
            )
            ImageCaptionPipeLine._tokenizer = AutoTokenizer.from_pretrained(
                ImageCaptionPipeLine.MODEL_NAME
            )

    @staticmethod
    def get_image_caption_pipeline() -> Pipeline:
        """
        Returns a pipeline for generating captions from images.
        """
        ImageCaptionPipeLine._initialize_vit_gpt2()
        image_caption_pipeline = pipeline(
            "image-to-text",
            model=ImageCaptionPipeLine.model,
            tokenizer=ImageCaptionPipeLine.tokenizer,
            feature_extractor=ImageCaptionPipeLine.feature_extractor,
            image_processor=ImageCaptionPipeLine.feature_extractor,
        )
        return image_caption_pipeline

    @staticmethod
    def get_blip2_image_caption_pipeline():
        """
        Returns a pipeline for generating captions from images
        using the BLIP2 model.
        """
        quantization_config = BitsAndBytesConfig(load_in_8bit=True, llm_int8_threshold=5.0)
        model = Blip2ForConditionalGeneration.from_pretrained(
            ImageCaptionPipeLine.BLIP2_MODEL_NAME,
            torch_dtype=torch.float16,
            device_map="auto",
            quantization_config=quantization_config,
        )
        return model

    @staticmethod
    def get_blip2_image_processor() -> AutoProcessor:
        """
        Returns the image processor for the BLIP2 model.
        """
        if ImageCaptionPipeLine._blip2_processor is None:
            ImageCaptionPipeLine._blip2_processor = AutoProcessor.from_pretrained(
                ImageCaptionPipeLine.BLIP2_MODEL_NAME
            )
        return ImageCaptionPipeLine._blip2_processor
