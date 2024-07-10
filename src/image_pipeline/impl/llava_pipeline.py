""" LLAVA Pipeline """

import torch
from transformers import (
    Pipeline,
    AutoProcessor,
    LlavaForConditionalGeneration,
    BitsAndBytesConfig,
)
from image_pipeline.abstract.image_pipeline_abstract import ImageCaptioningPipeline
from configuration_manager.config_manager import ConfigManager


class LlavaPipeline(ImageCaptioningPipeline):
    """
    A class for generating captions from images using the LLAVA model.
    """

    MODEL_NAME = ConfigManager.get_config_manager().get_app_config().multimodal.llava

    _model = None
    _processor = None

    @staticmethod
    def _initialize_llava():
        """
        Initializes the LLAVA model and processor if they have not been initialized yet.

        This method is a static method, which means it can be called directly from the class without creating an instance of the class.

        Parameters:
            None

        Returns:
            None

        Side Effects:
            - If the `_model` attribute of the `LlavaPipeline` class is `None`, the method initializes the `_model` attribute with an instance of the `LlavaForConditionalGeneration` class.
            - If the `_processor` attribute of the `LlavaPipeline` class is `None`, the method initializes the `_processor` attribute with an instance of the `AutoProcessor` class.

        Notes:
            - The `LlavaForConditionalGeneration` class is initialized with the `MODEL_NAME` attribute of the `LlavaPipeline` class.
            - The `AutoProcessor` class is initialized with the `MODEL_NAME` attribute of the `LlavaPipeline` class.
            - The `torch_dtype` parameter of the `LlavaForConditionalGeneration` class is set to `torch.float16`.
            - The `device_map` parameter of the `LlavaForConditionalGeneration` class is set to `"auto"`.
            - The `quantization_config` parameter of the `LlavaForConditionalGeneration` class is set to an instance of the `BitsAndBytesConfig` class with the `load_in_8bit` parameter set to `True` and the `llm_int8_threshold` parameter set to `5.0`.

        Example Usage:
            ```
            LlavaPipeline._initialize_llava()
            ```
        """

        if LlavaPipeline._model is None:
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True, llm_int8_threshold=5.0
            )
            LlavaPipeline._model = LlavaForConditionalGeneration.from_pretrained(
                LlavaPipeline.MODEL_NAME,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                quantization_config=quantization_config,
            )
            LlavaPipeline._processor = AutoProcessor.from_pretrained(
                LlavaPipeline.MODEL_NAME
            )

    def get_image_caption_pipeline(self) -> Pipeline:
        """
        Returns the LlavaPipeline pipeline.

        This function initializes the LlavaPipeline if it hasn't been initialized before,
        and then returns the `_model` attribute of the class.

        Returns:
            Pipeline: The LlavaPipeline pipeline.
        """
        LlavaPipeline._initialize_llava()
        return LlavaPipeline._model

    def get_image_processor(self) -> AutoProcessor:
        """
        Get the image processor for the LlavaPipeline.

        This function initializes the LlavaPipeline if it hasn't been initialized before.
        It then returns the image processor for the pipeline.

        Returns:
            AutoProcessor: The image processor for the LlavaPipeline.
        """
        LlavaPipeline._initialize_llava()
        return LlavaPipeline._processor
