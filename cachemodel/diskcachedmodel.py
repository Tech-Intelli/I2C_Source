import os
import pickle
import warnings

warnings.filterwarnings("ignore")


def get_image_caption_pipeline(image_path):
    # Define a cache that stores data on disk
    image_pipeline = None
    cache_file = "CACHED_FILE.pkl"
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            print("Preloaded from Pickle Cache")
            image_pipeline = pickle.load(f)
            print("Preloaded from Pickle Cache done")
            return image_pipeline(image_path)
    else:
        print("Preloaded Cache is not accessible,"
              " hence cache_data is being created.")
        from imagecaption.imagecaption import ImageCaptionPipeLine
        image_pipeline = ImageCaptionPipeLine.get_image_caption_pipeline()
        with open(cache_file, "wb") as f:
            pickle.dump(image_pipeline, f, protocol=pickle.HIGHEST_PROTOCOL)
        return image_pipeline(image_path)
