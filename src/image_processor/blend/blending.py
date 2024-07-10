import numpy as np
from PIL import Image


def blend_images(img1, img2, mode="normal"):
    img1 = img1.convert("RGBA")
    img2 = img2.convert("RGBA")

    np_img1 = np.array(img1).astype(float)
    np_img2 = np.array(img2).astype(float)

    if mode == "normal":
        blended = np_img1
    elif mode == "multiply":
        blended = np_img1 * np_img2 / 255
    elif mode == "screen":
        blended = 255 - ((255 - np_img1) * (255 - np_img2) / 255)
    elif mode == "overlay":
        blended = np.where(
            np_img1 < 128,
            2 * np_img1 * np_img2 / 255,
            255 - 2 * (255 - np_img1) * (255 - np_img2) / 255,
        )
    elif mode == "darken":
        blended = np.minimum(np_img1, np_img2)
    elif mode == "lighten":
        blended = np.maximum(np_img1, np_img2)
    elif mode == "color_dodge":
        blended = np_img2 / (255 - np_img1) * 255
        blended[blended > 255] = 255
    elif mode == "color_burn":
        blended = 255 - ((255 - np_img2) / np_img1 * 255)
        blended[blended < 0] = 0
    elif mode == "hard_light":
        blended = np.where(
            np_img2 < 128,
            2 * np_img1 * np_img2 / 255,
            255 - 2 * (255 - np_img1) * (255 - np_img2) / 255,
        )
    elif mode == "soft_light":
        blended = (np_img1 / 255) * (np_img2 / 255) * (255 - np_img1) + np_img1
        blended = 255 * np.clip(blended, 0, 1)
    elif mode == "difference":
        blended = np.abs(np_img1 - np_img2)
    elif mode == "exclusion":
        blended = np_img1 + np_img2 - 2 * np_img1 * np_img2 / 255
    else:
        raise ValueError(f"Unknown blending mode: {mode}")

    blended = blended.astype("uint8")
    return Image.fromarray(blended)


# Example usage
img1 = Image.open("../temp/test.png")
# Convert to RGBA if not already
if img1.mode != "RGBA":
    image = img1.convert("RGBA")
overlay = Image.new("RGBA", img1.size, (227, 187, 227, int(255 * 0.2)))
blended = Image.blend(img1, overlay, alpha=0.2)
blended_image = blend_images(img1, blended, mode="overlay")
blended_image.show()
