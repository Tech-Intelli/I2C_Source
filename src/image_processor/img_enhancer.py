from PIL import Image, ImageEnhance
import numpy as np
import colorsys


def adjust_temperature(image_path, output_path, temp_factor=1.0):
    """
    Adjust the temperature of an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        temp_factor (float, optional): Factor to adjust temperature. >1 for warmer, <1 for cooler. Defaults to 1.0.
    """
    image = Image.open(image_path)
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
    temp_image.save(output_path)


def adjust_hue(image_path, output_path, hue_shift=30):
    """
    Adjust hue of an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        hue_shift (int, optional): Degree to shift hue. Defaults to 30.
    """
    image = Image.open(image_path).convert("RGB")
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
    hue_image.save(output_path)
    print(f"Hue adjusted by a factor of {hue_shift}. Image saved to {output_path}.")


def adjust_contrast(image_path, output_path, factor):
    """
    Adjust the contrast of an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        factor (float): Contrast adjustment factor (1.0 is no change, <1.0 decreases contrast, >1.0 increases contrast).

    Returns:
        None

    This function opens an image using the provided `image_path`, enhances its contrast using the `ImageEnhance.Contrast` class, and saves the enhanced image to the specified `output_path`. The function also prints a message indicating the adjustment factor and the path where the image was saved.
    """

    image = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(image)
    image_enhanced = enhancer.enhance(factor)
    image_enhanced.save(output_path)
    print(f"Contrast adjusted by a factor of {factor}. Image saved to {output_path}.")


def adjust_brightness(image_path, output_path, factor):
    """
    Adjust the brightness of an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        factor (float): Brightness adjustment factor.
            A value of 1.0 represents no change,
            a value less than 1.0 decreases brightness,
            and a value greater than 1.0 increases brightness.

    Returns:
        None

    This function opens an image using the provided `image_path`,
    enhances its brightness using the `ImageEnhance.Brightness` class,
    and saves the enhanced image to the specified `output_path`.
    The function also prints a message indicating the adjustment factor
    and the path where the image was saved.
    """

    image = Image.open(image_path)
    enhancer = ImageEnhance.Brightness(image)
    image_enhanced = enhancer.enhance(factor)
    image_enhanced.save(output_path)
    print(f"Brightness adjusted by a factor of {factor}. Image saved to {output_path}.")


def adjust_sharpness(image_path, output_path, factor):
    """
    Adjust the sharpness of an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        factor (float): Sharpness adjustment factor.
            A value of 1.0 represents no change,
            a value less than 1.0 decreases sharpness,
            and a value greater than 1.0 increases sharpness.

    Returns:
        None

    This function opens an image using the provided `image_path`,
    enhances its sharpness using the `ImageEnhance.Sharpness` class,
    and saves the enhanced image to the specified `output_path`.
    The function also prints a message indicating the adjustment factor
    and the path where the image was saved.
    """

    image = Image.open(image_path)
    enhancer = ImageEnhance.Sharpness(image)
    image_enhanced = enhancer.enhance(factor)
    image_enhanced.save(output_path)
    print(f"Sharpness adjusted by a factor of {factor}. Image saved to {output_path}.")


def rotate_image(image_path, output_path, degrees):
    """
    Rotate an image by the specified number of degrees and save the rotated image to the specified output path.

    Args:
        image_path (str): The path to the input image.
        output_path (str): The path to save the rotated image.
        degrees (float): The number of degrees to rotate the image.

    Returns:
        None

    This function opens an image using the provided `image_path`,
    rotates it by the specified `degrees`,
    and saves the rotated image to the specified `output_path`.
    The function also prints a message indicating the rotation angle
    and the path where the image was saved.
    """
    image = Image.open(image_path)
    image_rotated = image.rotate(degrees)
    image_rotated.save(output_path)
    print(f"Rotated image by {degrees} degrees. Image saved to {output_path}.")


def flip_image(image_path, output_path, direction="horizontal"):
    """
    Flip the input image either horizontally or vertically based on the specified direction.

    Args:
        image_path (str): The path to the input image.
        output_path (str): The path to save the flipped image.
        direction (str, optional): The direction to flip the image, either 'horizontal' or 'vertical'. Defaults to 'horizontal'.

    Raises:
        ValueError: If the direction is not 'horizontal' or 'vertical'.

    Returns:
        None
    """
    image = Image.open(image_path)
    if direction == "horizontal":
        image_flipped = image.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == "vertical":
        image_flipped = image.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        raise ValueError("Direction must be 'horizontal' or 'vertical'")
    image_flipped.save(output_path)
    print(f"Flipped image {direction}. Image saved to {output_path}.")


def adjust_gamma(image_path, output_path, gamma=1.0):
    """
    Adjusts the gamma value of an image.

    Args:
        image_path (str): The path to the input image.
        output_path (str): The path to save the output image.
        gamma (float, optional): The gamma value to apply. Defaults to 1.0.

    Returns:
        None
    """

    image = Image.open(image_path)
    gamma_corrected = image.point(lambda p: 255 * (p / 255) ** (1 / gamma))
    gamma_corrected.save(output_path)


def adjust_clarity(image_path, output_path, clarity_factor=1.5):
    """
    Adjust clarity of an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        clarity_factor (float, optional): Factor to enhance clarity. Defaults to 1.5.
    Returns:
        None
    """
    image = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(image)
    clarity = enhancer.enhance(clarity_factor)
    clarity.save(output_path)


def adjust_saturation(image_path, output_path, saturation_factor=1.5):
    """
    Adjust saturation of an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        saturation_factor (float, optional): Factor to enhance saturation. Defaults to 1.5.
    Returns:
        None
    """
    image = Image.open(image_path)
    enhancer = ImageEnhance.Color(image)
    saturation = enhancer.enhance(saturation_factor)
    saturation.save(output_path)
