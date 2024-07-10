from processor.image_processor.enhance.img_enhancer import (
    adjust_brightness,
    adjust_saturation,
    adjust_temperature,
)


def winter_filter(image):
    image = adjust_brightness(image, 0.8)
    image = adjust_saturation(image, 0.7)
    return adjust_temperature(image, 0.8)
