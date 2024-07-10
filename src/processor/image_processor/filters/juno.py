from PIL import Image, ImageEnhance


def apply_sepia(image, intensity=0.35):
    width, height = image.size
    pixels = image.load()

    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            tr = int(tr * intensity + r * (1 - intensity))
            tg = int(tg * intensity + g * (1 - intensity))
            tb = int(tb * intensity + b * (1 - intensity))

            tr = min(255, tr)
            tg = min(255, tg)
            tb = min(255, tb)

            pixels[px, py] = (tr, tg, tb)
    image.save("image_sepia.jpg")
    return image


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
    sepia_image = apply_sepia(blended)

    # Apply contrast, brightness, and saturation adjustments
    enhancer = ImageEnhance.Contrast(sepia_image)
    sepia_image = enhancer.enhance(1.15)

    enhancer = ImageEnhance.Brightness(sepia_image)
    sepia_image = enhancer.enhance(1.15)

    enhancer = ImageEnhance.Color(sepia_image)
    sepia_image = enhancer.enhance(1.8)

    return sepia_image


# Load an image
image_path = "../../temp/test.png"
image = Image.open(image_path)
# Apply Juno filter
image_juno = juno(image)
# pilgram2._1977(image).save('juno.jpg')
# Save and show the image
image_juno.save("image_juno.jpg")
