"""
Image compression module
"""

from .img_compressor import compress_jpg, compress_to_webP

from .img_enhancer import (
    adjust_brightness,
    adjust_clarity,
    adjust_contrast,
    adjust_gamma,
    adjust_saturation,
    adjust_hue,
    adjust_sharpness,
    adjust_temperature,
)
from .special_effects import (
    apply_hdr,
    apply_3d_effect,
    apply_cross_processing,
    apply_comic_book,
    apply_posterize,
    apply_solarize,
    apply_duotone,
    apply_infrared,
    apply_lomography,
    apply_orton,
    apply_neon_glow,
)

from .color_adjustments import (
    black_and_white,
    apply_grayscale,
    selective_color,
    invert_colors,
    apply_sepia,
)
