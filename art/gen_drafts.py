#!/usr/bin/env python3
"""Asset design drafts for 로드킬 프로토콜 with Qwen-Image 2.1 (official weights) via the local ComfyUI.

Reuses ~/tools/qwen-gen/gen.py for the server and workflow, swapping only the diffusion model.

    python gen_drafts.py              # every style x asset
    python gen_drafts.py A cars       # one style, one asset
"""
import os
import shutil
import sys
import time

sys.path.insert(0, os.path.expanduser("~/tools/qwen-gen"))
import gen  # noqa: E402

UNET = "qwen_image_2.1_int8_convrot.safetensors"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "drafts")
SEED = 20261011

SHEET = (
    " Game sprite concept sheet for a top-down car survival game. Bird's-eye view from directly overhead, like a satellite photo: "
    "we see only roofs, hoods and tops, never the sides. Every object is drawn vertically with its front pointing to the top edge "
    "of the image. Draw each object exactly once, evenly spaced in a neat grid on a plain flat light grey background, "
    "clearly separated, no text, no labels, no letters, no UI."
)

STYLES = {
    "A": ("Gritty hand-painted wasteland illustration, Mad Max mood, rusty metal, dust and grime, "
          "warm desaturated palette with hazard-yellow accents, painterly brush texture, strong readable silhouettes."),
    "B": ("Chunky stylized 3D toy render, like die-cast miniature toy cars, soft studio lighting, smooth rounded shapes, "
          "bright saturated colors, clean readable silhouettes, slight bevels."),
    "C": ("Crisp 32-bit pixel art, limited palette, clean 1-pixel dark outlines, hard-edged shading, retro arcade sprite style, "
          "no anti-aliasing blur."),
}

ASSETS = {
    "cars": ("square",
             "Exactly five player vehicles in one row, no other vehicles: a yellow hatchback with two black hood stripes and a small machine-gun turret on the roof; "
             "a red muscle car with two white racing stripes and a rear spoiler; a teal open dune buggy with a roll cage and big tires; "
             "an orange dump truck with a ribbed cargo bed; a long yellow school bus." + SHEET),
    "enemies": ("square",
                "Exactly five figures, seen from above like a top-down shooter: a shambling grey-green zombie; a thin pale fast ghoul with red eyes; "
                "a hulking purple mutant brute with huge shoulders; a zombie with a glowing green acid sac on its back; "
                "and a big rust-red raider pickup truck with a spiked steel plow on the front as the boss." + SHEET),
    "items": ("square",
              "Pickups and props: a wooden supply crate with metal straps; a red explosive oil barrel with a warning mark; "
              "a green repair kit; a horseshoe magnet; a blue nitro canister; a round black bomb; a pile of shiny steel nuts and bolts; "
              "a small landmine with a red light; a spinning circular saw blade; a chrome hubcap." + SHEET),
    "ground": ("square",
               "Seamless tileable ground texture seen from directly above: cracked sun-baked asphalt road with faded yellow dashed "
               "center line and worn white edge lines, blending into dusty desert sand, oil stains and small pebbles. "
               "Flat even lighting, no objects, no vehicles, no text."),
    "key": ("landscape",
            "Key art for a game called Scrap Dash: a yellow hatchback with a roof turret drifting sideways across a cracked desert highway "
            "at dusk, plowing through a horde of zombies, sparks and dust flying, tire smoke, a rusty raider truck with a spiked plow "
            "chasing behind. High three-quarter top-down camera. Dramatic, energetic composition. No text, no logo."),
}


def run(style, asset):
    size, prompt = ASSETS[asset]
    full = f"{prompt} {STYLES[style]}"
    w, h = gen.SIZES[size]
    wf = gen.workflow(full, gen.NEGATIVE + ", text, watermark, logo, perspective view, side view", w, h, SEED, 3.0)
    wf["1"]["inputs"]["unet_name"] = UNET
    t0 = time.time()
    src = gen.generate(wf)
    dst = os.path.join(OUT, f"{style}_{asset}.png")
    shutil.copy2(src, dst)
    print(f"{style}_{asset}: {time.time() - t0:.0f}s -> {dst}", flush=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    gen.ensure_server()
    styles = [sys.argv[1]] if len(sys.argv) > 1 else list(STYLES)
    assets = [sys.argv[2]] if len(sys.argv) > 2 else list(ASSETS)
    for asset in assets:
        for style in styles:
            if os.path.exists(os.path.join(OUT, f"{style}_{asset}.png")) and len(sys.argv) == 1:
                print(f"{style}_{asset}: exists, skipped", flush=True)
                continue
            run(style, asset)


if __name__ == "__main__":
    main()
