
from transformers import VisionEncoderDecoderModel
from transformers import ViTImageProcessor
from transformers import AutoTokenizer
from transformers import Pipeline
from transformers import pipeline
import torch
import warnings

warnings.filterwarnings("ignore")


class ImageCaptionPipeLine:
    def __init__(self):
        self.model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.device = None

    def set_device(self):
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
        elif torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")
        self.model.to(self.device)

    def get_image_caption_pipeline(self) -> Pipeline:
        image_caption_pipeline = pipeline("image-to-text",
                                          model="nlpconnect/vit-gpt2-image-captioning",
                                          device=self.device,
                                          tokenizer=self.tokenizer,
                                          feature_extractor=self.feature_extractor,
                                          image_processor=self.feature_extractor)
        return image_caption_pipeline


def get_image_caption(image_path, image_pipeline: Pipeline):
    return image_pipeline(image_path)[0]['generated_text']


imagePipeline = ImageCaptionPipeLine()
imagePipeline.set_device()
imagePipeline = imagePipeline.get_image_caption_pipeline()
get_image_caption("test.jpg", imagePipeline)
