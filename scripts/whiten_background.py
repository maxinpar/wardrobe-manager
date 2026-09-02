"""Whiten the flat studio backdrop on a render without touching the garment.

A pixel is only changed when it is (a) close to the sampled border colour,
(b) bright, (c) NOT on an edge, and (d) connected to the image border through
other such pixels. The edge barrier is what protects pale garments: a white
polo on a light-grey backdrop still has a silhouette, and the fill stops there.

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


def whiten(path, out, tol=34, bright=196, feather=1.6, edge=5.0):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape

    edge_px = np.concatenate([a[:3].reshape(-1, 3), a[-3:].reshape(-1, 3),
                              a[:, :3].reshape(-1, 3), a[:, -3:].reshape(-1, 3)])
    bg = np.median(edge_px, axis=0)

    # edge barrier: the garment silhouette, even a pale one against pale grey
    g = im.convert("L").filter(ImageFilter.GaussianBlur(1.0))
    e = np.asarray(g.filter(ImageFilter.FIND_EDGES)).astype(np.float32)
    barrier = e > edge

    dist = np.sqrt(((a - bg) ** 2).sum(axis=2))
    mask = (dist < tol) & (a.min(axis=2) >= bright) & (~barrier)

    # flood fill at quarter scale for speed, then refine at full resolution
    sm = Image.fromarray((mask * 255).astype(np.uint8)).resize(
        (w // 4, h // 4), Image.NEAREST)
    keep_s = _edge_connected(np.asarray(sm) > 127)
    keep = np.asarray(Image.fromarray((keep_s * 255).astype(np.uint8))
                      .resize((w, h), Image.BILINEAR)) > 40
    bgmask = mask & keep

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
