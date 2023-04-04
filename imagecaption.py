
from transformers import VisionEncoderDecoderModel
from transformers import ViTImageProcessor
from transformers import AutoTokenizer
from transformers import pipeline
import torch
import warnings

warnings.filterwarnings("ignore")

model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
device = None
model.to(device)
if torch.backends.mps.is_available():
    device = torch.device("mps")
elif torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

image_to_text = pipeline("image-to-text",
    model="nlpconnect/vit-gpt2-image-captioning",
    device=device,
    tokenizer=tokenizer,
    feature_extractor=feature_extractor,
    image_processor=feature_extractor)

print(image_to_text("test.jpg")[0]['generated_text'])
