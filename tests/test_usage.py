import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

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
)
from processor.mage_processor.effects.special_effects import (
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
)


def main():

    image_path = "test_resources/images/test.png"
    image = Image.open(image_path)

    # create temp directory if it doesn't exist
    if not os.path.exists("../temp"):
        os.makedirs("../temp")

    output_bw_path = "../temp/output_bw.jpg"
    output_sepia_path = "../temp/output_sepia.jpg"
    output_sepia2_path = "../temp/output_sepia2.jpg"
    output_selective_path_blue = "../temp/output_selective_blue.jpg"
    output_selective_path_red = "../temp/output_selective_red.jpg"
    output_path_sharpness = "../temp/output_sharpness.jpg"
    output_gamma_path = "../temp/output_gamma.jpg"
    output_grayscale_path = "../temp/output_grayscale.jpg"
    output_grayscale1_path = "../temp/output_grayscale1.jpg"
    output_rotate_path = "../temp/output_rotate.jpg"
    output_invert_path = "../temp/output_invert.jpg"
    output_clarity_path = "../temp/output_clarifty.jpg"
    output_hue_path = "../temp/output_hue.jpg"
    output_temp_path_W = "../temp/output_temp_W.jpg"
    output_temp_path_C = "../temp/output_temp_C.jpg"
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
    output_path_contrast = "../temp/output_contrast.jpg"
    output_path_brightness = "../temp/output_brightness.jpg"
    output_path_color = "../temp/output_color.jpg"
    output_path_sharpness = "../temp/output_sharpness.jpg"
    output_gamma_path = "../temp/output_gamma.jpg"
    output_grayscale_path = "../temp/output_grayscale.jpg"
    output_rotate_path = "../temp/output_rotate.jpg"
    output_flip_path = "../temp/output_flip.jpg"
    output_clarity_path = "../temp/output_clarifty.jpg"
    output_hue_path = "../temp/output_hue.jpg"
    output_temp_path_W = "../temp/output_temp_W.jpg"
    output_temp_path_C = "../temp/output_temp_C.jpg"
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
    output_glitch = "../temp/output_glitch.jpg"
    output_retro_vintage = "../temp/output_retro_vintage.jpg"
    output_watercolor = "../temp/output_watercolor.jpg"
    output_sketch = "../temp/output_sketch.jpg"
    output_cartoon = "../temp/output_cartoon.jpg"
    output_pop_art = "../temp/output_pop_art.jpg"
    output_pixelate = "../temp/output_pixelate.jpg"

    img = invert_colors(image)
    img.save(output_invert_path)

    img = black_and_white(image, 128)
    img.save(output_bw_path)

    img = sepia(image, 75)
    img.save(output_sepia_path)

    img = sepia(image, 100)
    img.save(output_sepia2_path)

    img = selective_color(image, "blue", 1.5)
    img.save(output_selective_path_blue)
    img = selective_color(image, "red", 1.5)
    img.save(output_selective_path_red)

    img = grayscale(image, 80)
    img.save(output_grayscale_path)
    img = grayscale(image, 100)
    img.save(output_grayscale1_path)

    img = t3d_effect(image, shift=50)
    img.save(output_3d_path)

    img = comic_book(image)
    img.save(output_comic_path)

    img = solarize(image, threshold=128)
    img.save(output_solarize_path)

    img = posterize(image, bits=3)
    img.save(output_posterize_path)

    img = neon_glow(image)
    img.save(output_neon_glow)

    img = cross_processing(image)
    img.save(output_crosseprocessing_path)

    img = duotone(image, color1=(0, 128, 128), color2=(255, 128, 0))
    img.save(output_duo_path)

    img = infrared(image)
    img.save(output_infrared_path)

    img = lomography(image)
    img.save(output_lomo_path)

    img = orton(image)
    img.save(output_orton_path)

    img = hdr(image)
    img.save(output_hdr_path)

    img = adjust_contrast(image, 1.5)  # Increase contrast by 50%
    img.save(output_path_contrast)

    img = adjust_brightness(image, 0.2)
    img.save(output_path_brightness)

    img = adjust_sharpness(image, 2.0)
    img.save(output_path_sharpness)

    img = adjust_gamma(image, 0.5)
    img.save(output_gamma_path)

    img = adjust_clarity(image, 1.5)
    img.save(output_clarity_path)

    img = adjust_saturation(image, 1.5)
    img.save(output_path_color)

    img = rotate_image(image, 90)
    img.save(output_rotate_path)

    img = adjust_hue(image, hue_shift=30)
    img.save(output_hue_path)

    img = flip_image(image, "horizontal")
    img.save(output_flip_path)

    img = adjust_temperature(image, temp_factor=1.5)  # Warmer
    img.save(output_temp_path_W)
    img = adjust_temperature(image, temp_factor=0.7)  # Cooler
    img.save(output_temp_path_C)

    img = glitch(image, max_shift=20)
    img.save(output_glitch)

    img = watercolor(image)
    img.save(output_watercolor)

    # sketch(image)
    # image.save(output_sketch)

    img = cartoon(image)
    img.save(output_cartoon)

    img = pop_art(image)
    img.save(output_pop_art)

    img = pixelate(image, pixel_size=20)
    img.save(output_pixelate)

    img = retro_vintage(image)
    img.save(output_retro_vintage)


if __name__ == "__main__":
    main()
