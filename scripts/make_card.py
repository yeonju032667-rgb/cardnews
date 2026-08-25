#!/usr/bin/env python3
"""
Generate a 1080x1350 Jubjub-style news card PNG.

Usage:
    python make_card.py --photo PHOTO_PATH --headline "line1\\nline2" --out OUT_PATH [--tag "이슈 브리핑"]

Format matches jubjub_card_final.png: full-bleed photo background with a
bottom gradient, a pink pill tag, a headline anchored near the bottom, and
the Jubjub logo in the top-left corner.
"""
import argparse
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)
FONT_BOLD = os.path.join(REPO_ROOT, "assets", "fonts", "NotoSansKR-Bold.ttf")
LOGO_PATH = os.path.join(REPO_ROOT, "assets", "jubjub_logo.png")

W, H = 1080, 1350
PINK = (255, 105, 158)
NAVY = (31, 33, 56)


def font(size):
    return ImageFont.truetype(FONT_BOLD, size)


def cover_crop(im, target_w, target_h):
    src_w, src_h = im.size
    src_ratio = src_w / src_h
    tgt_ratio = target_w / target_h
    if src_ratio > tgt_ratio:
        new_h = src_h
        new_w = int(src_h * tgt_ratio)
        x0 = (src_w - new_w) // 2
        box = (x0, 0, x0 + new_w, new_h)
    else:
        new_w = src_w
        new_h = int(src_w / tgt_ratio)
        y0 = (src_h - new_h) // 2
        box = (0, y0, new_w, y0 + new_h)
    return im.crop(box).resize((target_w, target_h), Image.LANCZOS)


def gradient_overlay(im, color=NAVY, top_alpha=40, bottom_alpha=245):
    w, h = im.size
    grad = Image.new("L", (1, h))
    for y in range(h):
        a = int(top_alpha + (bottom_alpha - top_alpha) * (y / h))
        grad.putpixel((0, y), a)
    grad = grad.resize((w, h))
    overlay = Image.new("RGBA", (w, h), color + (0,))
    overlay.putalpha(grad)
    return Image.alpha_composite(im.convert("RGBA"), overlay)


def wrap_draw(draw, text, xy, f, fill, max_width, line_spacing=1.3):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for ch in para:
            test = cur + ch
            if draw.textlength(test, font=f) > max_width and cur:
                lines.append(cur)
                cur = ch
            else:
                cur = test
        lines.append(cur)
    x, y = xy
    lh = int(f.size * line_spacing)
    for i, line in enumerate(lines):
        draw.text((x, y + i * lh), line, font=f, fill=fill)
    return y + len(lines) * lh


def make_card(photo_path, headline, out_path, tag="이슈 브리핑"):
    img = Image.new("RGB", (W, H), NAVY)
    photo = Image.open(photo_path).convert("RGB")
    ph = cover_crop(photo, W, H)
    ph = gradient_overlay(ph, color=NAVY, top_alpha=40, bottom_alpha=245)
    img.paste(ph.convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img)

    logo = Image.open(LOGO_PATH).convert("RGBA").resize((120, 120))
    img.paste(logo, (60, 60), logo)

    size = 70
    while size > 40:
        title_f = font(size)
        nlines = 0
        for para in headline.split("\n"):
            cur = ""
            for ch in para:
                test = cur + ch
                if d.textlength(test, font=title_f) > 940 and cur:
                    nlines += 1
                    cur = ch
                else:
                    cur = test
            nlines += 1
        if nlines <= len(headline.split("\n")):
            break
        size -= 4
    title_f = font(size)

    tagf = font(30)
    d.rounded_rectangle([70, H - 500, 70 + 230, H - 500 + 58], radius=29, fill=PINK)
    d.text((100, H - 486), tag, font=tagf, fill=NAVY)

    wrap_draw(d, headline, (70, H - 430), title_f, (255, 255, 255), 940, line_spacing=1.3)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, "PNG")
    print("saved", out_path)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--photo", required=True)
    p.add_argument("--headline", required=True, help="Use \\n for a line break")
    p.add_argument("--out", required=True)
    p.add_argument("--tag", default="이슈 브리핑")
    args = p.parse_args()
    make_card(args.photo, args.headline.replace("\\n", "\n"), args.out, args.tag)
