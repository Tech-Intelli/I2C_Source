"""Compresses an image

Returns:
    str: Compressed Image Path
"""
# pylint: disable=E0401
# pylint: disable=R0903

import os
from PIL import Image

def compressJPG(image_path: str, compression_quality: int = 30, resize_factor: float = 0.3) -> os.path:
    """
    Compresses an image file and returns the path to the compressed image.

    Args:
        image_path (str): The path to the image file to compress.
        compression_quality (int): The quality of the compressed image.
            Default is 50.

    Returns:
        str: The path to the compressed image.
    """
    compressed_image_path = os.path.splitext(image_path)[0] + '_compressed.jpg'
    image = Image.open(image_path)

    if os.path.getsize(image_path) > 2 * 1024 * 1024:
        new_size = (int(image.size[0] * resize_factor), int(image.size[1] * resize_factor))
        image.resize(new_size, Image.LANCZOS).save(compressed_image_path,
                                    optimize=True,
                                    quality=compression_quality,
                                    exif=image.info.get('exif'))
    else:
        compressed_image_path = image_path
    return compressed_image_path



def compresstoWebP(image_path: str, compression_quality: int = 30, resize_factor: float = 0.3) -> str:
    """
    Compresses an image file to WebP format and returns the path to the compressed image.

    Args:
        image_path (str): The path to the image file to compress.
        compression_quality (int): The quality of the compressed image.
            Higher value means better quality. Default is 80.
        resize_factor (float): The factor by which to resize the image.
            Default is 0.5 (50% of original size).

    Returns:
        str: The path to the compressed image.
    """
    compressed_image_path = os.path.splitext(image_path)[0] + '_compressed.webp'
    image = Image.open(image_path)
    old_size = os.path.getsize(image_path)
    # Resize the image
    new_size = (int(image.size[0] * resize_factor), int(image.size[1] * resize_factor))
    image = image.resize(new_size, Image.LANCZOS)
    # Save the image in WebP format
    image.save(compressed_image_path, 'WEBP', quality=compression_quality)

    print(f"==== File has been compressed to webp from {old_size} bytes to {new_size} bytes!")

    return compressed_image_path

