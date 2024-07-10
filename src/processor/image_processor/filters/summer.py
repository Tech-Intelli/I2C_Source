
from processor.image_processor.enhance.img_enhancer import (
    adjust_brightness,
    adjust_saturation,
    adjust_temperature,
)
def summer_filter(image):
    image = adjust_brightness(image, 1.2)
    image = adjust_saturation(image, 1.5)
    return adjust_temperature(image, 1.2)
