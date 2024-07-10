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


def sepia(image, intensity=100):
    # Convert image to numpy array
    img_array = np.array(image)

    # Apply the sepia filter matrix
    sepia_filter = np.array([[0.393, 0.769, 0.189],
                             [0.349, 0.686, 0.168],
                             [0.272, 0.534, 0.131]])

    # Perform dot product and clip values to be in the 0-255 range
    sepia_array = img_array @ sepia_filter.T
    sepia_array = np.clip(sepia_array, 0, 255)

    # Convert back to uint8 to ensure correct image format
    sepia_array = sepia_array.astype(np.uint8)

    # Convert numpy array back to PIL Image
    sepia_image = Image.fromarray(sepia_array)

    return sepia_image


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
