from PIL import Image
import os


class ImageCompressor:
    def compress(self, image_path, compression_quality=50):
        image = Image.open(image_path)
        if os.path.getsize(image_path) > 2 * 1024 * 1024:
            new_size = (image.size[0] // 2, image.size[1] // 2)
            compressed_image_path = 'test_compressed.jpg'
            image.resize(new_size).save(compressed_image_path,
                                        optimize=True,
                                        quality=compression_quality,
                                        exif=image.info.get('exif'))
        else:
            compressed_image_path = image_path
