import diskcache
from imagecaption.imagecaption import ImageCaptionPipeLine
from transformers import Pipeline

# Define a cache that stores data on disk
cache = diskcache.Cache('modelcache')


def get_image_caption_pipeline() -> Pipeline:
    # Use the model path as the key for the cache
    key = 'image_caption_pipeline'

    # Try to get the pipeline from the cache
    pipeline = cache.get(key)

    if pipeline is None:
        # If the pipeline is not in the cache, create a new one
        pipeline = ImageCaptionPipeLine.get_image_caption_pipeline()

        # Store the pipeline in the cache
        cache.set(key, pipeline)

        print("New model loaded")
    else:
        print("Model loaded from cache")
    return pipeline
