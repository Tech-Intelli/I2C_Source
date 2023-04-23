"""Caches the pre-trained model using pickle"""
# pylint: disable=C0103
# pylint: disable=C0415
# pylint: disable=R0903
# pylint: disable=E0401
import os
import pickle
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")


class CachedModel:
    """
    A class that provides a way to cache and retrieve an image caption
    pipeline using pickle.

    Attributes:
        CACHE_DIR (str): The path to the cache directory.
        CACHE_FILE (str): The path to the pickle file where the image caption
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
    CACHE_FILE = os.path.join(CACHE_DIR, "image_caption_pipeline.pkl")

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

        try:
            with open(CachedModel.CACHE_FILE, 'rb') as f:
                image_pipeline = pickle.load(f)
                return image_pipeline(image_path)
        except (FileNotFoundError, pickle.UnpicklingError):
            print(f'''Could not open or find cache file,
                  creating cache file @ {CachedModel.CACHE_FILE}
                  "\nThis may take a while, please wait...''')

        from image_caption import ImageCaptionPipeLine
        image_pipeline = ImageCaptionPipeLine.get_image_caption_pipeline()
        with open(CachedModel.CACHE_FILE, "wb") as f:
            pickle.dump(image_pipeline, f, protocol=pickle.HIGHEST_PROTOCOL)
            print(
                f'''Cache has been created at {CachedModel.CACHE_FILE} successfully.''')
        return image_pipeline(image_path)
