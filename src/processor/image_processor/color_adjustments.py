import numpy as np
from PIL import Image, ImageOps


def selective_color(image_path, output_path, target_color, enhance_factor=1.5):
    """
    Enhance a specific color in an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        target_color (str): Color to enhance ('red', 'green', 'blue').
        enhance_factor (float, optional): Factor to enhance the target color. Defaults to 1.5.
    """
    image = Image.open(image_path).convert("RGB")
    np_image = np.array(image)
    r, g, b = np_image[:, :, 0], np_image[:, :, 1], np_image[:, :, 2]

    if target_color == "red":
        r = np.clip(r * enhance_factor, 0, 255)
    elif target_color == "green":
        g = np.clip(g * enhance_factor, 0, 255)
    elif target_color == "blue":
        b = np.clip(b * enhance_factor, 0, 255)

    enhanced_image = np.dstack((r, g, b)).astype(np.uint8)
    enhanced_image = Image.fromarray(enhanced_image, "RGB")
    enhanced_image.save(output_path)


def apply_sepia(image_path, output_path):
    """
    Apply sepia effect to an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
    """
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    pixels = image.load()

    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            pixels[px, py] = (min(tr, 255), min(tg, 255), min(tb, 255))

    image.save(output_path)


def black_and_white(image_path, output_path, threshold=128):
    """
    Convert an image to black and white using a threshold.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        threshold (int, optional): Threshold value for binarization. Defaults to 128.
    """
    image = Image.open(image_path).convert("L")
    bw = image.point(lambda x: 255 if x > threshold else 0, "1")
    bw.save(output_path)


def invert_colors(image_path, output_path):
    """
    Invert the colors of an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
    """
    image = Image.open(image_path)
    inverted_image = ImageOps.invert(image)
    inverted_image.save(output_path)


def apply_grayscale(image_path, output_path):
    """
    Apply grayscale filter to the input image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output grayscale image.

    Returns:
        None
    """
    image = Image.open(image_path).convert("L")
    image.save(output_path)
    print(f"Converted image to grayscale. Image saved to {output_path}.")
