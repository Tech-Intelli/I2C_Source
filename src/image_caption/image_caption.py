"""
Creates a Transformer pipeline from a pre-trained model

    Returns:
        Pipeline: Image caption pipeline
"""

import warnings
from abc import ABC, abstractmethod
from transformers import (
    Pipeline,
    AutoProcessor
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
