"""Caches the pre-trained model using pickle"""
# pylint: disable=C0103
# pylint: disable=C0415
# pylint: disable=R0903
# pylint: disable=E0401
import os
import warnings
from pathlib import Path
import torch

warnings.filterwarnings("ignore")


class CachedModel:
    """
    A class that provides a way to cache and retrieve an image caption
    pipeline using PyTorch's native serialization methods.

    Attributes:
        CACHE_DIR (str): The path to the cache directory.
        CACHE_FILE (str): The path to the file where the image caption
        pipeline is stored.

    Methods:
        get_image_caption_pipeline(image_path: str) -> ImageCaptionPipeLine:
            Returns the image caption pipeline for the specified image path.
            If the pipeline is not cached, it
            will be created and cached using the
            `ImageCaptionPipeLine.get_image_caption_pipeline()` method.
    """

    CACHE_DIR = os.path.join(Path.cwd(), ".cache")
    Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)
    CACHE_FILE = os.path.join(CACHE_DIR, "image_caption_pipeline.pt")

    @staticmethod
    def get_image_caption_pipeline(image_path):
        """
        Returns the image caption pipeline for the specified image path.
        If the pipeline is not cached, it
        will be created and cached using the
        `ImageCaptionPipeLine.get_image_caption_pipeline()` method.

        Args:
            image_path (str): The path to the image for which the caption
            pipeline is required.

        Returns:
            The image caption pipeline for the specified image path.
        """

        device = None
        if torch.cuda.is_available():
            device = torch.device("cuda")
            print("Cuda will be used to generate the caption")
        else:
            device = torch.device("cpu")
            print("CPU will be used to generate the caption")

        try:
            with open(CachedModel.CACHE_FILE, 'rb') as f:
                image_pipeline = torch.load(f, map_location=device)
                return image_pipeline(image_path)
        except FileNotFoundError:
            print(f'''Could not open or find cache file,
creating cache file @ {CachedModel.CACHE_FILE}
\nThis may take a while, please wait...''')

        from image_caption import ImageCaptionPipeLine
        image_pipeline = ImageCaptionPipeLine.get_image_caption_pipeline()
        with open(CachedModel.CACHE_FILE, "wb") as f:
            torch.save(image_pipeline, CachedModel.CACHE_FILE)
            print(
                f'''Cache has been created at {CachedModel.CACHE_FILE} successfully.''')
        return image_pipeline(image_path)
