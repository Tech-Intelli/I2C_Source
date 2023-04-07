from joblib import dump, load
from imagecaption.imagecaption import ImageCaptionPipeLine

# Initialize the ImageCaptionPipeLine class and create a pipeline object
image_caption_pipeline = ImageCaptionPipeLine.get_image_caption_pipeline()

# Save the initialized ImageCaptionPipeLine class to disk
dump(image_caption_pipeline, 'image_caption_pipeline.joblib')
