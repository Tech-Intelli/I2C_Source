"""Caches the pre-trained model using pickle"""
# pylint: disable=C0103
# pylint: disable=C0415
# pylint: disable=R0903
# pylint: disable=E0401
import os
import gc
import pickle
import warnings
import concurrent.futures
from pathlib import Path
import dill
import torch
from torchvision import transforms
from PIL import Image
from image_caption import ImageCaptionPipeLine
from chromadb_vector_store import get_unique_image_id
from chromadb_vector_store import add_image_to_chroma

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
    CACHE_FILE_BLIP2 = os.path.join(CACHE_DIR, "blip2_8bit.pkl")
    BLIP2_MODEL = None
    BLIP2_PROCESSOR = None

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

        device = "cpu"
        # pylint: disable=E1101
        # pylint: disable=W0105
        '''
        if torch.cuda.is_available():
            device = torch.device("cuda")
            print("Cuda will be used to generate the caption")
        else:
            device = torch.device("cpu")
            print("CPU will be used to generate the caption")
        '''
        transform = transforms.Resize((256, 256))
        try:
            with open(CachedModel.CACHE_FILE, 'rb') as f:
                image_pipeline = torch.load(f, map_location=device)
                image = Image.open(image_path)
                image_input = transform(image)
                if hasattr(image_pipeline, 'to'):
                    image_pipeline = image_pipeline.to(device)
                return image_pipeline(image_input)
        except FileNotFoundError:
            print(f'''Could not open or find cache file,
creating cache file @ {CachedModel.CACHE_FILE}
\nThis may take a while, please wait...''')
        image_pipeline = ImageCaptionPipeLine.get_image_caption_pipeline()
        with open(CachedModel.CACHE_FILE, "wb") as f:
            torch.save(image_pipeline, CachedModel.CACHE_FILE)
            print(
                f'''Cache has been created at {CachedModel.CACHE_FILE} successfully.''')
        return image_pipeline(image_path)

    @staticmethod
    def get_blip2_image_caption_pipeline(image_path, device = 'cpu', collection = None):
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
        os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128'
        image = Image.open(image_path).convert('RGB')
        # pylint: disable=E1102
        inputs = CachedModel.BLIP2_PROCESSOR(
            images=image,
            return_tensors="pt").to(device, torch.float16)
        generated_ids = CachedModel.BLIP2_MODEL.generate(**inputs)
        generated_text = CachedModel.BLIP2_PROCESSOR.batch_decode(
            generated_ids,
            skip_special_tokens=True)[0].strip()
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        gc.collect()
        pixel_values = inputs['pixel_values']
        with concurrent.futures.ThreadPoolExecutor() as executor:
            unique_id_future = executor.submit(get_unique_image_id, pixel_values)
            def store_in_chroma_db(fut, collection, pixel_values, generated_text):
                unique_id = fut.result()
                add_image_to_chroma(
                    collection,
                    unique_id,
                    pixel_values,
                    generated_text)
            unique_id_future.add_done_callback(lambda fut: store_in_chroma_db(
                fut,
                collection,
                pixel_values,
                generated_text))
            del inputs
        del generated_ids
        return generated_text

    @staticmethod
    def load_blip2():
        """
        Load the blip2 image caption model.
        If the pipeline is not cached, it
        will be created and cached using the
        `ImageCaptionPipeLine.get_blip2_image_caption_pipeline()` method.

        Args:
            None.

        Returns:
            None.
        """
        """
        try:
            with open(CachedModel.CACHE_FILE_BLIP2, 'rb') as f:
                print("BLIP2 model loading from the cache started.")
                CachedModel.BLIP2_PROCESSOR = ImageCaptionPipeLine.get_blip2_image_processor()
                unpickler = pickle.Unpickler(f)
                CachedModel.BLIP2_MODEL = unpickler.load()
                print("BLIP2 model loaded from the cache successfully.")
                return CachedModel.BLIP2_MODEL
        except FileNotFoundError:
            print(f'''Could not open or find cache file,
creating cache file @ {CachedModel.CACHE_FILE_BLIP2} 
\nThis may take a while, please wait...''')
        CachedModel.BLIP2_PROCESSOR = ImageCaptionPipeLine.get_blip2_image_processor()
        CachedModel.BLIP2_MODEL = ImageCaptionPipeLine.get_blip2_image_caption_pipeline()
        with open(CachedModel.CACHE_FILE_BLIP2, "wb") as f:
            dill.dump(CachedModel.BLIP2_MODEL, f)
            print(
                f'''Cache has been created at
{CachedModel.CACHE_FILE_BLIP2} successfully.''')
        print("BLIP2 model loaded successfully")
        return CachedModel.BLIP2_MODEL
        """
        CachedModel.BLIP2_PROCESSOR = ImageCaptionPipeLine.get_blip2_image_processor()
        CachedModel.BLIP2_MODEL = ImageCaptionPipeLine.get_blip2_image_caption_pipeline()
        return CachedModel.BLIP2_MODEL
