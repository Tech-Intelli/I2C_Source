from transformers import (
    VisionEncoderDecoderModel,
    ViTImageProcessor,
    AutoTokenizer,
    Pipeline,
    pipeline,
    AutoProcessor,
)
from image_caption import ImageCaptioningPipeline


class ViTGPT2ImageCaptioningPipeline(ImageCaptioningPipeline):
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
        if ViTGPT2ImageCaptioningPipeline._model is None:
            ViTGPT2ImageCaptioningPipeline._model = (
                VisionEncoderDecoderModel.from_pretrained(
                    ViTGPT2ImageCaptioningPipeline.MODEL_NAME
                )
            )
            ViTGPT2ImageCaptioningPipeline._feature_extractor = (
                ViTImageProcessor.from_pretrained(
                    ViTGPT2ImageCaptioningPipeline.MODEL_NAME
                )
            )
            ViTGPT2ImageCaptioningPipeline._tokenizer = AutoTokenizer.from_pretrained(
                ViTGPT2ImageCaptioningPipeline.MODEL_NAME
            )

    def get_image_caption_pipeline(self) -> Pipeline:
        """
        Returns a pipeline for generating captions from images.
        """
        ViTGPT2ImageCaptioningPipeline._initialize_vit_gpt2()
        image_caption_pipeline = pipeline(
            "image-to-text",
            model=ViTGPT2ImageCaptioningPipeline._model,
            tokenizer=ViTGPT2ImageCaptioningPipeline._tokenizer,
            feature_extractor=ViTGPT2ImageCaptioningPipeline._feature_extractor,
            image_processor=ViTGPT2ImageCaptioningPipeline._feature_extractor,
        )
        return image_caption_pipeline

    def get_image_processor(self) -> AutoProcessor:
        """
        Returns the image processor for the ViT-GPT2 model.
        """
        ViTGPT2ImageCaptioningPipeline._initialize_vit_gpt2()
        return ViTGPT2ImageCaptioningPipeline._feature_extractor
