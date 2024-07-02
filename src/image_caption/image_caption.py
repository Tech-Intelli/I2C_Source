"""
Creates a Transformer pipeline from a pre-trained model

    Returns:
        Pipeline: Image caption pipeline
"""

import warnings
import torch
from abc import ABC, abstractmethod
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

class ImageCaptioningPipeline(ABC):
    """
    Abstract base class for image captioning models.
    """

    @abstractmethod
    def get_image_caption_pipeline(self) -> Pipeline:
        """
        Abstract method to get the image caption pipeline.
        """
        pass

    @abstractmethod
    def get_image_processor(self) -> AutoProcessor:
        """
        Abstract method to get the image processor.
        """
        pass


class ViTGPT2ImageCaptioningPipeline(ImageCaptioningPipeline):
    """
    A class for generating captions from images using the ViT-GPT2 image captioning model.
    """

    MODEL_NAME = "nlpconnect/vit-gpt2-image-captioning"

    _model = None
    _feature_extractor = None
    _tokenizer = None

    @staticmethod
    def _initialize_vit_gpt2():
        """Initializes the ViT-GPT2 model, feature extractor, and tokenizer if not already initialized."""
        if ViTGPT2ImageCaptioningPipeline._model is None:
            ViTGPT2ImageCaptioningPipeline._model = VisionEncoderDecoderModel.from_pretrained(
                ViTGPT2ImageCaptioningPipeline.MODEL_NAME
            )
            ViTGPT2ImageCaptioningPipeline._feature_extractor = ViTImageProcessor.from_pretrained(
                ViTGPT2ImageCaptioningPipeline.MODEL_NAME
            )
            ViTGPT2ImageCaptioningPipeline._tokenizer = AutoTokenizer.from_pretrained(
                ViTGPT2ImageCaptioningPipeline.MODEL_NAME
            )

    def get_image_caption_pipeline(self) -> Pipeline:
        """
        Returns a pipeline for generating captions from images.
        """
        ViTGPT2ImageCaptioningPipeline._initialize_vit_gpt2()
        image_caption_pipeline = pipeline(
            "image-to-text",
            model=ViTGPT2ImageCaptioningPipeline._model,
            tokenizer=ViTGPT2ImageCaptioningPipeline._tokenizer,
            feature_extractor=ViTGPT2ImageCaptioningPipeline._feature_extractor,
            image_processor=ViTGPT2ImageCaptioningPipeline._feature_extractor,
        )
        return image_caption_pipeline

    def get_image_processor(self) -> AutoProcessor:
        """
        Returns the image processor for the ViT-GPT2 model.
        """
        ViTGPT2ImageCaptioningPipeline._initialize_vit_gpt2()
        return ViTGPT2ImageCaptioningPipeline._feature_extractor


class Blip2ImageCaptioningPipeline(ImageCaptioningPipeline):
    """
    A class for generating captions from images using the BLIP2 model.
    """

    MODEL_NAME = "Salesforce/blip2-opt-2.7b"

    _model = None
    _processor = None

    @staticmethod
    def _initialize_blip2():
        """Initializes the BLIP2 model and processor if not already initialized."""
        if Blip2ImageCaptioningPipeline._model is None:
            quantization_config = BitsAndBytesConfig(
                load_in_8bit=True, llm_int8_threshold=5.0
            )
            Blip2ImageCaptioningPipeline._model = Blip2ForConditionalGeneration.from_pretrained(
                Blip2ImageCaptioningPipeline.MODEL_NAME,
                torch_dtype=torch.float16,
                device_map="auto",
                quantization_config=quantization_config,
            )
            Blip2ImageCaptioningPipeline._processor = AutoProcessor.from_pretrained(
                Blip2ImageCaptioningPipeline.MODEL_NAME
            )

    def get_image_caption_pipeline(self) -> Pipeline:
        """
        Returns a pipeline for generating captions from images
        using the BLIP2 model.
        """
        Blip2ImageCaptioningPipeline._initialize_blip2()
        return Blip2ImageCaptioningPipeline._model

    def get_image_processor(self) -> AutoProcessor:
        """
        Returns the image processor for the BLIP2 model.
        """
        Blip2ImageCaptioningPipeline._initialize_blip2()
        return Blip2ImageCaptioningPipeline._processor
