import torch
from transformers import (
    Pipeline,
    AutoProcessor,
    Blip2ForConditionalGeneration,
    BitsAndBytesConfig,
)
from image_captioning_pipeline import ImageCaptioningPipeline


class Blip2Pipeline(ImageCaptioningPipeline):
    """
    A class for generating captions from images using the BLIP2 model.
    """

    MODEL_NAME = "Salesforce/blip2-opt-2.7b"

    _model = None
    _processor = None

    @staticmethod
    def _initialize_blip2():
        """
        Initializes the BLIP2 model and processor if they have not been initialized yet.

        This method is a static method, which means it can be called directly from the class without creating an instance of the class.

        Parameters:
            None

        Returns:
            None

        Side Effects:
            - If the `_model` attribute of the `Blip2ImageCaptioningPipeline` class is `None`, the method initializes the `_model` attribute with an instance of the `Blip2ForConditionalGeneration` class.
            - If the `_processor` attribute of the `Blip2ImageCaptioningPipeline` class is `None`, the method initializes the `_processor` attribute with an instance of the `AutoProcessor` class.

        Notes:
            - The `Blip2ForConditionalGeneration` class is initialized with the `MODEL_NAME` attribute of the `Blip2ImageCaptioningPipeline` class.
            - The `AutoProcessor` class is initialized with the `MODEL_NAME` attribute of the `Blip2ImageCaptioningPipeline` class.
            - The `torch_dtype` parameter of the `Blip2ForConditionalGeneration` class is set to `torch.float16`.
            - The `device_map` parameter of the `Blip2ForConditionalGeneration` class is set to `"auto"`.
            - The `quantization_config` parameter of the `Blip2ForConditionalGeneration` class is set to an instance of the `BitsAndBytesConfig` class with the `load_in_8bit` parameter set to `True` and the `llm_int8_threshold` parameter set to `5.0`.

        Example Usage:
            ```
            Blip2ImageCaptioningPipeline._initialize_blip2()
            ```
        """
       
        if Blip2ImageCaptioningPipeline._model is None:
            quantization_config = BitsAndBytesConfig(
                load_in_8bit=True, llm_int8_threshold=5.0
            )
            Blip2Pipeline._model = Blip2ForConditionalGeneration.from_pretrained(
                Blip2Pipeline.MODEL_NAME,
                torch_dtype=torch.float16,
                device_map="auto",
                quantization_config=quantization_config,
            )
            Blip2Pipeline._processor = AutoProcessor.from_pretrained(
                Blip2Pipeline.MODEL_NAME
            )

    def get_image_caption_pipeline(self) -> Pipeline:
        """
        Returns the Blip2ImageCaptioningPipeline pipeline.

        This function initializes the Blip2ImageCaptioningPipeline if it hasn't been initialized before,
        and then returns the `_model` attribute of the class.

        Returns:
            Pipeline: The Blip2ImageCaptioningPipeline pipeline.
        """
        Blip2Pipeline._initialize_blip2()
        return Blip2Pipeline._model

    def get_image_processor(self) -> AutoProcessor:
        """
        Get the image processor for the Blip2ImageCaptioningPipeline.

        This function initializes the Blip2ImageCaptioningPipeline if it hasn't been initialized before.
        It then returns the image processor for the pipeline.

        Returns:
            AutoProcessor: The image processor for the Blip2ImageCaptioningPipeline.
        """
        Blip2Pipeline._initialize_blip2()
        return Blip2Pipeline._processor
