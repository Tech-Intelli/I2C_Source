"""Caches the pre-trained model using pickle"""

import os
import gc
import warnings
import concurrent.futures
from abc import ABC, abstractmethod
from pathlib import Path
import torch
from torchvision import transforms
from PIL import Image
from image_caption import ImageCaptionPipeLine
from chromadb_vector_store import get_unique_image_id
from chromadb_vector_store import add_image_to_chroma
from logger import log

warnings.filterwarnings("ignore")


class CachedModel(ABC):
    """
    Abstract base class for caching and retrieving models.

    Methods:
        get_image_caption_pipeline(image_path: str) -> ImageCaptionPipeLine:
            Abstract method to be implemented for retrieving the image caption pipeline.
    """

    CACHE_DIR = os.path.join(Path.cwd(), ".cache")
    Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)

    def __init__(self, cache_file, collection):
        """
        Initializes a new instance of the CachedModel class.

        Args:
            cache_file (str): The name of the cache file.
            collection (str): The name of the chromadb collection.

        Returns:
            None
        """
        self.cache_file = os.path.join(self.CACHE_DIR, cache_file)
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


class ImageCaptionModel(CachedModel):
    """
    Concrete class for caching and retrieving an image caption pipeline.
    """

    def __init__(self):
        super().__init__("image_caption_pipeline.pt", None)

    def get_image_caption_pipeline(self, image_path):
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
        device = self.get_device()
        transform = self.get_transform()

        try:
            with open(self.cache_file, "rb") as f:
                image_pipeline = torch.load(f, map_location=device)
                image = self.load_image(image_path)
                image_input = transform(image).unsqueeze(0).to(device)
                if hasattr(image_pipeline, "to"):
                    image_pipeline = image_pipeline.to(device)
                return image_pipeline(image_input)
        except FileNotFoundError as e:
            log.error(f"Error loading cached pipeline: {e}")

        log.info(f"Creating cache file @ {CachedModel.CACHE_FILE}, please wait...")

        image_pipeline = ImageCaptionPipeLine.get_image_caption_pipeline()
        with open(self.cache_file, "wb") as f:
            torch.save(image_pipeline, f)
            log.info(
                f"""Cache has been created at {CachedModel.CACHE_FILE} successfully."""
            )
        return image_pipeline(image_path)

    def load_model(self):
        """Loads the model if it's not already cached."""
        if not os.path.exists(self.cache_file):
            print(f"Creating cache file @ {self.cache_file}, please wait...")
            image_pipeline = ImageCaptionPipeLine.get_image_caption_pipeline()
            with open(self.cache_file, "wb") as f:
                torch.save(image_pipeline, f)
                print(f"Cache has been created at {self.cache_file} successfully.")
        else:
            print(f"Model loaded from cache @ {self.cache_file}")


class Blip2Model(CachedModel):
    """
    Concrete class for caching and retrieving the BLIP2 image caption pipeline.
    """

    BLIP2_MODEL = None
    BLIP2_PROCESSOR = None

    def __init__(self, collection):
        super().__init__("blip2_8bit.pth", collection)

    def get_image_caption_pipeline(self, image_path):
        """
        Returns the image caption pipeline for the specified image path.
        If the pipeline is not cached, it
        will be created and cached using the
        `ImageCaptionPipeLine.get_blip2_image_caption_pipeline()` method.

        Args:
            image_path (str): The path to the image for which the caption
            pipeline is required.
            device (str): The device on which the model and the inputs will be loaded.
        Returns:
            The image caption pipeline for the specified image path.
        """
        device = self.get_device()
        os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
        image = CachedModel.load_image(image_path)
        inputs = Blip2Model.BLIP2_PROCESSOR(images=image, return_tensors="pt").to(
            device, torch.float16
        )
        generated_ids = Blip2Model.BLIP2_MODEL.generate(**inputs)
        generated_text = Blip2Model.BLIP2_PROCESSOR.batch_decode(
            generated_ids, skip_special_tokens=True
        )[0].strip()

        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        gc.collect()

        pixel_values = inputs["pixel_values"]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            unique_id_future = executor.submit(get_unique_image_id, pixel_values)

            def store_in_chroma_db(fut, collection, pixel_values, generated_text):
                unique_id = fut.result()
                add_image_to_chroma(collection, unique_id, pixel_values, generated_text)

            unique_id_future.add_done_callback(
                lambda fut: store_in_chroma_db(
                    fut, self.collection, pixel_values, generated_text
                )
            )
            del inputs
        del generated_ids
        return generated_text

    def load_model(self):
        """
        Loads the BLIP2 model if it's not already cached.

        This function checks if the BLIP2_MODEL and BLIP2_PROCESSOR attributes of the Blip2Model class are None.
        If they are, it initializes them by calling the get_blip2_image_processor() and get_blip2_image_caption_pipeline()
        methods from the ImageCaptionPipeLine class. It then saves the BLIP2_MODEL and BLIP2_PROCESSOR attributes to a
        cache file specified by the cache_file attribute of the current instance.

        If the BLIP2_MODEL and BLIP2_PROCESSOR attributes are not None, it prints a message indicating that the model has been loaded from the cache.

        Parameters:
            self (Blip2Model): The current instance of the Blip2Model class.

        Returns:
            None
        """
        Blip2Model.BLIP2_PROCESSOR = (
            ImageCaptionPipeLine.get_blip2_image_processor()
            if Blip2Model.BLIP2_PROCESSOR is None
            else Blip2Model.BLIP2_PROCESSOR
        )
        Blip2Model.BLIP2_MODEL = (
            ImageCaptionPipeLine.get_blip2_image_caption_pipeline()
            if Blip2Model.BLIP2_MODEL is None
            else Blip2Model.BLIP2_MODEL
        )
        return Blip2Model.BLIP2_MODEL
