from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageChops


def apply_hdr(image_path, output_path, contrast_factor=1.5, brightness_factor=1.3):
    """
    Apply HDR effect to an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        contrast_factor (float, optional): Factor to enhance contrast. Defaults to 1.5.
        brightness_factor (float, optional): Factor to enhance brightness. Defaults to 1.3.
    """
    image = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(image)
    hdr_image = enhancer.enhance(contrast_factor)
    enhancer = ImageEnhance.Brightness(hdr_image)
    hdr_image = enhancer.enhance(brightness_factor)
    hdr_image.save(output_path)


def apply_orton(image_path, output_path, blur_radius=2, enhance_factor=1.5):
    """
    Apply Orton effect to an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        blur_radius (int, optional): Radius for Gaussian blur. Defaults to 2.
        enhance_factor (float, optional): Factor to enhance brightness. Defaults to 1.5.
    """
    image = Image.open(image_path)
    blurred = image.filter(ImageFilter.GaussianBlur(blur_radius))
    enhancer = ImageEnhance.Brightness(blurred)
    brightened = enhancer.enhance(enhance_factor)
    orton_image = Image.blend(image, brightened, alpha=0.5)
    orton_image.save(output_path)


def apply_lomography(image_path, output_path, contrast_factor=1.5, vignette_size=2):
    """
    Apply lomography effect to an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        contrast_factor (float, optional): Factor to enhance contrast. Defaults to 1.5.
        vignette_size (int, optional): Size of vignette effect. Defaults to 2.
    """
    image = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(image)
    lomo_image = enhancer.enhance(contrast_factor)

    vignette = Image.new("L", image.size, 0)
    vignette = vignette.filter(ImageFilter.GaussianBlur(vignette_size * 10))
    vignette = ImageOps.invert(vignette)
    vignette = vignette.point(lambda p: p * 0.8)
    lomo_image.putalpha(vignette)
    lomo_image = lomo_image.convert("RGB")

    lomo_image.save(output_path)


def apply_infrared(image_path, output_path):
    """
    Apply infrared effect to an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
    """
    image = Image.open(image_path).convert("RGB")
    r, g, b = image.split()
    infrared_image = Image.merge("RGB", (b, g, r))
    infrared_image.save(output_path)


def apply_duotone(image_path, output_path, color1=(0, 0, 0), color2=(255, 255, 255)):
    """
    Apply duotone effect to an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        color1 (tuple, optional): First color for duotone. Defaults to black.
        color2 (tuple, optional): Second color for duotone. Defaults to white.
    """
    image = Image.open(image_path).convert("L")
    duotone = ImageOps.colorize(image, black=color1, white=color2)
    duotone.save(output_path)


def apply_cross_processing(image_path, output_path):
    """
    Apply cross processing effect to an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
    """
    image = Image.open(image_path)
    r, g, b = image.split()
    r = r.point(lambda i: i * 1.2 if i < 128 else i * 0.8)
    b = b.point(lambda i: i * 0.8 if i < 128 else i * 1.2)
    cross_processed = Image.merge("RGB", (r, g, b))
    cross_processed.save(output_path)


def apply_neon_glow(image_path, output_path, edge_enhance=1.5, color_enhance=1.5):
    """
    Apply neon glow effect to an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        edge_enhance (float, optional): Factor to enhance edges. Defaults to 1.5.
        color_enhance (float, optional): Factor to enhance colors. Defaults to 1.5.
    """
    image = Image.open(image_path)
    edges = image.filter(ImageFilter.FIND_EDGES)
    edges = ImageEnhance.Contrast(edges).enhance(edge_enhance)
    neon_image = ImageEnhance.Color(edges).enhance(color_enhance)
    neon_image.save(output_path)


def apply_posterize(image_path, output_path, bits=4):
    """
    Apply posterize effect to an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        bits (int, optional): Number of bits to use for each color channel. Defaults to 4.
    """
    image = Image.open(image_path)
    posterized_image = ImageOps.posterize(image, bits)
    posterized_image.save(output_path)


def apply_solarize(image_path, output_path, threshold=128):
    """
    Apply solarize effect to an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        threshold (int, optional): Threshold value above which to invert pixel values. Defaults to 128.
    """
    image = Image.open(image_path)
    solarized_image = ImageOps.solarize(image, threshold)
    solarized_image.save(output_path)


from PIL import Image, ImageFilter, ImageEnhance


def apply_comic_book(image_path, output_path, edge_enhance=1.5, color_enhance=1.5):
    """
    Apply comic book effect to an image.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        edge_enhance (float, optional): Factor to enhance edges. Defaults to 1.5.
        color_enhance (float, optional): Factor to enhance colors. Defaults to 1.5.
    """
    image = Image.open(image_path)
    edges = image.filter(ImageFilter.CONTOUR)
    edges = ImageEnhance.Contrast(edges).enhance(edge_enhance)
    comic_image = ImageEnhance.Color(edges).enhance(color_enhance)
    comic_image.save(output_path)


def apply_3d_effect(image_path, output_path, shift=5):
    """
    Apply 3D effect to an image by shifting the red and blue channels.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the output image.
        shift (int, optional): Number of pixels to shift the channels. Defaults to 5.
    """
    image = Image.open(image_path)
    r, g, b = image.split()
    r = ImageChops.offset(r, shift, 0)
    b = ImageChops.offset(b, -shift, 0)
    _3d_image = Image.merge("RGB", (r, g, b))
    _3d_image.save(output_path)


def main():
    # Example usage
    image_path = "../temp/test.png"
    output_3d_path = "../temp/output_3d.jpg"
    output_comic_path = "../temp/output_comic.jpg"
    output_solarize_path = "../temp/output_solarize.jpg"
    output_posterize_path = "../temp/output_posterize.jpg"
    output_neon_glow = "../temp/output_neon.jpg"
    output_crosseprocessing_path = "../temp/output_cross.jpg"
    output_duo_path = "../temp/output_duo.jpg"
    output_infrared_path = "../temp/output_infrared.jpg"
    output_lomo_path = "../temp/output_lomo.jpg"
    output_orton_path = "../temp/output_orton.jpg"
    output_hdr_path = "../temp/output_hdr.jpg"
    output_temp_path_W = "../temp/output_temp_W.jpg"
    output_temp_path_C = "../temp/output_temp_C.jpg"

    apply_3d_effect(image_path, output_3d_path, shift=50)
    apply_comic_book(image_path, output_comic_path)
    apply_solarize(image_path, output_solarize_path, threshold=128)
    apply_posterize(image_path, output_posterize_path, bits=3)
    apply_neon_glow(image_path, output_neon_glow)
    apply_cross_processing(image_path, output_crosseprocessing_path)
    apply_duotone(
        image_path, output_duo_path, color1=(0, 128, 128), color2=(255, 128, 0)
    )
    apply_infrared(image_path, output_infrared_path)
    apply_lomography(image_path, output_lomo_path)
    apply_orton(image_path, output_orton_path)
    apply_hdr(image_path, output_hdr_path)


if __name__ == "__main__":
    main()
