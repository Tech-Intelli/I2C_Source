from PIL import Image
from processor.image_processor.filters.in1977 import apply_1977_filter


def apply_1990_filter(image):
    """
    Applies the 1990 filter effect to the input image.

    Args:
        image: The input image to which the filter will be applied.

    Returns:
        Image: The filtered image after applying the 1990 filter effect.
    """
    image = apply_1977_filter(image)

    # Add a slight blue tint
    r, g, b = image.split()
    b = b.point(lambda i: i * 1.1)
    image = Image.merge("RGB", (r, g, b))

    return image
