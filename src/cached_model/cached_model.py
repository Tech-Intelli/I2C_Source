"""Caches the pre-trained model using pickle"""
# pylint: disable=C0103
# pylint: disable=C0415
# pylint: disable=R0903
# pylint: disable=E0401
import os
import warnings
from pathlib import Path
import dill
import torch
from torchvision import transforms
from PIL import Image

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

        from image_caption import ImageCaptionPipeLine
        image_pipeline = ImageCaptionPipeLine.get_image_caption_pipeline()
        with open(CachedModel.CACHE_FILE, "wb") as f:
            torch.save(image_pipeline, CachedModel.CACHE_FILE)
            print(
                f'''Cache has been created at {CachedModel.CACHE_FILE} successfully.''')
        return image_pipeline(image_path)

    @staticmethod
    def get_blip2_image_caption_pipeline(image_path):
        """
        Returns the image caption pipeline for the specified image path.
        If the pipeline is not cached, it
        will be created and cached using the
        `ImageCaptionPipeLine.get_blip2_image_caption_pipeline()` method.

        Args:
            image_path (str): The path to the image for which the caption
            pipeline is required.

        Returns:
            The image caption pipeline for the specified image path.
        """
        if torch.cuda.is_available():
            device = torch.device("cuda")
            print("Cuda will be used to generate the caption")
        else:
            device = torch.device("cpu")
            print("CPU will be used to generate the caption")
        try:
            with open(CachedModel.CACHE_FILE_BLIP2, 'rb') as f:
                processor, model = dill.load(f)
                image = Image.open(image_path).convert('RGB')
                inputs = processor(images=image, return_tensors="pt").to(device, torch.float16)
                generated_ids = model.generate(**inputs)
                generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
                return generated_text
        except FileNotFoundError:
            print(f'''Could not open or find cache file,
creating cache file @ {CachedModel.CACHE_FILE_BLIP2}
\nThis may take a while, please wait...''')
        from image_caption import ImageCaptionPipeLine
        processor, model = ImageCaptionPipeLine.get_blip2_image_caption_pipeline()
        with open(CachedModel.CACHE_FILE_BLIP2, "wb") as f:
            dill.dump(model, f)
            print(
                f'''Cache has been created at {CachedModel.CACHE_FILE_BLIP2} successfully.''')
            image = Image.open(image_path).convert('RGB')
            inputs = processor(images=image, return_tensors="pt").to(device, torch.float16)
            generated_ids = model.generate(**inputs)
            generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
            return generated_text