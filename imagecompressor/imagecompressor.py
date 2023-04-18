"""Compresses an image

Returns:
    str: Compressed Image Path
"""
# pylint: disable=E0401
import os
from PIL import Image
# pylint: disable=R0903


class ImageCompressor:
    """
    A class for compressing input images.

    Attributes:
        None

    Methods:
        compress(image_path: str, compression_quality: int = 50) -> str:
            Compresses an input image and returns the path of the compressed image.

            Args:
                image_path (str): The path of the input image.
                compression_quality (int): The quality of the compressed image,
                defaults to 50.

            Returns:
                str: The path of the compressed image.
    """

    @staticmethod
    def compress(image_path, compression_quality=50) -> os.path:
        """
        Compresses an image file and returns the path to the compressed image.

        Args:
            image_path (str): The path to the image file to compress.
            compression_quality (int): The quality of the compressed image.
                Default is 50.

        Returns:
            str: The path to the compressed image.
        """
        compressed_image_path = image_path.split('.jpg')[0] + '_compressed.jpg'
        image = Image.open(image_path)
        if os.path.getsize(image_path) > 2 * 1024 * 1024:
            new_size = (image.size[0] // 2, image.size[1] // 2)
            image.resize(new_size).save(compressed_image_path,
                                        optimize=True,
                                        quality=compression_quality,
                                        exif=image.info.get('exif'))
        else:
            compressed_image_path = image_path
        return compressed_image_path
