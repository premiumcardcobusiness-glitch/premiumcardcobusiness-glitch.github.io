"""Build the slab guard product shots for guards.html from Kenny's phone photos.

Each photo becomes the guard alone on a dark gradient: the guard is cut out with a hand-measured outline
(threshold masks caught the bedsheet's shadows and folds as "guard"), the outline is pulled in a few pixels
before it is feathered so no bedsheet grey rides along the edge, and the result is written at 1600px and 800px
on the long side as WebP. The front shot is perspective-corrected to a flat rectangle first.

Outlines are in "thumb" coordinates: the photo after EXIF rotation, scaled so its long side is 1000px.
Run: python make_guard_images.py  (writes next to this file)
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

SRC = r"C:\Users\Solis\.claude\uploads\97c312ac-6c46-497b-a7bf-facb52842ab2"
OUT = os.path.dirname(os.path.abspath(__file__))

TOP, BOTTOM = (0x0b, 0x0f, 0x1a), (0x11, 0x18, 0x27)

# The front shot: outer corners of the guard (TL, TR, BR, BL) in full-resolution pixels. The bottom pair sits
# on the base of the front wall, so the flattened shot shows the guard's full height.
HERO_CORNERS = [(390, 293), (1424, 306), (1570, 2198), (160, 2198)]
# Width over height of the flattened guard. Chosen so the card inside comes out at its real 63x88 mm shape.
HERO_ASPECT = 0.604
HERO_RADIUS = 0.045  # corner rounding, as a share of the guard's width

SHOTS = {
    "side-profile": ("19a43e6d", [(240, 220), (330, 222), (640, 244), (712, 249), (722, 254), (840, 342),
                                  (846, 352), (837, 390), (830, 402), (640, 400), (330, 390), (138, 380),
                                  (128, 376), (119, 315), (122, 310)]),
    "angle-1": ("72f3232e", [(344, 218), (352, 210), (586, 132), (600, 132), (610, 142), (615, 170), (392, 660),
                             (342, 766), (330, 772), (316, 770), (80, 626), (76, 612), (89, 600)]),
    "angle-2": ("e5a3222a", [(290, 206), (297, 199), (544, 171), (555, 175), (558, 185), (530, 280), (436, 480),
                             (372, 606), (362, 620), (346, 630), (330, 632), (280, 624), (200, 603), (89, 577),
                             (0, 543), (0, 492)]),
    # Close-up of the embossed edge. The outline drops the white desk, the keyboard and the second guard.
    "edge-logo": ("59616b00", [(0, 322), (236, 219), (509, 217), (520, 222), (606, 256), (750, 326), (750, 472),
                               (0, 478)]),
}


def load(photo_id):
    return ImageOps.exif_transpose(Image.open(os.path.join(SRC, photo_id + "-image.jpg"))).convert("RGB")


def gradient(size):
    w, h = size
    t = np.linspace(0.0, 1.0, h)[:, None, None]
    rows = np.array(TOP) * (1 - t) + np.array(BOTTOM) * t
    return Image.fromarray(np.broadcast_to(rows, (h, w, 3)).astype("uint8"), "RGB")


def feather(mask, long_side):
    # Erode before blurring so the soft edge starts inside the guard; blurring the raw outline mixes the
    # light bedsheet into the dark background and leaves a grey halo.
    inset = max(3, round(long_side / 700)) | 1
    return mask.filter(ImageFilter.MinFilter(inset)).filter(ImageFilter.GaussianBlur(inset / 2))


def compose(photo, mask, pad_share=0.07):
    """Crop to the mask with a margin, level the guard's exposure, and lay it on the gradient."""
    box = mask.getbbox()
    pad = round(max(box[2] - box[0], box[3] - box[1]) * pad_share)
    # Where the guard runs off the photo, let it run off the shot too; a margin there shows a straight cut.
    w, h = mask.size
    box = (box[0] - pad if box[0] > 0 else 0, box[1] - pad if box[1] > 0 else 0,
           box[2] + pad if box[2] < w else w, box[3] + pad if box[3] < h else h)
    photo, mask = photo.crop(box), mask.crop(box)  # outside the photo crops as black / unmasked
    photo = ImageOps.autocontrast(photo, cutoff=0.5, mask=mask.point(lambda v: 255 if v > 250 else 0))
    return Image.composite(photo, gradient(photo.size), mask)


def perspective_coeffs(src, dst):
    # PIL maps each output pixel back into the input, so solve for the transform taking dst corners to src.
    rows, rhs = [], []
    for (x, y), (u, v) in zip(dst, src):
        rows.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        rows.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        rhs += [u, v]
    return np.linalg.solve(np.array(rows, float), np.array(rhs, float)).tolist()


def hero_front():
    photo = load("3f9bfbfb")
    gh = 2000
    gw = round(gh * HERO_ASPECT)
    m = round(gh * 0.03)  # warp a little past the outline so the feather has real pixels to work with
    dst = [(m, m), (m + gw, m), (m + gw, m + gh), (m, m + gh)]
    flat = photo.transform((gw + 2 * m, gh + 2 * m), Image.PERSPECTIVE, perspective_coeffs(HERO_CORNERS, dst),
                           Image.BICUBIC)
    mask = Image.new("L", flat.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((m, m, m + gw, m + gh), radius=round(gw * HERO_RADIUS), fill=255)
    return compose(flat, feather(mask, gh))


def outlined(photo_id, outline):
    photo = load(photo_id)
    scale = max(photo.size) / 1000
    mask = Image.new("L", photo.size, 0)
    ImageDraw.Draw(mask).polygon([(x * scale, y * scale) for x, y in outline], fill=255)
    return compose(photo, feather(mask, max(photo.size)))


def fit(img, long_side):
    k = long_side / max(img.size)
    return img.resize((round(img.width * k), round(img.height * k)), Image.LANCZOS)


def save(name, img):
    for long_side, suffix in ((1600, ""), (800, "-800")):
        out = fit(img, long_side).filter(ImageFilter.UnsharpMask(radius=1.2, percent=40, threshold=3))
        out.save(os.path.join(OUT, f"{name}{suffix}.webp"), "WEBP", quality=82, method=6)


def og_image(hero):
    W, H = 1200, 630
    card = gradient((W, H))
    shot = fit(hero, 590)
    card.paste(shot, (70, (H - shot.height) // 2))
    d = ImageDraw.Draw(card)
    fonts = r"C:\Windows\Fonts"
    title = ImageFont.truetype(os.path.join(fonts, "segoeuib.ttf"), 96)
    site = ImageFont.truetype(os.path.join(fonts, "segoeuib.ttf"), 46)
    x = 70 + shot.width + 70
    d.text((x, 215), "Slab Guard", font=title, fill=(242, 242, 242))
    d.text((x, 345), "beltstra.com", font=site, fill=(0x4a, 0xde, 0x80))
    card.save(os.path.join(OUT, "guards-og.jpg"), "JPEG", quality=88)


if __name__ == "__main__":
    hero = hero_front()
    save("hero-front", hero)
    for name, (photo_id, outline) in SHOTS.items():
        save(name, outlined(photo_id, outline))
    og_image(hero)
