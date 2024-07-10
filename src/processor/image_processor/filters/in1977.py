from PIL import Image, ImageEnhance


def apply_1977_filter(image):
    """
    Applies the 1977 filter effect to the input image.

    Args:
        image: The input image to which the filter will be applied.

    Returns:
        Image: The filtered image after applying the 1977 filter effect.
    """
    # Convert to RGB if not already
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Apply brightness, contrast, and color adjustments
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.2)  # Slight increase in brightness

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(0.888)  # Slight increase in contrast

    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(0.88)  # Slight increase in saturation

    # Add a subtle warm tone by adjusting the RGB channels
    r, g, b = image.split()
    r = r.point(lambda i: i * 1.18)  # Slightly increase red channel
    g = g.point(lambda i: i * 0.95)  # Slightly increase green channel
    b = b.point(lambda i: i * 0.95)  # Slightly decrease blue channel
    image = Image.merge("RGB", (r, g, b))

    return image
