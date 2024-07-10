import numpy as np
from PIL import Image, ImageOps


def selective_color(image, target_color, enhance_factor=1.5):
    """
    Enhance a specific color in an image.
    Args:
        image_path (str): Path to the input image.
        target_color (str): Color to enhance ('red', 'green', 'blue').
        enhance_factor (float, optional): Factor to enhance the target color. Defaults to 1.5.
    Returns:
        PIL.Image.Image: The enhanced image with the specified color.
    Raises:
        ValueError: If the target color is not 'red', 'green', or 'blue'.
    """
    image = image.convert("RGB")
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
    return enhanced_image


def sepia(image, intensity):
    """
    Apply a sepia effect to an image.

    Args:
        image_path (str): The path to the input image.
        intensity (int): The intensity of the sepia effect. Must be between 0 and 100.

    Returns:
        PIL.Image.Image: The image with the sepia effect applied.

    Raises:
        ValueError: If the intensity is not between 0 and 100.
    """

    if not (0 <= intensity <= 100):
        raise ValueError("Intensity must be between 0 and 100.")

    # Load the original image
    image = image.convert("RGB")
    width, height = image.size
    pixels = image.load()

    # Create a sepia-toned image
    sepia_image = Image.new("RGB", (width, height))
    sepia_pixels = sepia_image.load()

    for py in range(height):
        for px in range(width):
            r, g, b = image.getpixel((px, py))

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            sepia_pixels[px, py] = (min(tr, 255), min(tg, 255), min(tb, 255))

    # Blend the original and sepia images
    intensity_ratio = intensity / 100.0
    blended_image = Image.blend(image, sepia_image, intensity_ratio)

    # Save the output image
    return blended_image


def black_and_white(image, threshold=128):
    """
    Convert an image to black and white based on a threshold value.

    Args:
        image (PIL.Image.Image): The input image to convert.
        threshold (int, optional): The threshold value to determine the black and white conversion. Defaults to 128.

    Returns:
        PIL.Image.Image: The black and white image.
    """

    image = image.convert("L")
    bw = image.point(lambda x: 255 if x > threshold else 0, "1")
    return bw


def invert_colors(image):
    """
    Inverts the colors of the input image.

    Args:
        image: The input image to invert.

    Returns:
        PIL.Image.Image: The inverted image.
    """

    inverted_image = ImageOps.invert(image)
    return inverted_image


def grayscale(image, intensity):
    """
    Apply a grayscale effect to an image with a given intensity.

    Args:
        image (PIL.Image.Image): The input image to apply the grayscale effect.
        intensity (int): The intensity of the grayscale effect, ranging from 0 to 100.

    Returns:
        PIL.Image.Image: The image with the grayscale effect applied.

    Raises:
        ValueError: If the intensity is not between 0 and 100.

    Example:
        >>> image = Image.open('input.jpg')
        >>> grayscale_image = grayscale(image, 50)
    """

    if not (0 <= intensity <= 100):
        raise ValueError("Intensity must be between 0 and 100.")

    # Convert the image to grayscale
    grayscale_image = image.convert("L").convert("RGB")

    # Blend the original and grayscale images
    intensity_ratio = intensity / 100.0
    blended_image = Image.blend(image, grayscale_image, intensity_ratio)

    # Save the output image
    return blended_image
