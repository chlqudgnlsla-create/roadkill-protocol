#!/usr/bin/env python3
"""Game sprites in art direction A (gritty hand-painted wasteland) with Qwen-Image 2.1.

One object per image, seen straight from above, on flat magenta so the background can be keyed out.

    python gen_sprites.py              # everything not generated yet
    python gen_sprites.py car_hatch    # one sprite (regenerates)
"""
import os
import shutil
import sys
import time

sys.path.insert(0, os.path.expanduser("~/tools/qwen-gen"))
import gen  # noqa: E402

UNET = "qwen_image_2.1_int8_convrot.safetensors"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites", "raw")
SEED = 20261012

STYLE = ("Gritty hand-painted wasteland game art, Mad Max mood, rusty metal, dust and grime, warm desaturated palette "
         "with hazard-yellow accents, painterly brush texture, strong readable silhouette.")
TOP = ("A single game sprite seen from directly overhead (bird's-eye view, like a satellite photo), only the top is visible. "
       "Exactly one object, centered, filling about 70% of the frame, front pointing to the top edge. "
       "Isolated on a perfectly flat solid magenta (#FF00FF) background, no shadow on the background, no ground, "
       "no text, no border, no other objects.")

SPRITES = {
    # vehicles
    "car_hatch":  "A small yellow hatchback with two black racing stripes on the hood and a compact machine-gun turret on the roof.",
    "car_muscle": "A red American muscle car with two white racing stripes running over hood and roof, black rear spoiler, hood scoop.",
    "car_buggy":  "A teal open dune buggy with an exposed tubular roll cage, two seats, rear engine and four large off-road tires.",
    "car_dump":   "An orange dump truck with a short cab at the front and a long ribbed steel cargo bed, six wheels.",
    "car_bus":    "A long yellow school bus roof with black side stripes and two roof hatches.",
    # enemies (heads and shoulders from above)
    "en_swarm":   "A tiny emaciated grey-green zombie seen from above: top of a bald head, hunched shoulders and reaching arms.",
    "en_walker":  "A shambling olive-green zombie in torn clothes seen from above: top of the head, shoulders and arms reaching forward.",
    "en_runner":  "A thin pale fast ghoul seen from above, long limbs stretched forward mid-sprint, glowing red eyes.",
    "en_brute":   "A hulking purple mutant brute seen from above with enormous shoulders and fists, cracked skin.",
    "en_spitter": "A zombie seen from above with a swollen glowing green acid sac bulging on its back.",
    "en_boss":    "A rust-red armored raider pickup truck seen from above, scrap metal in the cargo bed, a huge spiked steel plow on the front.",
    # props and pickups
    "prop_crate":  "A wooden supply crate with metal corner brackets and cross straps, seen from above.",
    "prop_barrel": "A red explosive oil drum seen from above, round lid with a yellow hazard symbol.",
    "prop_mine":   "A small round metal landmine with a glowing red light in the middle, seen from above.",
    "pick_repair": "A green metal repair toolbox with a white cross, seen from above.",
    "pick_magnet": "A red and silver horseshoe magnet, seen from above.",
    "pick_nitro":  "A blue nitro gas canister with a valve, seen from above.",
    "pick_bomb":   "A round black bomb with a short lit fuse, seen from above.",
    "gem_scrap":   "A small pile of shiny steel hex nuts and bolts, seen from above.",
}
GROUND = ("Seamless tileable ground texture seen from directly above: cracked sun-baked dark asphalt with dust, small pebbles, "
          "faint oil stains and tire marks. Even flat lighting, no road markings, no objects, no vehicles, no text. ")


def run(name):
    if name == "ground":
        prompt, neg = GROUND + STYLE, gen.NEGATIVE + ", text, watermark, objects"
    else:
        prompt, neg = f"{SPRITES[name]} {TOP} {STYLE}", gen.NEGATIVE + ", text, watermark, perspective view, side view, multiple objects, shadow"
    wf = gen.workflow(prompt, neg, 1024, 1024, SEED, 3.0)
    wf["1"]["inputs"]["unet_name"] = UNET
    t0 = time.time()
    src = gen.generate(wf)
    dst = os.path.join(OUT, f"{name}.png")
    shutil.copy2(src, dst)
    print(f"{name}: {time.time() - t0:.0f}s -> {dst}", flush=True)


def main():
    os.makedirs(OUT, exist_ok=True)
    gen.ensure_server()
    names = sys.argv[1:] or list(SPRITES) + ["ground"]
    for name in names:
        if len(sys.argv) == 1 and os.path.exists(os.path.join(OUT, f"{name}.png")):
            continue
        run(name)


if __name__ == "__main__":
    main()
