import os
import pickle
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

CACHE_DIR = os.path.join(Path.home(), ".cache")
Path(CACHE_DIR).mkdir(parents=True, exist_ok=True)
CACHE_FILE = os.path.join(CACHE_DIR, "image_caption_pipeline.pkl")


def get_image_caption_pipeline(image_path):
    try:
        with open(CACHE_FILE, 'rb') as f:
            image_pipeline = pickle.load(f)
            return image_pipeline(image_path)
    except (FileNotFoundError, pickle.UnpicklingError):
        print("Could not open or find cache file, creating."
              "\nThis may take a while, please wait...")

    from imagecaption.imagecaption import ImageCaptionPipeLine
    image_pipeline = ImageCaptionPipeLine.get_image_caption_pipeline()
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(image_pipeline, f, protocol=pickle.HIGHEST_PROTOCOL)

    return image_pipeline(image_path)
