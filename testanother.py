# Load the initialized ImageCaptionPipeLine class from disk
# Use the function to generate captions for images
from cachemodel.diskcachedmodel import get_image_caption_pipeline
import time
import diskcache

start_time = time.time()
piplin = diskcache.Cache('modelcache').get('image_caption_pipeline')
captiono = piplin("test2.jpg")[0]['generated_text']
elapsed_time = time.time() - start_time
print(f"Caption generation took {elapsed_time} seconds.")
'''captions = get_image_caption_pipeline()("test2.jpg")[0]['generated_text']
elapsed_time = time.time() - start_time
print(f"Caption generation took {elapsed_time:.2f} seconds.")
captions_2 = get_image_caption_pipeline()("test.jpg")[0]['generated_text']
print(captions)
print(captions_2)'''
print(captiono)