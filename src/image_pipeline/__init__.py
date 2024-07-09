"""
Image Captioning Module
"""
from .abstract.image_pipeline_abstract import ImageCaptioningPipeline
from .impl.vit_pipeline import ViTGPT2Pipeline
from .impl.blip2_pipeline import Blip2Pipeline
from .impl.llava_pipeline import LlavaPipeline


__all__ = (
    "ImageCaptioningPipeline",
    "ViTGPT2Pipeline",
    "Blip2Pipeline",
    "LlavaPipeline",
)
