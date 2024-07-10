from PIL import Image, ImageEnhance
import numpy as np
import colorsys


def adjust_temperature(image, temp_factor=1.0):
    """
    Adjusts the temperature of an image by a specified factor.

    Parameters:
        image (PIL.Image.Image): The input image.
        temp_factor (float, optional): The temperature factor to adjust the image.
            A value greater than 1 makes the image warmer by enhancing the red color
            and decreasing the blue color. A value less than 1 makes the image cooler
            by decreasing the red color and enhancing the blue color. Defaults to 1.0.

    Returns:
        PIL.Image.Image: The image with the adjusted temperature.
    """

    r, g, b = image.split()

    if temp_factor > 1:
        # Warmer: Enhance red, decrease blue
        r = r.point(lambda i: min(255, i * temp_factor))
        b = b.point(lambda i: max(0, i / temp_factor))
    else:
        # Cooler: Decrease red, enhance blue
        r = r.point(lambda i: max(0, i * temp_factor))
        b = b.point(lambda i: min(255, i / temp_factor))

    temp_image = Image.merge("RGB", (r, g, b))
    return temp_image


def adjust_hue(image, hue_shift=30):
    """
    Adjusts the hue of an image by a specified shift value.

    Args:
        image (PIL.Image.Image): The input image to adjust.
        hue_shift (int, optional): The amount to shift the hue by, in degrees. Defaults to 30.

    Returns:
        PIL.Image.Image: The image with the adjusted hue.
    """

    image = image.convert("RGB")
    np_image = np.array(image)

    def shift_hue(arr, shift):
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                r, g, b = arr[i, j] / 255.0
                h, l, s = colorsys.rgb_to_hls(r, g, b)
                h = (h + shift / 360.0) % 1.0
                r, g, b = colorsys.hls_to_rgb(h, l, s)
                arr[i, j] = int(r * 255), int(g * 255), int(b * 255)
        return arr

    hue_adjusted = shift_hue(np_image, hue_shift)
    hue_image = Image.fromarray(hue_adjusted, "RGB")
    return hue_image


def adjust_contrast(image, factor):
    """
    Adjust the contrast of an image.

    Args:
        image: The input image.
        factor: Contrast adjustment factor.

    Returns:
        The image with enhanced contrast.
    """

    enhancer = ImageEnhance.Contrast(image)
    image_enhanced = enhancer.enhance(factor)
    return image_enhanced


def adjust_brightness(image, factor):
    """
    Adjust the brightness of an image.

    Args:
        image: The input image.
        factor: Brightness adjustment factor.

    Returns:
        The image with enhanced brightness.
    """

    enhancer = ImageEnhance.Brightness(image)
    image_enhanced = enhancer.enhance(factor)
    return image_enhanced


def adjust_sharpness(image, factor):
    """
    Adjust the sharpness of an image.

    Args:
        image: The input image.
        factor: Sharpness adjustment factor.

    Returns:
        The image with enhanced sharpness.
    """

    enhancer = ImageEnhance.Sharpness(image)
    image_enhanced = enhancer.enhance(factor)
    return image_enhanced


def rotate_image(image, degrees):
    """
    Rotate an image by the specified number of degrees.

    Args:
        image (PIL.Image.Image): The input image.
        degrees (float): The number of degrees to rotate the image.

    Returns:
        PIL.Image.Image: The rotated image.
    """

    return image.rotate(degrees)


def flip_image(image, direction="horizontal"):
    """
    Flips the input image horizontally or vertically based on the specified direction.

    Args:
        image: The input image to be flipped.
        direction: The direction in which to flip the image. Default is "horizontal".

    Returns:
        Image: The flipped image.

    Raises:
        ValueError: If the direction is not 'horizontal' or 'vertical'.
    """

    if direction == "horizontal":
        image_flipped = image.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == "vertical":
        image_flipped = image.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        raise ValueError("Direction must be 'horizontal' or 'vertical'")
    return image_flipped


def adjust_gamma(image, gamma=1.0):
    """
    Adjusts the gamma value of an image.

    Args:
        image (PIL.Image.Image): The input image.
        gamma (float, optional): The gamma value to apply. Defaults to 1.0.

    Returns:
        PIL.Image.Image: The gamma-corrected image.

    The gamma correction formula is:
        new_value = 255 * (old_value / 255) ** (1 / gamma)
    """

    # Apply gamma correction to each pixel value
    gamma_corrected = image.point(lambda p: 255 * (p / 255) ** (1 / gamma))

    return gamma_corrected


def adjust_clarity(image, clarity_factor=1.5):
    """
    Adjust clarity of an image.

    Args:
        image (PIL.Image.Image): The input image.
        clarity_factor (float, optional): Factor to enhance clarity. Defaults to 1.5.

    Returns:
        PIL.Image.Image: The image with enhanced clarity.
    """

    enhancer = ImageEnhance.Contrast(image)
    clarity = enhancer.enhance(clarity_factor)
    return clarity


def adjust_saturation(image, saturation_factor=1.5):
    """
    Adjusts the saturation of an image.

    Args:
        image (PIL.Image.Image): The input image.
        saturation_factor (float, optional): The factor to enhance or decrease the saturation of the image. Defaults to 1.5.

    Returns:
        PIL.Image.Image: The image with adjusted saturation.
    """

    enhancer = ImageEnhance.Color(image)
    saturated = enhancer.enhance(saturation_factor)
    return saturated
