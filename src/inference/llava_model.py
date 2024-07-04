"""Concrete class for caching and retrieving the LLAVA image caption pipeline."""

import os
import gc
import concurrent.futures
import torch
from inference.inference_abstract import InferenceAbstract
from image_pipeline import ImageCaptioningPipeline
from image_pipeline.llava_pipeline import LlavaPipeline
from vector_store import get_unique_image_id
from vector_store import add_image_to_chroma


class LlavaModel(InferenceAbstract):
    """
    Concrete class for caching and retrieving the LLAVA image caption pipeline.
    """

    LLAVA_MODEL = None
    LLAVA_PROCESSOR = None

    def __init__(self, collection):
        super().__init__(collection)
        self.image_pipeline: ImageCaptioningPipeline = LlavaPipeline()

    def get_image_caption_pipeline(self, image_path):
        """
        Returns the image caption pipeline for the specified image path.
        If the pipeline is not cached, it
        will be created and cached using the
        `ImageCaptionPipeLine.get_image_caption_pipeline()` method.

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
        inputs = LlavaModel.LLAVA_PROCESSOR("USER: <image>\nWhat are these?\nASSISTANT:", images=image, return_tensors="pt").to(
            device, torch.float16
        )
        generated_ids = LlavaModel.LLAVA_MODEL.generate(**inputs, max_new_tokens=200, do_sample=False)
        generated_text = LlavaModel.LLAVA_PROCESSOR.batch_decode(
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
        Loads the LLAVA model if it's not already cached.

        This function checks if the LLAVA_MODEL and LLAVA_PROCESSOR attributes of the LlavaModel class are None.
        If they are, it initializes them by calling the get_blip2_image_processor() and get_image_caption_pipeline()
        methods from the ImageCaptionPipeLine class. It then saves the LLAVA_MODEL and LLAVA_PROCESSOR attributes to a
        cache file specified by the cache_file attribute of the current instance.

        If the LLAVA_MODEL and LLAVA_PROCESSOR attributes are not None, it prints a message indicating that the model has been loaded from the cache.

        Parameters:
            self (LlavaModel): The current instance of the LlavaModel class.

        Returns:
            None
        """
        LlavaModel.LLAVA_PROCESSOR = (
            self.image_pipeline.get_image_processor()
            if LlavaModel.LLAVA_PROCESSOR is None
            else LlavaModel.LLAVA_PROCESSOR
        )
        LlavaModel.LLAVA_MODEL = (
            self.image_pipeline.get_image_caption_pipeline()
            if LlavaModel.LLAVA_MODEL is None
            else LlavaModel.LLAVA_MODEL
        )
        return LlavaModel.LLAVA_MODEL
