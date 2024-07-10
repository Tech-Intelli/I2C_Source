from PIL import Image, ImageEnhance
import pilgram2


def apply_1977_filter(image):
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


def apply_1990_filter(image):
    image = apply_1977_filter(image)

    # Add a slight blue tint
    r, g, b = image.split()
    b = b.point(lambda i: i * 1.1)
    image = Image.merge("RGB", (r, g, b))

    return image

