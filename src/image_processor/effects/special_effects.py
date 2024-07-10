from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageChops
import cv2
import numpy as np


def hdr(image, contrast_factor=1.5, brightness_factor=1.3):
    """
    Apply HDR effect to an image.

    Args:
        image (PIL.Image.Image): The input image.
        contrast_factor (float, optional): Factor to enhance contrast. Defaults to 1.5.
        brightness_factor (float, optional): Factor to enhance brightness. Defaults to 1.3.

    Returns:
        PIL.Image.Image: The resulting HDR image.
    """

    enhancer = ImageEnhance.Contrast(image)
    hdr_image = enhancer.enhance(contrast_factor)
    enhancer = ImageEnhance.Brightness(hdr_image)
    hdr_image = enhancer.enhance(brightness_factor)
    return hdr_image


def orton(image, blur_radius=2, enhance_factor=1.5):
    """
    Apply the Orton effect to an image.

    The Orton effect is a post-processing technique that combines a blurred version of an image with the original image to create a depth-of-field effect. This function applies the Orton effect to the input image by first blurring the image using a Gaussian blur with a specified radius. Then, it enhances the brightness of the blurred image using the ImageEnhance module from the PIL library. Finally, it blends the original image and the brightened blurred image together with an alpha value of 0.5.

    Args:
        image (PIL.Image.Image): The input image to apply the Orton effect.
        blur_radius (int, optional): The radius for the Gaussian blur. Defaults to 2.
        enhance_factor (float, optional): The factor to enhance the brightness of the blurred image. Defaults to 1.5.

    Returns:
        PIL.Image.Image: The resulting image with the Orton effect applied.
    """

    blurred = image.filter(ImageFilter.GaussianBlur(blur_radius))
    enhancer = ImageEnhance.Brightness(blurred)
    brightened = enhancer.enhance(enhance_factor)
    orton_image = Image.blend(image, brightened, alpha=0.5)
    return orton_image


def lomography(image, contrast_factor=1.5, vignette_size=2):
    """
    Apply lomography effect to an image.

    Args:
        image (PIL.Image.Image): The input image.
        contrast_factor (float, optional): Factor to enhance contrast. Defaults to 1.5.
        vignette_size (int, optional): Size of vignette effect. Defaults to 2.

    Returns:
        PIL.Image.Image: The resulting image with the lomography effect applied.
    """

    enhancer = ImageEnhance.Contrast(image)
    lomo_image = enhancer.enhance(contrast_factor)

    vignette = Image.new("L", image.size, 0)
    vignette = vignette.filter(ImageFilter.GaussianBlur(vignette_size * 10))
    vignette = ImageOps.invert(vignette)
    vignette = vignette.point(lambda p: p * 0.8)
    lomo_image.putalpha(vignette)
    lomo_image = lomo_image.convert("RGB")

    return lomo_image


def infrared(image):
    """
    Apply an infrared effect to an image.

    Args:
        image_path (str): The path to the input image.
        output_path (str): The path to save the output image.

    Returns:
        PIL.Image.Image: The resulting image with the infrared effect applied.
    """
    r, g, b = image.split()
    infrared_image = Image.merge("RGB", (b, g, r))
    return infrared_image


def duotone(image, color1=(0, 0, 0), color2=(255, 255, 255)):
    """
    Apply duotone effect to an image.

    Args:
        image (PIL.Image.Image): The input image to apply the duotone effect to.
        color1 (tuple, optional): First color for duotone. Defaults to black.
        color2 (tuple, optional): Second color for duotone. Defaults to white.

    Returns:
        PIL.Image.Image: The resulting image with the duotone effect applied.
    """

    image = image.convert("L")
    duotone = ImageOps.colorize(image, black=color1, white=color2)
    return duotone


def cross_processing(image):
    """
    Apply cross processing effect to an image.

    Args:
        image (PIL.Image.Image): The input image to apply the cross processing effect to.

    Returns:
        PIL.Image.Image: The resulting image with the cross processing effect applied.

    The cross processing effect is achieved by manipulating the red and blue channels of the image. For each pixel in the image, if the red channel value is less than 128, it is multiplied by 1.2, and if it is greater than or equal to 128, it is multiplied by 0.8. Similarly, for each pixel in the image, if the blue channel value is less than 128, it is multiplied by 0.8, and if it is greater than or equal to 128, it is multiplied by 1.2. Finally, the modified red and blue channels are merged back into an RGB image.
    """

    r, g, b = image.split()
    r = r.point(lambda i: i * 1.2 if i < 128 else i * 0.8)
    b = b.point(lambda i: i * 0.8 if i < 128 else i * 1.2)
    cross_processed = Image.merge("RGB", (r, g, b))
    return cross_processed


