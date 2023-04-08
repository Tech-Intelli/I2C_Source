# Load the initialized ImageCaptionPipeLine class from disk
# Use the function to generate captions for images
import time
import warnings
warnings.filterwarnings("ignore")
from cachemodel.diskcachedmodel import get_image_caption_pipeline

for val in list:
    start_time = time.time()
    piplin = get_image_caption_pipeline(val)
    #caption = piplin("test2.jpg")[0]['generated_text']
    elapsed_time = time.time() - start_time
    print(f"Caption generation took {elapsed_time} seconds.")
#print(caption)
