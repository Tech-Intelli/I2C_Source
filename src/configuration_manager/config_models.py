"""Configuration models module."""

from dataclasses import dataclass, field


@dataclass
class ModelSelectionConfig:
    model_name: str = "blip2"


@dataclass
class MultiModalConfig:
    blip: str = "Salesforce/blip2-opt-2.7b"
    vit: str = "nlpconnect/vit-gpt2-image-captioning"
    llava: str = "llava-hf/llava-1.5-7b-hf"


@dataclass
class Variants:
    phi3: str = "phi3"
    llama3: str = "llama3"
    gemma2: str = "gemma2"


@dataclass
class OllamaConfig:
    variants: Variants = field(default_factory=Variants)
    use: str = "Phi"
    temperature: int = 1
    top_p: float = 0.9
    stream: bool = False


@dataclass
class ImageCompressionConfig:
    type: str = "webp"
    compress: bool = True
    compression_quality: int = 50
    resize_factor: float = 0.5


@dataclass
class TransformConfig:
    resize: tuple = (256, 256)
    center_crop: int = 224
