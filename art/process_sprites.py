#!/usr/bin/env python3
"""Turn raw magenta-background renders into game-ready sprites.

Keys out the magenta, removes magenta spill on the edges, crops to the object, rotates so the
front points to +x (the game's facing), scales down and writes WebP with alpha to ../assets/.
Run with the ComfyUI env's python (it has Pillow + numpy):
    ~/miniconda3/envs/comfyui/bin/python process_sprites.py
"""
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "sprites", "raw")
OUT = os.path.join(HERE, "..", "assets")

# name: (which way the front faces in the render, longest side in px after scaling)
SPRITES = {
    "car_hatch": ("up", 256), "car_muscle": ("up", 256), "car_buggy": ("up", 256), "car_dump": ("up", 256), "car_bus": ("up", 320),
    "en_boss": ("up", 256),
    "en_spitter": ("up", 128), "en_walker": ("down", 128), "en_runner": ("down", 128), "en_brute": ("down", 160), "en_swarm": ("down", 96),
    "prop_crate": ("up", 128), "prop_barrel": ("up", 128), "prop_mine": ("up", 96),
    "pick_repair": ("up", 96), "pick_magnet": ("up", 96), "pick_nitro": ("up", 96), "pick_bomb": ("up", 96),
    "gem_scrap": ("up", 64),
}


def key_out(im):
    from scipy import ndimage
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    # how magenta a pixel is: red and blue both well above green
    mag = np.minimum(r, b) - g
    # background = magenta-ish pixels connected to the image border, so purple skin inside the object survives
    cand = mag > 95
    lab, _ = ndimage.label(cand)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    bg = np.isin(lab, border[border > 0]) | (mag > 140)   # plus strongly magenta holes (handles, cages)
    alpha = np.where(bg, 0.0, 1.0)
    # soften a thin band around the cut-out and remove the magenta that bled into it
    band = ndimage.binary_dilation(bg, iterations=7) & ~bg
    soft = np.clip(1 - (mag - 22) / 45, 0, 1)
    alpha = np.where(band, np.minimum(alpha, soft), alpha)
    lim = g + 8
    r = np.where(band, np.minimum(r, lim), r)
    b = np.where(band, np.minimum(b, lim), b)
    out = np.dstack([r, g, b, alpha * 255]).clip(0, 255).astype(np.uint8)
    return Image.fromarray(out, "RGBA")


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (facing, size) in SPRITES.items():
        src = os.path.join(RAW, name + ".png")
        if not os.path.exists(src):
            print("missing", name)
            continue
        im = key_out(Image.open(src))
        # drop faint specks before cropping
        a = np.asarray(im)[..., 3]
        ys, xs = np.where(a > 40)
        im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
        im = im.rotate(-90 if facing == "up" else 90, expand=True, resample=Image.BICUBIC)
        im.thumbnail((size, size), Image.LANCZOS)
        dst = os.path.join(OUT, name + ".webp")
        im.save(dst, "WEBP", quality=88, method=6)
        print(f"{name}: {im.size} {os.path.getsize(dst) // 1024}KB")


if __name__ == "__main__":
    main()
