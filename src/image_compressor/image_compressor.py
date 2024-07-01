"""Compresses an image

Returns:
    str: Compressed Image Path
"""

# pylint: disable=E0401
# pylint: disable=R0903

import os
import io
from PIL import Image
from logger import log


def compress_jpg(
    image_path: str, compression_quality: int = 30, resize_factor: float = 0.3
) -> os.path:
    """
    Compresses an image file and returns the path to the compressed image.

    Args:
        image_path (str): The path to the image file to compress.
        compression_quality (int): The quality of the compressed image.
            Default is 50.

    Returns:
        str: The path to the compressed image.
    """
    compressed_image_path = os.path.splitext(image_path)[0] + "_compressed.jpg"
    image = Image.open(image_path)

    if os.path.getsize(image_path) > 2 * 1024 * 1024:
        new_size = (
            int(image.size[0] * resize_factor),
            int(image.size[1] * resize_factor),
        )
        image.resize(new_size, Image.LANCZOS).save(
            compressed_image_path,
            optimize=True,
            quality=compression_quality,
            exif=image.info.get("exif"),
        )
    else:
        compressed_image_path = image_path
    return compressed_image_path


def compresstoWebP(
    image_data, compression_quality: int = 50, resize_factor: float = 0.5
) -> str:
    """
    Compresses an image file to WebP format and returns the in-memory compressed image.

    Args:
        image_data (bytes): The in-memory image data to compress.
        compression_quality (int): The quality of the compressed image. Default is 50.
        resize_factor (float): The factor by which to resize the image. Default is 0.5.

    Returns:
        io.BytesIO: The in-memory compressed image.
    """
    image = Image.open(io.BytesIO(image_data))
    old_size = len(image_data)
    new_size = (int(image.size[0] * resize_factor), int(image.size[1] * resize_factor))
    image = image.resize(new_size, Image.LANCZOS)

    compressed_image = io.BytesIO()
    image.save(compressed_image, "WEBP", quality=compression_quality)
    compressed_image.seek(0)

    new_size_bytes = compressed_image.getbuffer().nbytes
    log.info(
        f"File has been compressed from {old_size} bytes to {new_size_bytes} bytes."
    )

    return compressed_image
