from PIL import Image, ImageEnhance
import numpy as np
import colorsys
import cv2


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
    np_image = np.array(image, dtype=np.float32) / 255.0

    r, g, b = np_image[..., 0], np_image[..., 1], np_image[..., 2]
    h, l, s = np.vectorize(colorsys.rgb_to_hls)(r, g, b)  # noqa: E741
    h = (h + hue_shift / 360.0) % 1.0
    r, g, b = np.vectorize(colorsys.hls_to_rgb)(h, l, s)

    np_image[..., 0], np_image[..., 1], np_image[..., 2] = r, g, b
    hue_adjusted = (np_image * 255).astype(np.uint8)
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


def apply_vignette(image, intensity=0.8):
    image_np = np.array(image)

    # Convert RGB to BGR (OpenCV uses BGR by default)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Create a mask of ones with the same dimensions as the image
    mask = np.ones_like(image_bgr, dtype=np.float32)

    # Calculate the center coordinates
    center_x, center_y = mask.shape[1] // 2, mask.shape[0] // 2

    # Calculate the maximum distance from the center to any edge
    max_distance = np.sqrt((center_x**2) + (center_y**2))

    # Calculate the distance of each pixel from the center
    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            distance = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            # Normalize distance to be between 0 and 1
            distance /= max_distance
            # Apply vignette effect inversely based on the distance from the center
            mask[y, x] *= 1 - intensity * distance

    # Apply the mask to each channel of the image
    vignette_image = image_bgr * mask

    # Convert back to RGB and then to PIL image
    vignette_image_rgb = cv2.cvtColor(np.uint8(vignette_image), cv2.COLOR_BGR2RGB)
    vignette_image_pil = Image.fromarray(vignette_image_rgb)

    return vignette_image_pil


def apply_color_splash(image, target_color, threshold=60):
    """
    Apply a color splash effect to an image.

    Args:
        image (PIL.Image.Image): The input image.
        target_color (tuple): The target color to isolate (R, G, B).
        threshold (int): The color difference threshold.

    Returns:
        PIL.Image.Image: The image with the color splash effect applied.
    """
    # Convert PIL image to NumPy array
    image_np = np.array(image)

    # Convert RGB to BGR (OpenCV uses BGR by default)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

    # Define the target color in HSV
    target_color_hsv = cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_RGB2HSV)[0][0]

    # Define the lower and upper bounds for the target color
    lower_bound = np.array([max(target_color_hsv[0] - threshold, 0), 50, 50])
    upper_bound = np.array([min(target_color_hsv[0] + threshold, 179), 255, 255])

    # Create a mask for the target color
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # Create a 3-channel grayscale image
    gray_3_channel = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    # Apply the mask to retain the target color and desaturate the rest
    result = cv2.bitwise_and(image_bgr, image_bgr, mask=mask)
    mask_inv = cv2.bitwise_not(mask)
    gray_background = cv2.bitwise_and(gray_3_channel, gray_3_channel, mask=mask_inv)
    color_splash = cv2.add(result, gray_background)

    # Convert the result back to RGB and then to PIL Image
    color_splash_rgb = cv2.cvtColor(color_splash, cv2.COLOR_BGR2RGB)
    color_splash_pil = Image.fromarray(color_splash_rgb)

    return color_splash_pil
