from PIL import Image, ImageEnhance
from processor.image_processor.effects.color_effects import sepia


def juno(image):
    # Convert to RGBA if not already
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    # Create an overlay with a specific color and alpha
    overlay = Image.new("RGBA", image.size, (227, 187, 227, int(255 * 0.2)))

    # Blend the image using the overlay
    blended = Image.blend(image, overlay, alpha=0.2)

    # Convert back to RGB mode
    blended = blended.convert("RGB")

    # Apply sepia filter
    sepia_image = sepia(blended)

    # Apply contrast, brightness, and saturation adjustments
    enhancer = ImageEnhance.Contrast(sepia_image)
    sepia_image = enhancer.enhance(1.15)

    enhancer = ImageEnhance.Brightness(sepia_image)
    sepia_image = enhancer.enhance(1.15)

    enhancer = ImageEnhance.Color(sepia_image)
    sepia_image = enhancer.enhance(1.8)

    return sepia_image
