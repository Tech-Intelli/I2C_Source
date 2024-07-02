import os
from unittest.mock import patch, mock_open
from src.image_compressor import image_compressor

def save_bytesio_to_file(bytesio_obj, output_path):
    with open(output_path, 'wb') as file:
        file.write(bytesio_obj.getvalue())

def test_compresstoWebP():
    """
    Test Image Compression
    """
    # Test case 1: Compress image with default compression quality
    current_directory = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(
        current_directory, "test_resources", "images", "test_image.jpg"
    )
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    
    # Compress and save to a temporary file
    compressed_image_stream = image_compressor.compresstoWebP(image_data)
    compressed_path = os.path.join(current_directory, "test_resources", "images", "compressed_image.webp")
    save_bytesio_to_file(compressed_image_stream, compressed_path)

    assert os.path.isfile(compressed_path)
    assert os.path.splitext(compressed_path)[1] == ".webp"
    assert os.path.getsize(compressed_path) < os.path.getsize(image_path)
    os.remove(compressed_path)

    # Test case 2: Compress image with custom compression quality
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    compression_quality = 70
    
    # Compress and save to a temporary file
    compressed_image_stream = image_compressor.compresstoWebP(image_data, compression_quality)
    compressed_path = os.path.join(current_directory, "test_resources", "images", "compressed_image_quality70.webp")
    save_bytesio_to_file(compressed_image_stream, compressed_path)

    assert os.path.isfile(compressed_path)
    assert os.path.splitext(compressed_path)[1] == ".webp"
    assert os.path.getsize(compressed_path) < os.path.getsize(image_path)
    os.remove(compressed_path)

    # Test case 3: Compress small image, should return same image path
    small_image_path = os.path.join(
        current_directory, "test_resources", "images", "small_image.jpg"
    )
    compressed_path = image_compressor.compress_jpg(small_image_path)
    assert compressed_path == small_image_path

    # Test case 4: Compress non-existent image, should raise FileNotFoundError
    nonexistent_image_path = "nonexistent_image.jpg"
    try:
        with open(nonexistent_image_path, "rb") as image_file:
            image_data = image_file.read()
        image_compressor.compresstoWebP(image_data)
    except FileNotFoundError:
        assert True
    else:
        assert False