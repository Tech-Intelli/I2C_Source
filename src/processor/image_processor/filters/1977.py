from PIL import Image, ImageEnhance, ImageOps, ImageChops
import numpy as np
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


# Load an image
image_path = "../../temp/test.png"
image = Image.open(image_path)

# Apply filters
image_1977 = apply_1977_filter(image)
image_1990 = apply_1990_filter(image)

# Save the images
image_1977.save("image_1977.jpg")
image_1990.save("image_1990.jpg")
pilgram2._1977(image).save("1977.jpg")
# Show the images
image_1977.show()
image_1990.show()
