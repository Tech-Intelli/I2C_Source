
from transformers import VisionEncoderDecoderModel
from transformers import ViTImageProcessor
from transformers import AutoTokenizer
from transformers import Pipeline
from transformers import pipeline
import torch
import warnings

warnings.filterwarnings("ignore")


class ImageCaptionPipeLine:
    model = VisionEncoderDecoderModel.from_pretrained(
        "nlpconnect/vit-gpt2-image-captioning")
    feature_extractor = ViTImageProcessor.from_pretrained(
        "nlpconnect/vit-gpt2-image-captioning")
    tokenizer = AutoTokenizer.from_pretrained(
        "nlpconnect/vit-gpt2-image-captioning")
    device = None

    if torch.backends.mps.is_available():
        device = torch.device("mps")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    model.to(device)

    @staticmethod
    def get_image_caption_pipeline() -> Pipeline:
        image_caption_pipeline = pipeline(
            "image-to-text",
            model=ImageCaptionPipeLine.model,
            device=ImageCaptionPipeLine.device,
            tokenizer=ImageCaptionPipeLine.tokenizer,
            feature_extractor=ImageCaptionPipeLine.feature_extractor,
            image_processor=ImageCaptionPipeLine.feature_extractor)
        return image_caption_pipeline
