from abstracts.inference_abstract import InferenceAbstract
from abstracts.image_pipeline_abstract import ImageCaptioningPipeline
from image_pipeline.vit_pipeline import ViTGPT2Pipeline
from utils.logger import log
import torch


class VITModel(InferenceAbstract):
    """
    Concrete class for caching and retrieving an image caption pipeline.
    """

    def __init__(self):
        super().__init__(None)
        self.image_pipeline: ImageCaptioningPipeline = ViTGPT2Pipeline()

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

        log.info(
            f"Creating cache file @ {InferenceAbstract.CACHE_FILE}, please wait..."
        )
        image_pipeline = self.image_pipeline.get_image_caption_pipeline()
        with open(self.cache_file, "wb") as f:
            torch.save(image_pipeline, f)
            log.info(
                f"""Cache has been created at {InferenceAbstract.CACHE_FILE} successfully."""
            )
        return image_pipeline(image_path)

    def load_model(self):
        """Loads the model if it's not already cached."""
        if not os.path.exists(self.cache_file):
            print(f"Creating cache file @ {self.cache_file}, please wait...")
            image_pipeline = self.image_pipeline.get_image_caption_pipeline()
            with open(self.cache_file, "wb") as f:
                torch.save(image_pipeline, f)
                print(f"Cache has been created at {self.cache_file} successfully.")
        else:
            print(f"Model loaded from cache @ {self.cache_file}")
