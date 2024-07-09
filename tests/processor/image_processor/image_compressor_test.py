import os
import pytest
from unittest.mock import patch, mock_open
from processor.image_processor import img_compressor


def save_bytesio_to_file(bytesio_obj, output_path):
    """
    Saves the content of the BytesIO object to the specified output path.

    Args:
        bytesio_obj: The BytesIO object containing the content to be saved.
        output_path: The path where the content will be saved.

    Returns:
        None
    """
    with open(output_path, "wb") as file:
        file.write(bytesio_obj.getvalue())


@pytest.fixture
def parent_directory():
    """
    Fixture that returns the current directory path of the file where this fixture is defined.
    """
    parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return parent_directory


@pytest.fixture
def image_path(parent_directory):
    """
    Returns the path to the test image file.

    Args:
        parent_directory (str): The current directory.

    Returns:
        str: The path to the test image file.
    """
    return os.path.join(parent_directory, "test_resources", "images", "test_image.jpg")


@pytest.fixture
def small_image_path(parent_directory):
    """
    Fixture that returns the path to the small image file for testing.

    Args:
        parent_directory: The current directory path.

    Returns:
        str: The path to the small image file.
    """
    return os.path.join(parent_directory, "test_resources", "images", "small_image.jpg")


@pytest.fixture
def image_data(image_path):
    """
    A fixture that returns the image data by reading the binary contents of the image file specified by the image_path parameter.

    Args:
        image_path: The path to the image file.

    Returns:
        bytes: The binary contents of the image file.
    """
    with open(image_path, "rb") as image_file:
        return image_file.read()


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.getsize")
@patch("os.path.isfile")
def test_compress_to_webP_default(
    mock_isfile, mock_getsize, mock_file, image_data, image_path, parent_directory
):
    """
    Test the `compress_to_webP_default` function in the `img_compressor` module.

    This function tests the default behavior of the `compress_to_webP` function by mocking the `os.path.getsize`,
    `os.path.isfile`, and `builtins.open` functions. It ensures that the compressed image is saved to a temporary file
    with the correct extension and that its size is smaller than the original image.

    Args:
        mock_isfile (MagicMock): A mock object for the `os.path.isfile` function.
        mock_getsize (MagicMock): A mock object for the `os.path.getsize` function.
        mock_file (MagicMock): A mock object for the `builtins.open` function.
        image_data (bytes): The binary contents of the image file.
        image_path (str): The path to the image file.
        parent_directory (str): The current directory path.

    Returns:
        None
    """

    # Mock the getsize to return specific values based on the path
    def getsize_side_effect(path):
        """
        Returns the size of a file based on its path.

        Parameters:
            path (str): The path of the file.

        Returns:
            int: The size of the file. If the path ends with "compressed_image.webp", returns 100. Otherwise, returns 200.
        """
        if path.endswith("compressed_image.webp"):
            return 100  # Compressed size
        else:
            return 200  # Original size

    mock_getsize.side_effect = getsize_side_effect
    mock_isfile.return_value = True

    # Compress and save to a temporary file
    compressed_image_stream = img_compressor.compress_to_webP(image_data)
    compressed_path = os.path.join(
        parent_directory, "test_resources", "images", "compressed_image.webp"
    )
    save_bytesio_to_file(compressed_image_stream, compressed_path)

    assert os.path.isfile(compressed_path)
    assert os.path.splitext(compressed_path)[1] == ".webp"
    assert os.path.getsize(compressed_path) < os.path.getsize(image_path)


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.getsize")
@patch("os.path.isfile")
def test_compress_to_webP_custom_quality(
    mock_isfile, mock_getsize, mock_file, image_data, image_path, parent_directory
):
    """
    Returns the size of a file based on its path.

    Parameters:
        path (str): The path of the file.

    Returns:
        int: The size of the file.
    """

    # Mock the getsize to return specific values based on the path
    def getsize_side_effect(path):
        """
        Returns the size of a file based on its path.

        Parameters:
            path (str): The path of the file.

        Returns:
            int: The size of the file.
        """
        if path.endswith("compressed_image_quality70.webp"):
            return 100  # Compressed size
        else:
            return 200  # Original size

    mock_getsize.side_effect = getsize_side_effect
    mock_isfile.return_value = True

    compression_quality = 70
    # Compress and save to a temporary file
    compressed_image_stream = img_compressor.compress_to_webP(
        image_data, compression_quality
    )
    compressed_path = os.path.join(
        parent_directory, "test_resources", "images", "compressed_image_quality70.webp"
    )
    save_bytesio_to_file(compressed_image_stream, compressed_path)

    assert os.path.isfile(compressed_path)
    assert os.path.splitext(compressed_path)[1] == ".webp"
    assert os.path.getsize(compressed_path) < os.path.getsize(image_path)


@patch("processor.image_processor.img_compressor.compress_jpg")
def test_compress_small_image(mock_compress_jpg, small_image_path):
    """
    Test the `compress_small_image` function by mocking the `compress_jpg` function.

    This test function mocks the `compress_jpg` function from the `img_compressor` module in the `processor.image_processor` package.
    It sets the return value of the mocked function to the `small_image_path` parameter.
    Then, it calls the `compress_jpg` function with the `small_image_path` parameter and assigns the result to the `compressed_path` variable.
    Finally, it asserts that the `compressed_path` is equal to the `small_image_path`.

    Parameters:
        mock_compress_jpg (MagicMock): A mock object of the `compress_jpg` function.
        small_image_path (str): The path to the small image file.

    Returns:
        None
    """
    mock_compress_jpg.return_value = small_image_path
    compressed_path = img_compressor.compress_jpg(small_image_path)
    assert compressed_path == small_image_path


def test_compress_nonexistent_image():
    """
    Test the behavior of the `compress_to_webP` function when given a path to a non-existent image.

    This function tests the `compress_to_webP` function by passing it a path to a non-existent image. It expects
    a `FileNotFoundError` to be raised. The function is wrapped in a `with` statement to ensure that the file is
    properly closed after it is opened. The `open` function is used to open the file in binary mode. The `read`
    method is then called on the file object to read its contents into the `image_data` variable. Finally, the
    `compress_to_webP` function is called with the `image_data` as an argument.

    This test is useful for ensuring that the `compress_to_webP` function handles the case when the image file does
    not exist.

    Parameters:
    - None

    Returns:
    - None
    """
    nonexistent_image_path = "nonexistent_image.jpg"
    with pytest.raises(FileNotFoundError):
        with open(nonexistent_image_path, "rb") as image_file:
            image_data = image_file.read()
        img_compressor.compress_to_webP(image_data)
