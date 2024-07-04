"""Caches the pre-trained model using pickle"""

import os
import warnings
from abc import ABC, abstractmethod
from pathlib import Path
import torch
from torchvision import transforms
from PIL import Image

warnings.filterwarnings("ignore")


class InferenceAbstract(ABC):
    """
    Abstract base class for caching and retrieving models.

    Methods:
        get_image_caption_pipeline(image_path: str) -> ImageCaptionPipeLine:
            Abstract method to be implemented for retrieving the image caption pipeline.
    """

    def __init__(self, collection):
        """
        Initializes a new instance of the InferenceAbstract class.

        Args:
            collection (str): The name of the chromadb collection.

        Returns:
            None
        """
        self.collection = collection

    @staticmethod
    def get_device():
        """Returns the device to be used for PyTorch operations."""
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @staticmethod
    def get_transform():
        """Returns the composed transform for image preprocessing."""
        return transforms.Compose(
            [
                transforms.Resize((256, 256)),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
            ]
        )

    @staticmethod
    def load_image(image_path):
        """Loads an image from the specified path and returns it."""
        return Image.open(image_path).convert("RGB")

    @abstractmethod
    def get_image_caption_pipeline(self, image_path):
        pass

    @abstractmethod
    def load_model(self):
        pass