def neon_glow(image, edge_enhance=1.5, color_enhance=1.5):
    """
    Apply neon glow effect to an image.

    Args:
        image (PIL.Image.Image): The input image.
        edge_enhance (float, optional): Factor to enhance edges. Defaults to 1.5.
        color_enhance (float, optional): Factor to enhance colors. Defaults to 1.5.

    Returns:
        PIL.Image.Image: The image with the neon glow effect applied.
    """

    edges = image.filter(ImageFilter.FIND_EDGES)
    edges = ImageEnhance.Contrast(edges).enhance(edge_enhance)
    neon_image = ImageEnhance.Color(edges).enhance(color_enhance)
    return neon_image


def posterize(image, bits=4):
    """
    Apply the posterize effect to an image.

    Args:
        image (PIL.Image.Image): The input image.
        bits (int, optional): The number of bits to use for each color channel. Defaults to 4.

    Returns:
        PIL.Image.Image: The image with the posterize effect applied.
    """

    posterized_image = ImageOps.posterize(image, bits)
    return posterized_image


def solarize(image, threshold=128):
    """
    Apply the solarize effect to an image.

    Args:
        image (PIL.Image.Image): The input image.
        threshold (int, optional): The threshold value above which to invert pixel values. Defaults to 128.

    Returns:
        PIL.Image.Image: The image with the solarize effect applied.
    """

    solarized_image = ImageOps.solarize(image, threshold)
    return solarized_image


def comic_book(image, edge_enhance=2.5, color_enhance=1.5):
    """
    Apply the comic book effect to an image.

    Args:
        image (PIL.Image.Image): The input image.
        edge_enhance (float, optional): The factor to enhance the edges. Defaults to 2.5.
        color_enhance (float, optional): The factor to enhance the colors. Defaults to 1.5.

    Returns:
        PIL.Image.Image: The comic book image with enhanced edges and colors.
    """

    edges = image.filter(ImageFilter.CONTOUR)
    edges = ImageEnhance.Contrast(edges).enhance(edge_enhance)
    comic_image = ImageEnhance.Color(edges).enhance(color_enhance)
    return comic_image


def t3d_effect(image, shift=5):
    """
    Apply 3D effect to an image by shifting the red and blue channels.

    Args:
        image (Image): Input image to apply the effect.
        shift (int, optional): Number of pixels to shift the red and blue channels. Defaults to 5.

    Returns:
        Image: The image with the 3D effect applied.
    """

    r, g, b = image.split()
    r = ImageChops.offset(r, shift, 0)
    b = ImageChops.offset(b, -shift, 0)
    _3d_image = Image.merge("RGB", (r, g, b))
    return _3d_image


def glitch(image, max_shift=10):
    """
    Apply a glitch effect to an image by shifting its rows randomly.

    Args:
        image (numpy.ndarray): The input image as a 3D numpy array.
        max_shift (int, optional): The maximum number of pixels to shift each row. Defaults to 10.

    Returns:
        numpy.ndarray: The glitched image as a 3D numpy array.
    """
    imagenp = np.array(image)
    rows, cols, _ = imagenp.shape
    glitch = np.copy(imagenp)

    for i in range(0, rows, 10):
        dx = np.random.randint(-max_shift, max_shift)
        glitch[i : i + 10, :] = np.roll(glitch[i : i + 10, :], dx, axis=0)

    return Image.fromarray(glitch.astype(np.uint8))


def watercolor(image):
    """
    Apply a watercolor effect to an image.

    Args:
        image_pil (PIL.Image.Image): The input image as a PIL Image.

    Returns:
        PIL.Image.Image: The image with the watercolor effect applied.
    """
    # Convert PIL Image to NumPy array
    image_np = np.array(image)

    # Convert RGB to BGR (OpenCV uses BGR by default)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    # Apply watercolor effect using OpenCV's stylization function
    watercolor_image_bgr = cv2.stylization(image_bgr, sigma_s=60, sigma_r=0.6)

    # Convert image back to RGB and then to PIL Image
    watercolor_image_rgb = cv2.cvtColor(watercolor_image_bgr, cv2.COLOR_BGR2RGB)
    watercolor_image_pil = Image.fromarray(watercolor_image_rgb)

    return watercolor_image_pil


