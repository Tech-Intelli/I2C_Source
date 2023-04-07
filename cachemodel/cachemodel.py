from imagecaption.imagecaption import ImageCaptionPipeLine
from cachetools import cached, TTLCache
from transformers import Pipeline


# Define a cache with a TTL (time-to-live) of 1 hour
cache = TTLCache(maxsize=10000, ttl=3600)


# Define a function to get the image caption pipeline
@cached(cache)
def get_image_caption_pipeline() -> Pipeline:
    image_caption_pipeline = ImageCaptionPipeLine.get_image_caption_pipeline()
    if cache.currsize == 0:
        print("New model loaded")
    else:
        print("Model loaded from cache")
    return image_caption_pipeline
