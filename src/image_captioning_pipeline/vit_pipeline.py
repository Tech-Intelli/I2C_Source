from transformers import (
    VisionEncoderDecoderModel,
    ViTImageProcessor,
    AutoTokenizer,
    Pipeline,
    pipeline,
    AutoProcessor,
)
from image_captioning_pipeline import ImageCaptioningPipeline


class ViTGPT2Pipeline(ImageCaptioningPipeline):
    """
    A class for generating captions from images using the ViT-GPT2 image captioning model.
    """

    MODEL_NAME = "nlpconnect/vit-gpt2-image-captioning"

    _model = None
    _feature_extractor = None
    _tokenizer = None

    @staticmethod
    def _initialize_vit_gpt2():
        """Initializes the ViT-GPT2 model, feature extractor, and tokenizer if not already initialized."""
        if ViTGPT2Pipeline._model is None:
            ViTGPT2Pipeline._model = VisionEncoderDecoderModel.from_pretrained(
                ViTGPT2Pipeline.MODEL_NAME
            )
            ViTGPT2Pipeline._feature_extractor = ViTImageProcessor.from_pretrained(
                ViTGPT2Pipeline.MODEL_NAME
            )
            ViTGPT2Pipeline._tokenizer = AutoTokenizer.from_pretrained(
                ViTGPT2Pipeline.MODEL_NAME
            )

    def get_image_caption_pipeline(self) -> Pipeline:
        """
        Returns a pipeline for generating captions from images.
        """
        ViTGPT2Pipeline._initialize_vit_gpt2()
        image_caption_pipeline = pipeline(
            "image-to-text",
            model=ViTGPT2Pipeline._model,
            tokenizer=ViTGPT2Pipeline._tokenizer,
            feature_extractor=ViTGPT2Pipeline._feature_extractor,
            image_processor=ViTGPT2Pipeline._feature_extractor,
        )
        return image_caption_pipeline

    def get_image_processor(self) -> AutoProcessor:
        """
        Returns the image processor for the ViT-GPT2 model.
        """
        ViTGPT2Pipeline._initialize_vit_gpt2()
        return ViTGPT2Pipeline._feature_extractor
