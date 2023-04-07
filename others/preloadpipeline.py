import pickle
from imagecaption.imagecaption import ImageCaptionPipeLine
# create an instance of the ImageCaptionPipeLine class
image_caption_pipeline = ImageCaptionPipeLine.get_image_caption_pipeline()

# save the instance to disk using pickle
with open("image_caption_pipeline.pkl", "wb") as f:
    pickle.dump(image_caption_pipeline, f)

# load the saved instance from disk using pickle
with open("image_caption_pipeline.pkl", "rb") as f:
    image_caption_pipeline = pickle.load(f)

# now you can use the loaded instance of the class to get the image captioning pipeline
# use the pipeline for image captioning
captions = image_caption_pipeline("test2.jpg")
print(captions)