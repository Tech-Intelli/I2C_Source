from cached_model import CachedModel
from image_captioning_pipeline import ImageCaptioningPipeline
from image_captioning_pipeline.vit_pipeline import ViTGPT2Pipeline
from logger import log
import torch


class VITModel(CachedModel):
    """
    Concrete class for caching and retrieving an image caption pipeline.
    """

    def __init__(self):
        super().__init__("image_caption_pipeline.pt", None)
        self.image_captioning_pipeline: ImageCaptioningPipeline = ViTGPT2Pipeline()

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
                image_captioning_pipeline = torch.load(f, map_location=device)
                image = self.load_image(image_path)
                image_input = transform(image).unsqueeze(0).to(device)
                if hasattr(image_captioning_pipeline, "to"):
                    image_captioning_pipeline = image_captioning_pipeline.to(device)
                return image_captioning_pipeline(image_input)
        except FileNotFoundError as e:
            log.error(f"Error loading cached pipeline: {e}")

        log.info(f"Creating cache file @ {CachedModel.CACHE_FILE}, please wait...")
        image_captioning_pipeline = (
            self.image_captioning_pipeline.get_image_caption_pipeline()
        )
        with open(self.cache_file, "wb") as f:
            torch.save(image_captioning_pipeline, f)
            log.info(
                f"""Cache has been created at {CachedModel.CACHE_FILE} successfully."""
            )
        return image_captioning_pipeline(image_path)

    def load_model(self):
        """Loads the model if it's not already cached."""
        if not os.path.exists(self.cache_file):
            print(f"Creating cache file @ {self.cache_file}, please wait...")
            image_captioning_pipeline = (
                self.image_captioning_pipeline.get_image_caption_pipeline()
            )
            with open(self.cache_file, "wb") as f:
                torch.save(image_captioning_pipeline, f)
                print(f"Cache has been created at {self.cache_file} successfully.")
        else:
            print(f"Model loaded from cache @ {self.cache_file}")
