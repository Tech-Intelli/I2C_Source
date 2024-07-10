import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

import time
from utils.logger import log
from PIL import Image
from processor.image_processor.effects.color_effects import (
    black_and_white,
    grayscale,
    selective_color,
    invert_colors,
    sepia,
)
from processor.image_processor.enhance.img_enhancer import (
    adjust_brightness,
    adjust_clarity,
    adjust_contrast,
    adjust_gamma,
    adjust_saturation,
    adjust_hue,
    adjust_sharpness,
    adjust_temperature,
    flip_image,
    rotate_image,
    apply_vignette,
    apply_color_splash,
)
from processor.image_processor.effects.special_effects import (
    cartoon,
    comic_book,
    duotone,
    hdr,
    orton,
    glitch,
    pixelate,
    pop_art,
    posterize,
    retro_vintage,
    sketch,
    solarize,
    t3d_effect,
    cross_processing,
    infrared,
    lomography,
    neon_glow,
    watercolor,
    gotham_filter,
)

from processor.image_processor.filters.in1977 import (
    apply_1977_filter, 
    apply_1990_filter,
)
from processor.image_processor.filters.juno import juno
    
from processor.image_processor.filters.summer import summer_filter
from processor.image_processor.filters.winter import winter_filter



def time_it(method):
    def timed(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        if duration > 1:
            log.error(f"{method.__name__} Duration:  {duration:.4f} seconds")
        else:
            log.info(f"{method.__name__} Duration:  {duration:.4f} seconds")
        return result

    return timed


class TestImageProcessing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.image_path = "../tests/test_resources/images/test.png"
        cls.image = Image.open(cls.image_path)

        cls.temp_dir = "../temp"
        if not os.path.exists(cls.temp_dir):
            os.makedirs(cls.temp_dir)

    def check_image_saved(self, image, output_path):
        image.save(output_path)
        self.assertTrue(os.path.exists(output_path), f"{output_path} not saved.")

    @time_it
    def test_invert_colors(self):
        img = invert_colors(self.image)
        output_path = os.path.join(self.temp_dir, "output_invert.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_black_and_white(self):
        img = black_and_white(self.image, 128)
        output_path = os.path.join(self.temp_dir, "output_bw.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_sepia(self):
        img = sepia(self.image, 75)
        output_path = os.path.join(self.temp_dir, "output_sepia.jpg")
        self.check_image_saved(img, output_path)

        img = sepia(self.image, 100)
        output_path = os.path.join(self.temp_dir, "output_sepia2.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_selective_color(self):
        img = selective_color(self.image, "blue", 1.5)
        output_path = os.path.join(self.temp_dir, "output_selective_blue.jpg")
        self.check_image_saved(img, output_path)

        img = selective_color(self.image, "red", 1.5)
        output_path = os.path.join(self.temp_dir, "output_selective_red.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_grayscale(self):
        img = grayscale(self.image, 80)
        output_path = os.path.join(self.temp_dir, "output_grayscale.jpg")
        self.check_image_saved(img, output_path)

        img = grayscale(self.image, 100)
        output_path = os.path.join(self.temp_dir, "output_grayscale1.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_t3d_effect(self):
        img = t3d_effect(self.image, shift=50)
        output_path = os.path.join(self.temp_dir, "output_3d.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_comic_book(self):
        img = comic_book(self.image)
        output_path = os.path.join(self.temp_dir, "output_comic.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_solarize(self):
        img = solarize(self.image, threshold=128)
        output_path = os.path.join(self.temp_dir, "output_solarize.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_posterize(self):
        img = posterize(self.image, bits=3)
        output_path = os.path.join(self.temp_dir, "output_posterize.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_neon_glow(self):
        img = neon_glow(self.image)
        output_path = os.path.join(self.temp_dir, "output_neon.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_cross_processing(self):
        img = cross_processing(self.image)
        output_path = os.path.join(self.temp_dir, "output_cross.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_duotone(self):
        img = duotone(self.image, color1=(0, 128, 128), color2=(255, 128, 0))
        output_path = os.path.join(self.temp_dir, "output_duo.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_infrared(self):
        img = infrared(self.image)
        output_path = os.path.join(self.temp_dir, "output_infrared.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_lomography(self):
        img = lomography(self.image)
        output_path = os.path.join(self.temp_dir, "output_lomo.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_orton(self):
        img = orton(self.image)
        output_path = os.path.join(self.temp_dir, "output_orton.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_hdr(self):
        img = hdr(self.image)
        output_path = os.path.join(self.temp_dir, "output_hdr.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_adjust_contrast(self):
        img = adjust_contrast(self.image, 1.5)  # Increase contrast by 50%
        output_path = os.path.join(self.temp_dir, "output_contrast.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_adjust_brightness(self):
        img = adjust_brightness(self.image, 0.2)
        output_path = os.path.join(self.temp_dir, "output_brightness.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_adjust_sharpness(self):
        img = adjust_sharpness(self.image, 2.0)
        output_path = os.path.join(self.temp_dir, "output_sharpness.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_adjust_gamma(self):
        img = adjust_gamma(self.image, 0.5)
        output_path = os.path.join(self.temp_dir, "output_gamma.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_adjust_clarity(self):
        img = adjust_clarity(self.image, 1.5)
        output_path = os.path.join(self.temp_dir, "output_clarity.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_adjust_saturation(self):
        img = adjust_saturation(self.image, 1.5)
        output_path = os.path.join(self.temp_dir, "output_color.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_rotate_image(self):
        img = rotate_image(self.image, 90)
        output_path = os.path.join(self.temp_dir, "output_rotate.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_adjust_hue(self):
        img = adjust_hue(self.image, hue_shift=30)
        output_path = os.path.join(self.temp_dir, "output_hue.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_flip_image(self):
        img = flip_image(self.image, "horizontal")
        output_path = os.path.join(self.temp_dir, "output_flip.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_adjust_temperature(self):
        img = adjust_temperature(self.image, temp_factor=1.5)  # Warmer
        output_path = os.path.join(self.temp_dir, "output_temp_W.jpg")
        self.check_image_saved(img, output_path)

        img = adjust_temperature(self.image, temp_factor=0.7)  # Cooler
        output_path = os.path.join(self.temp_dir, "output_temp_C.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_glitch(self):
        img = glitch(self.image, max_shift=20)
        output_path = os.path.join(self.temp_dir, "output_glitch.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_watercolor(self):
        img = watercolor(self.image)
        output_path = os.path.join(self.temp_dir, "output_watercolor.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_cartoon(self):
        img = cartoon(self.image)
        output_path = os.path.join(self.temp_dir, "output_cartoon.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_pop_art(self):
        img = pop_art(self.image)
        output_path = os.path.join(self.temp_dir, "output_pop_art.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_pixelate(self):
        img = pixelate(self.image, pixel_size=20)
        output_path = os.path.join(self.temp_dir, "output_pixelate.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_retro_vintage(self):
        img = retro_vintage(self.image)
        output_path = os.path.join(self.temp_dir, "output_retro_vintage.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_sketch(self):
        img = sketch(self.image)
        output_path = os.path.join(self.temp_dir, "output_sketch.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_vignette(self):
        img = apply_vignette(self.image)
        output_path = os.path.join(self.temp_dir, "output_vignette.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_gotham_filter(self):
        img = gotham_filter(self.image)
        output_path = os.path.join(self.temp_dir, "output_gotham.jpg")
        self.check_image_saved(img, output_path)

    @time_it
    def test_color_splash(self):
        tc = (255, 0, 0)
        img = apply_color_splash(self.image, tc)
        output_path = os.path.join(self.temp_dir, "output_color_splash.jpg")
        self.check_image_saved(img, output_path)

        
    @time_it
    def test_in1977(self):
        img = apply_1977_filter(self.image)
        output_path = os.path.join(self.temp_dir, "output_in1977.jpg")
        self.check_image_saved(img, output_path)

        
    @time_it
    def test_in1990(self):
        img = apply_1990_filter(self.image)
        output_path = os.path.join(self.temp_dir, "output_in1990.jpg")
        self.check_image_saved(img, output_path)

        
    @time_it
    def test_juno(self):
        
        img = juno(self.image)
        output_path = os.path.join(self.temp_dir, "output_color_juno.jpg")
        self.check_image_saved(img, output_path)

        
    @time_it
    def test_summer(self):
        img = summer_filter(self.image)
        output_path = os.path.join(self.temp_dir, "output_color_summer.jpg")
        self.check_image_saved(img, output_path)

        
    @time_it
    def test_winter(self):
        img = winter_filter(self.image)
        output_path = os.path.join(self.temp_dir, "output_winter.jpg")
        self.check_image_saved(img, output_path)


if __name__ == "__main__":
    unittest.main()