def sketch(image: Image.Image) -> Image.Image:
    """
    Apply a pencil sketch effect to an image.

    Args:
        image (PIL.Image.Image): The input image as a PIL Image.

    Returns:
        PIL.Image.Image: The image with the pencil sketch effect applied.
    """
    # Convert PIL Image to NumPy array
    imagenp = np.array(image)
    # Convert RGB image to grayscale
    gray = cv2.cvtColor(imagenp, cv2.COLOR_RGB2GRAY)
    # Apply pencil sketch effect using cv2.pencilSketch
    sketch, _ = cv2.pencilSketch(gray, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
    # Convert sketch back to RGB (OpenCV returns grayscale)
    sketch_rgb = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
    # Convert NumPy array back to PIL Image
    sketch_pil = Image.fromarray(sketch_rgb)

    return sketch_pil


def cartoon(image):
    """
    Applies a cartoon effect to the input image by converting it to grayscale,
    applying median blur, adaptive thresholding, bilateral filtering, bitwise
    AND operation, and returns the cartoon image as a PIL Image.

    Args:
        image (numpy.ndarray): Input image to apply the cartoon effect to.

    Returns:
        PIL.Image.Image: Image with the cartoon effect applied.
    """
    imagenp = np.array(image)

    gray = cv2.cvtColor(imagenp, cv2.COLOR_BGR2GRAY)

    # Apply median blur to the grayscale image
    blurred = cv2.medianBlur(gray, 7)

    # Apply adaptive thresholding to get the edges
    edges = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2
    )

    # Apply bilateral filtering to the original color image
    color = cv2.bilateralFilter(imagenp, 9, 300, 300)

    # Combine color image with edges using bitwise AND
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    # Convert NumPy array back to PIL Image
    cartoon_pil = Image.fromarray(cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB))

    return cartoon_pil


def pop_art(image):
    """
    Given an image, applies a pop art effect by reshaping the image, performing k-means clustering with K=8, and returning the pop art image.

    Args:
        image: The input image to apply the pop art effect to.

    Returns:
        Image: The output pop art image.
    """
    imagenp = np.array(image)
    Z = imagenp.reshape((-1, 3))
    Z = np.float32(Z)
    K = 8
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    pop_art = res.reshape((imagenp.shape))
    return Image.fromarray(pop_art)


def pixelate(image, pixel_size=10):
    """
    Apply a pixelate effect to an image.

    Args:
        image (numpy.ndarray): The input image.
        pixel_size (int, optional): The size of the pixels. Defaults to 10.

    Returns:
        PIL.Image.Image: The pixelated image.
    """

    # image = cv2.imread(image_path)
    imagenp = np.array(image)
    height, width = imagenp.shape[:2]
    temp = cv2.resize(
        imagenp,
        (width // pixel_size, height // pixel_size),
        interpolation=cv2.INTER_LINEAR,
    )
    pixelated = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
    return Image.fromarray(pixelated)  # cv2.imwrite(output_path, pixelated)


def retro_vintage(image):
    """
    Apply a retro/vintage effect to an image.

    Args:
        image (PIL.Image.Image): The input image.

    Returns:
        PIL.Image.Image: The image with the retro/vintage effect applied.

    This function adjusts the colors, contrast, and brightness of an image to give it a vintage look. It then adds random noise to the image. The resulting image is returned as a PIL.Image.Image object.

    Example usage:
    ```
    from PIL import Image
    image = Image.open("input_image.jpg")
    vintage_image = retro_vintage(image)
    vintage_image.save("output_image.jpg")
    ```
    """

    # Adjust colors to give a vintage look
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(0.5)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.2)

    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.1)

    # Add noise
    np_image = np.array(image)
    noise = np.random.normal(loc=0, scale=25, size=np_image.shape)
    np_image = np_image + noise
    np_image = np.clip(np_image, 0, 255).astype(np.uint8)

    vintage_image = Image.fromarray(np_image)
    return vintage_image
