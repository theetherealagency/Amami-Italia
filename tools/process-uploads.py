#!/usr/bin/env python3
"""Turn photos uploaded in the admin portal into the sizes the site serves.

Run from the repo root:  python3 tools/process-uploads.py

An upload lands in content/uploads/<yyyy>/<mm>/<name>.<jpg|png|webp>. For each
one not processed yet this writes, under src/wp-content/uploads/<yyyy>/<mm>/:

  <name>.jpg / .webp                 the full photo (at most 2400 px wide)
  <name>-<N>w.jpg / .webp            every width the site's pages ask for
  <name>-1200x630.jpg                the share card (Facebook, WhatsApp, Google)

Photos are only resized: no colour grading, no filters, no sharpening. A width
larger than the photo is written at the photo's own size, so every file a page
can ask for exists. Uploaded files keep new names, never overwrite old ones
(uploads are cached by browsers for a year).
"""
import glob
import os

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX = os.path.join(ROOT, 'content', 'uploads')
OUT = os.path.join(ROOT, 'src', 'wp-content', 'uploads')
WIDTHS = (240, 480, 600, 800, 1100, 1200, 1367, 1374, 1600, 2000, 2400)
FULL = 2400


def save(im, path, w):
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(path + '.jpg', 'JPEG', quality=84, optimize=True, progressive=True)
    im.save(path + '.webp', 'WEBP', quality=82, method=6)


def main():
    done = 0
    for src in sorted(glob.glob(os.path.join(INBOX, '**', '*'), recursive=True)):
        if not src.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            continue
        rel = os.path.splitext(os.path.relpath(src, INBOX))[0]
        base = os.path.join(OUT, rel)
        if os.path.exists(base + '.jpg'):
            continue
        os.makedirs(os.path.dirname(base), exist_ok=True)
        im = ImageOps.exif_transpose(Image.open(src))
        if im.mode != 'RGB':
            bg = Image.new('RGB', im.size, (238, 233, 218))     # the site's cream, behind any transparency
            bg.paste(im.convert('RGBA'), mask=im.convert('RGBA').split()[-1])
            im = bg
        for w in WIDTHS:
            save(im, f'{base}-{w}w', w)
        # share card: 1200x630, centred
        ratio = 1200 / 630
        if im.width / im.height > ratio:
            cw = round(im.height * ratio)
            card = im.crop(((im.width - cw) // 2, 0, (im.width - cw) // 2 + cw, im.height))
        else:
            ch = round(im.width / ratio)
            card = im.crop((0, (im.height - ch) // 2, im.width, (im.height - ch) // 2 + ch))
        card.resize((1200, 630), Image.LANCZOS).save(base + '-1200x630.jpg', 'JPEG', quality=84, optimize=True, progressive=True)
        save(im, base, FULL)        # written last: its presence means "done"
        done += 1
        print(f'processed {rel} ({im.width}x{im.height})')
    print(f'process-uploads: {done} new photo(s)')


if __name__ == '__main__':
    main()
