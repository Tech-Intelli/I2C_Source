import torch
from transformers import (
    Pipeline,
    AutoProcessor,
    Blip2ForConditionalGeneration,
    BitsAndBytesConfig
)
from image_caption import ImageCaptioningPipeline

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
