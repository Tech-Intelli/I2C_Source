"""
Unit Test Case Image Compression Method
"""

import os
# pylint: disable=E0401
from imagecompressor import ImageCompressor


def test_compress():
    """
    Test Image Compression
    """
    # Test case 1: Compress image with default compression quality
    image_path = 'tests/test_resources/images/test_image.jpg'
    compressed_path = ImageCompressor.compress(image_path)
    assert os.path.isfile(compressed_path)
    assert os.path.splitext(compressed_path)[1] == '.jpg'
    assert os.path.getsize(compressed_path) < os.path.getsize(image_path)
    os.remove(compressed_path)

    # Test case 2: Compress image with custom compression quality
    image_path = 'tests/test_resources/images/test_image.jpg'
    compression_quality = 70
    compressed_path = ImageCompressor.compress(image_path, compression_quality)
    assert os.path.isfile(compressed_path)
    assert os.path.splitext(compressed_path)[1] == '.jpg'
    assert os.path.getsize(compressed_path) < os.path.getsize(image_path)
    os.remove(compressed_path)

    # Test case 3: Compress small image, should return same image path
    image_path = 'tests/test_resources/images/small_image.jpg'
    compressed_path = ImageCompressor.compress(image_path)
    assert compressed_path == image_path

    # Test case 4: Compress non-existent image, should raise FileNotFoundError
    image_path = 'nonexistent_image.jpg'
    try:
        ImageCompressor.compress(image_path)
    except FileNotFoundError:
        assert True
    else:
        assert False
