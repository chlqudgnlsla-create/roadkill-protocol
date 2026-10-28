#!/usr/bin/env python3
"""Launcher icons for the Android app from the hatchback sprite (needs Pillow).

Writes an adaptive icon (dark background + car foreground) and legacy square icons for older launchers.
"""
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "app", "src", "main", "res")
CAR = os.path.join(HERE, "..", "assets", "car_hatch.webp")
BG = (23, 25, 28, 255)
HAZARD = (242, 192, 28, 255)
DENS = {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}

car = Image.open(CAR).convert("RGBA").rotate(30, expand=True, resample=Image.BICUBIC)


def stripe(d, size, y0):
    band = max(2, size // 10)
    for x in range(-size, size * 2, band * 2):
        d.polygon([(x, y0), (x + band, y0), (x + band * 2, y0 + band), (x + band, y0 + band)], fill=HAZARD)


for name, k in DENS.items():
    folder = os.path.join(RES, f"mipmap-{name}")
    os.makedirs(folder, exist_ok=True)
    # adaptive foreground: 108dp canvas, art kept inside the central safe zone (~66dp)
    fg_size = int(108 * k)
    fg = Image.new("RGBA", (fg_size, fg_size), (0, 0, 0, 0))
    c = car.copy(); c.thumbnail((int(fg_size * .62), int(fg_size * .62)), Image.LANCZOS)
    fg.alpha_composite(c, ((fg_size - c.width) // 2, (fg_size - c.height) // 2))
    fg.save(os.path.join(folder, "ic_launcher_fg.png"))
    # legacy icon: 48dp square
    s = int(48 * k)
    im = Image.new("RGBA", (s, s), BG)
    stripe(ImageDraw.Draw(im), s, s - max(2, s // 10))
    c = car.copy(); c.thumbnail((int(s * .84), int(s * .84)), Image.LANCZOS)
    im.alpha_composite(c, ((s - c.width) // 2, (s - c.height) // 2 - s // 20))
    im.convert("RGB").save(os.path.join(folder, "ic_launcher.png"))

anydpi = os.path.join(RES, "mipmap-anydpi-v26")
os.makedirs(anydpi, exist_ok=True)
open(os.path.join(anydpi, "ic_launcher.xml"), "w").write("""<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/asphalt" />
    <foreground android:drawable="@mipmap/ic_launcher_fg" />
</adaptive-icon>
""")
print("icons written to", RES)
