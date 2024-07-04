"""Concrete class for caching and retrieving the BLIP2 image caption pipeline."""

import os
import gc
import concurrent.futures
import torch
from src.inference.inference_abstract import InferenceAbstract
from image_pipeline import ImageCaptioningPipeline
from image_pipeline.blip2_pipeline import Blip2Pipeline
from vector_store import get_unique_image_id
from vector_store import add_image_to_chroma


class Blip2Model(InferenceAbstract):
    """
    Concrete class for caching and retrieving the BLIP2 image caption pipeline.
    """

    BLIP2_MODEL = None
    BLIP2_PROCESSOR = None

    def __init__(self, collection):
        super().__init__("blip2_8bit.pkl", collection)
        self.image_pipeline: ImageCaptioningPipeline = Blip2Pipeline()

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
        image = InferenceAbstract.load_image(image_path)
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
            self.image_pipeline.get_image_processor()
            if Blip2Model.BLIP2_PROCESSOR is None
            else Blip2Model.BLIP2_PROCESSOR
        )
        Blip2Model.BLIP2_MODEL = (
            self.image_pipeline.get_image_caption_pipeline()
            if Blip2Model.BLIP2_MODEL is None
            else Blip2Model.BLIP2_MODEL
        )
        return Blip2Model.BLIP2_MODEL
