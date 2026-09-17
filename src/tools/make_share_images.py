"""Build 1200x630 share images for Open Graph / Twitter cards.

Every photograph in the library is portrait, which is the wrong shape for a
link preview: Facebook, Instagram DMs, WhatsApp and the ad platforms all crop a
portrait to a wide card and usually cut the subject in half. So the wide crops
are made here, once, and committed — the pages point at these rather than at
the originals.

Run: python3 tools/make_share_images.py
"""
import pathlib
import sys

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from media_map import MEDIA  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "_assets" / "share"
W, H = 1200, 630

# slot -> where the crop window sits vertically, 0 = top, 1 = bottom.
# Set per photograph so the subject survives the crop.
SLOTS = {
    "room_wide": .34, "room_evening": .30, "room_lounge": .30, "room_private": .48,
    "room_bar": .34, "room_booths": .34, "table_setting": .40,
    "pasta_finish": .56, "pasta_truffle": .46, "dish_dark": .52, "chef_plate": .26,
    "cocktail_smoke": .34, "wine_pour": .38, "wine_table": .42, "server_wine": .34,
    "pizza": .50, "chef_kitchen": .30,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for slot, focus in SLOTS.items():
        src = ROOT / MEDIA[slot][0].lstrip("/")
        if not src.exists():
            print("  missing", src)
            continue
        im = Image.open(src).convert("RGB")
        # widest possible window at 1200:630, positioned by the slot's focus
        cw = im.width
        ch = round(cw * H / W)
        if ch > im.height:
            ch = im.height
            cw = round(ch * W / H)
        left = (im.width - cw) // 2
        top = round((im.height - ch) * focus)
        im = im.crop((left, top, left + cw, top + ch)).resize((W, H), Image.LANCZOS)
        dest = OUT / f"{slot}.jpg"
        im.save(dest, "JPEG", quality=82, optimize=True, progressive=True)
        print(f"  {slot:16} -> {dest.relative_to(ROOT)}  {dest.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
