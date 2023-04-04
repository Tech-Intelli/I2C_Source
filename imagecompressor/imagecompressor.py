from PIL import Image
import os


class ImageCompressor:
    def get_compressed_image(self, image_path) -> os.path:
        compressed_image_path = image_path.split('.jpg')[0] + '_compressed.jpg'
        return compressed_image_path

    def compress(self, image_path, compression_quality=50) -> os.path:
        image = Image.open(image_path)
        if os.path.getsize(image_path) > 2 * 1024 * 1024:
            new_size = (image.size[0] // 2, image.size[1] // 2)
            compressed_image_path = self.get_compressed_image(image_path)
            image.resize(new_size).save(compressed_image_path,
                                        optimize=True,
                                        quality=compression_quality,
                                        exif=image.info.get('exif'))
        else:
            compressed_image_path = image_path
        return compressed_image_path
