"""
Image compression module
"""

from .compression.img_compressor import compress_jpg, compress_to_webP

from .enhance.img_enhancer import (
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
from .effects.special_effects import (
    hdr,
    t3d_effect,
    cross_processing,
    comic_book,
    posterize,
    solarize,
    duotone,
    infrared,
    lomography,
    orton,
    neon_glow,
    cartoon,
    glitch,
    retro_vintage,
    watercolor,
    sketch,
    pixelate,
    pop_art,
    gotham_filter,
)

from .effects.color_effects import (
    black_and_white,
    grayscale,
    selective_color,
    invert_colors,
    sepia,
)
