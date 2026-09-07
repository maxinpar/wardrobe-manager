"""Whiten the studio backdrop on a render without touching the garment.

v3. The backdrop AND any soft cast shadow are achromatic and no darker than a
floor; the garment is either chromatic or dark or behind a hard silhouette edge.
Only pixels that satisfy the backdrop test AND connect to the image border
through other such pixels are changed.

v2 tested colour DISTANCE from the border shade, which cut soft shadows in half
and left ragged islands (it wrecked tees_04 and hats_23). v3 tests saturation
and luminance instead, so a shadow is taken whole.

Usage:
    python scripts/whiten_background.py <in> <out>
    python scripts/whiten_background.py --dir <in_dir> <out_dir>
"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter


def _edge_connected(mask):
    """Keep only True regions touching the border. numpy-only flood fill."""
    reach = np.zeros_like(mask)
    reach[0], reach[-1], reach[:, 0], reach[:, -1] = (
        mask[0], mask[-1], mask[:, 0], mask[:, -1])
    while True:
        grown = reach.copy()
        grown[1:] |= reach[:-1]
        grown[:-1] |= reach[1:]
        grown[:, 1:] |= reach[:, :-1]
        grown[:, :-1] |= reach[:, 1:]
        grown &= mask
        if grown.sum() == reach.sum():
            return reach
        reach = grown


def whiten(path, out, sat_max=18, lum_floor=150, edge=5.0, feather=1.6):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    sat = a.max(axis=2) - a.min(axis=2)
    lum = a.mean(axis=2)

    frame = np.concatenate([a[:3].reshape(-1, 3), a[-3:].reshape(-1, 3),
                            a[:, :3].reshape(-1, 3), a[:, -3:].reshape(-1, 3)])
    bg = np.median(frame, axis=0)
    bg_lum = float(bg.mean())

    g = im.convert("L").filter(ImageFilter.GaussianBlur(1.0))
    e = np.asarray(g.filter(ImageFilter.FIND_EDGES)).astype(np.float32)
    e[:2, :] = 0; e[-2:, :] = 0; e[:, :2] = 0; e[:, -2:] = 0  # filter's garbage frame
    barrier = e > edge

    region = ((sat <= sat_max) & (lum >= lum_floor)
              & (lum <= bg_lum + 12) & (~barrier))

    sm = Image.fromarray((region * 255).astype(np.uint8)).resize(
        (w // 4, h // 4), Image.NEAREST)
    keep_s = _edge_connected(np.asarray(sm) > 127)
    keep = np.asarray(Image.fromarray((keep_s * 255).astype(np.uint8))
                      .resize((w, h), Image.BILINEAR)) > 40
    bgmask = region & keep

    alpha = np.asarray(Image.fromarray((bgmask * 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(feather))
                       ).astype(np.float32) / 255.0
    res = a.astype(np.float32) * (1 - alpha[..., None]) + 255.0 * alpha[..., None]
    img = Image.fromarray(np.clip(res, 0, 255).astype(np.uint8))
    ext = os.path.splitext(out)[1].lower()
    if ext == ".png":
        img.save(out, "PNG")
    else:
        img.save(out, "JPEG", quality=95, subsampling=0)
    return bg.astype(int).tolist(), float(bgmask.mean())


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--dir"]:
        src, dst = args[1], args[2]
        os.makedirs(dst, exist_ok=True)
        for n in sorted(os.listdir(src)):
            if os.path.splitext(n)[1].lower() not in (".png", ".jpg", ".jpeg"):
                continue
            bg, frac = whiten(os.path.join(src, n), os.path.join(dst, n))
            print(f"{n:56s} bg={bg} bg_area={frac:.3f}")
    else:
        bg, frac = whiten(args[0], args[1])
        print(f"bg={bg} bg_area={frac:.3f}")
