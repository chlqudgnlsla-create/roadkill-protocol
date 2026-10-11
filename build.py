#!/usr/bin/env python3
"""Build a standalone static site in dist/ from index.html (which is authored as a Claude artifact body).

Adds the document shell the artifact viewer normally provides, a web app manifest and icons
so phones can add it to the home screen, and copies assets/.
    python3 build.py
Then serve dist/ with any static host (GitHub Pages, nginx, `python3 -m http.server -d dist`).
"""
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")

src = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
cut = src.index("</style>") + len("</style>")
head, body = src[:cut], src[cut:]
# the artifact file carries its own viewport meta; the shell below provides it instead
head = head.replace('<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n', "")

page = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, user-scalable=no">
<meta name="theme-color" content="#17191c">
<meta name="description" content="차량이 주인공인 뱀서류 생존 게임. 좀비 대군을 들이받고 무기 시너지로 쓸어버리세요.">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icons/icon-192.png">
<link rel="apple-touch-icon" href="icons/icon-192.png">
{head}
</head>
<body>
{body.strip()}
</body>
</html>
"""

if os.path.exists(DIST):
    shutil.rmtree(DIST)
os.makedirs(os.path.join(DIST, "icons"))
open(os.path.join(DIST, "index.html"), "w", encoding="utf-8").write(page)
shutil.copytree(os.path.join(HERE, "assets"), os.path.join(DIST, "assets"))

# icons: the hatchback sprite on the game's asphalt with a hazard-yellow stripe
try:
    from PIL import Image, ImageDraw
    car = Image.open(os.path.join(HERE, "assets", "car_hatch.webp")).convert("RGBA")
    for size in (192, 512):
        im = Image.new("RGBA", (size, size), (23, 25, 28, 255))
        d = ImageDraw.Draw(im)
        band = size // 10
        for x in range(-size, size * 2, band * 2):
            d.polygon([(x, size - band), (x + band, size - band), (x + band * 2, size), (x + band, size)], fill=(242, 192, 28, 255))
        c = car.rotate(30, expand=True, resample=Image.BICUBIC)
        c.thumbnail((int(size * .82), int(size * .82)), Image.LANCZOS)
        im.alpha_composite(c, ((size - c.width) // 2, (size - c.height) // 2 - band // 2))
        im.convert("RGB").save(os.path.join(DIST, "icons", f"icon-{size}.png"))
except ImportError:
    print("Pillow not found: skipped icons (run with the comfyui env python to generate them)")

manifest = {
    "name": "로드킬 프로토콜",
    "short_name": "로드킬",
    "lang": "ko",
    "start_url": "./",
    "scope": "./",
    "display": "fullscreen",
    "orientation": "any",
    "background_color": "#17191c",
    "theme_color": "#17191c",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
    ],
}
open(os.path.join(DIST, "manifest.webmanifest"), "w", encoding="utf-8").write(json.dumps(manifest, ensure_ascii=False, indent=2))
# GitHub Pages: serve files as-is
open(os.path.join(DIST, ".nojekyll"), "w").close()
print("built", DIST, sorted(os.listdir(DIST)))
