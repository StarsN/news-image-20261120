#!/usr/bin/env python3
"""Build entry.png for news-image-20261120.

A newspaper front page summing up Friday 20 November 2026. Every story
on the page was first reported on that day (verified against wire
reports during the build). All artwork is drawn here with PIL
primitives; no photographs, no downloads, no network at run time.

Run:  python3 compose.py [out.png]
"""
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 227)
INK = (20, 20, 20)
RED = (158, 27, 27)
GREY = (90, 86, 76)
LIGHT_LINE = (180, 172, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SERIF = FONT_DIR + "DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit in `width` px."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, leading, color=INK):
    """Draw a wrapped paragraph; returns the y below the last line."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def star_points(cx, cy, r_out, r_in, rot=-90):
    import math
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        ang = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def vgrad(draw, box, top, bottom):
    """Vertical gradient inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    steps = max(1, y1 - y0)
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[j] + (bottom[j] - top[j]) * t) for j in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


# ---------------------------------------------------------------- art panels

def art_kyiv(draw, box):
    """Night barrage over Kyiv: dark sky, lit skyline, missile trails."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    vgrad(draw, box, (12, 16, 42), (58, 48, 88))
    # fixed stars
    for fx, fy in [(0.08, 0.12), (0.25, 0.27), (0.44, 0.09), (0.63, 0.23),
                   (0.80, 0.11), (0.19, 0.42), (0.55, 0.46), (0.88, 0.35),
                   (0.38, 0.58), (0.73, 0.58)]:
        sx, sy = x0 + fx * w, y0 + fy * h
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(230, 230, 240))
    # missile trails: bright arcs sweeping down (bboxes kept inside the box)
    draw.arc([x0 + 0.05 * w, y0 + 0.02 * h, x0 + 0.72 * w, y0 + 0.72 * h],
             start=200, end=335, fill=(255, 170, 60), width=5)
    draw.arc([x0 + 0.38 * w, y0 + 0.06 * h, x0 + 0.98 * w, y0 + 0.78 * h],
             start=205, end=330, fill=(255, 120, 40), width=4)
    for fx, fy in [(0.69, 0.22), (0.94, 0.24)]:
        gx, gy = x0 + fx * w, y0 + fy * h
        draw.ellipse([gx - 4, gy - 4, gx + 4, gy + 4], fill=(255, 220, 130))
    # smoke plumes above the rooftops
    for fx, fy, frx, fry in [(0.25, 0.50, 0.10, 0.09), (0.63, 0.54, 0.12, 0.10),
                             (0.84, 0.48, 0.08, 0.08)]:
        cx, cy = x0 + fx * w, y0 + fy * h
        draw.ellipse([cx - frx * w, cy - fry * h, cx + frx * w, cy + fry * h],
                     fill=(120, 110, 125))
    # skyline silhouettes with lit windows
    base = y1 - 6
    for fbx, fbw, fbh in [(0, 0.10, 0.30), (0.11, 0.07, 0.42), (0.19, 0.13, 0.25),
                          (0.32, 0.06, 0.37), (0.39, 0.11, 0.27), (0.51, 0.08, 0.45),
                          (0.60, 0.12, 0.31), (0.73, 0.09, 0.38), (0.82, 0.11, 0.25),
                          (0.94, 0.06, 0.34)]:
        bx, bw, bh = fbx * w, fbw * w, fbh * h
        draw.rectangle([x0 + bx, base - bh, x0 + bx + bw, base], fill=(10, 10, 24))
        wy = base - bh + 8
        while wy < base - 8:
            wx = bx + 6
            while wx < bx + bw - 6:
                if (int(wx) * 7 + int(wy) * 3) % 5 == 0:
                    draw.rectangle([x0 + wx, wy, x0 + wx + 4, wy + 5],
                                   fill=(255, 205, 90))
                wx += 14
            wy += 16
    # bridge across the bottom
    draw.rectangle([x0, base - 3, x1, base + 2], fill=(8, 8, 20))
    for fpx in (0.19, 0.53, 0.84):
        px = x0 + fpx * w
        draw.rectangle([px, base - 26, px + 4, base], fill=(8, 8, 20))
    draw.line([(x0 + 0.19 * w, base - 26), (x0 + 0.53 * w, base - 3)],
              fill=(8, 8, 20), width=2)
    draw.line([(x0 + 0.53 * w, base - 26), (x0 + 0.84 * w, base - 3)],
              fill=(8, 8, 20), width=2)


def art_riyadh(draw, box):
    """Riyadh's tallest tower at dusk, windows blown out on eight floors."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    vgrad(draw, box, (24, 30, 66), (214, 130, 70))
    # low sun
    sx, sy, sr = x0 + 0.78 * w, y0 + 0.55 * h, 0.14 * h
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 190, 90))
    # tower: tapered glass slab
    cx = x0 + 0.5 * w
    top_w, bot_w = 0.20 * w, 0.30 * w
    draw.polygon([(cx - top_w / 2, y0 + 3), (cx + top_w / 2, y0 + 3),
                  (cx + bot_w / 2, y1 - 10), (cx - bot_w / 2, y1 - 10)],
                 fill=(52, 74, 110))
    # window grid, widening toward the base
    y = y0 + 10
    while y < y1 - 16:
        t = (y - y0) / h
        half = top_w / 2 + (bot_w - top_w) / 2 * t
        wx = cx - half + 6
        while wx < cx + half - 8:
            draw.rectangle([wx, y, wx + 5, y + 5], fill=(190, 210, 235))
            wx += 11
        y += 9
    # broken band: dark jagged patch across the middle floors
    by0, by1 = y0 + 0.34 * h, y0 + 0.56 * h
    pts = []
    for i, fx in enumerate([-0.13, -0.09, -0.05, -0.01, 0.03, 0.07, 0.11, 0.13]):
        pts.append((cx + fx * w, by0 + (4 if i % 2 == 0 else -2)))
    for i, fx in enumerate([0.13, 0.09, 0.05, 0.01, -0.03, -0.07, -0.11, -0.13]):
        pts.append((cx + fx * w, by1 + (4 if i % 2 == 0 else -2)))
    draw.polygon(pts, fill=(18, 16, 20))
    # neighbouring blocks
    for fbx, fbw, fbh in [(0.02, 0.13, 0.42), (0.17, 0.10, 0.58),
                          (0.72, 0.11, 0.50), (0.85, 0.12, 0.38)]:
        bx, bw, bh = x0 + fbx * w, fbw * w, fbh * h
        draw.rectangle([bx, y1 - 10 - bh, bx + bw, y1 - 10], fill=(30, 34, 54))
        wy = y1 - 10 - bh + 6
        while wy < y1 - 14:
            wx = bx + 5
            while wx < bx + bw - 5:
                if (int(wx) + int(wy)) % 3 == 0:
                    draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 200, 110))
                wx += 10
            wy += 10
    draw.rectangle([x0, y1 - 10, x1, y1], fill=(16, 16, 26))


def art_flags(draw, box):
    """Three flags (US, China, Russia) above a signed document."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    vgrad(draw, box, (238, 232, 214), (222, 212, 186))
    fw, fh = 0.28 * w, 0.52 * h
    gap = 0.025 * w
    total = fw * 3 + gap * 2
    sx = x0 + (w - total) / 2
    fy = y0 + 5
    # --- US flag
    ux = sx
    for i in range(13):
        c = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([ux, fy + i * fh / 13, ux + fw, fy + (i + 1) * fh / 13],
                       fill=c)
    draw.rectangle([ux, fy, ux + fw * 2 / 5, fy + fh * 7 / 13], fill=(60, 59, 110))
    for r in range(4):
        for col in range(5):
            draw.ellipse([ux + 5 + col * 13, fy + 4 + r * 9,
                          ux + 8 + col * 13, fy + 7 + r * 9], fill=(255, 255, 255))
    # --- China flag
    cx0 = sx + fw + gap
    draw.rectangle([cx0, fy, cx0 + fw, fy + fh], fill=(222, 41, 16))
    draw.polygon(star_points(cx0 + 0.20 * fw, fy + 0.27 * fh, 0.11 * fw, 0.045 * fw),
                 fill=(255, 222, 0))
    for sfx, sfy in [(0.48, 0.16), (0.60, 0.27), (0.60, 0.44), (0.48, 0.55)]:
        draw.polygon(star_points(cx0 + sfx * fw, fy + sfy * fh, 0.045 * fw,
                                 0.019 * fw), fill=(255, 222, 0))
    # --- Russia flag
    rx0 = sx + 2 * (fw + gap)
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([rx0, fy + i * fh / 3, rx0 + fw, fy + (i + 1) * fh / 3],
                       fill=c)
    # document below
    dy = fy + fh + 6
    draw.rectangle([sx, dy, sx + total, y1 - 4], fill=(255, 255, 255),
                   outline=(120, 110, 90))
    for i, lw in enumerate([0.82, 0.64, 0.74]):
        ly = dy + 7 + i * 9
        draw.line([(sx + 10, ly), (sx + 10 + total * lw, ly)], fill=(120, 116, 100),
                  width=2)


def art_globe(draw, box):
    """A warming globe beside a rising thermometer."""
    import math
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    vgrad(draw, box, (226, 238, 246), (190, 214, 232))
    cx, cy, r = x0 + 0.40 * w, y0 + 0.48 * h, 0.30 * h
    # sun rays
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        draw.line([(cx + (r + 5) * math.cos(a), cy + (r + 5) * math.sin(a)),
                   (cx + (r + 13) * math.cos(a), cy + (r + 13) * math.sin(a))],
                  fill=(230, 150, 40), width=3)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 110, 190),
                 outline=(30, 70, 140), width=3)
    # continents (green blobs kept inside the circle)
    for fx, fy, frx, fry in [(0.30, 0.36, 0.09, 0.07), (0.50, 0.46, 0.07, 0.11),
                             (0.30, 0.58, 0.08, 0.06), (0.52, 0.60, 0.06, 0.04)]:
        ex, ey = x0 + fx * w, y0 + fy * h
        draw.ellipse([ex - frx * w, ey - fry * h, ex + frx * w, ey + fry * h],
                     fill=(86, 160, 90))
    # thermometer
    tx = x0 + 0.85 * w
    draw.rounded_rectangle([tx - 7, y0 + 0.14 * h, tx + 7, y0 + 0.86 * h], radius=7,
                           fill=(255, 255, 255), outline=(150, 40, 40), width=2)
    draw.rectangle([tx - 3, y0 + 0.42 * h, tx + 3, y0 + 0.84 * h], fill=(200, 40, 40))
    draw.ellipse([tx - 12, y0 + 0.80 * h, tx + 12, y0 + 0.96 * h], fill=(200, 40, 40),
                 outline=(150, 40, 40), width=2)


def art_baseball(draw, box):
    """A baseball diamond with a stitched ball."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    vgrad(draw, box, (214, 232, 200), (150, 190, 130))
    # infield diamond
    cx, cy = x0 + 0.5 * w, y0 + 0.72 * h
    s = 0.30 * h
    draw.polygon([(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)],
                 fill=(196, 164, 120), outline=(120, 90, 60))
    # bases
    for bx, by in [(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)]:
        draw.rectangle([bx - 5, by - 5, bx + 5, by + 5], fill=(255, 255, 255),
                       outline=(90, 90, 90))
    # pitcher's mound
    draw.ellipse([cx - 8, cy - 3, cx + 8, cy + 7], fill=(220, 200, 160))
    # the ball, top right: white with two curved red seams
    bx, by, br = x1 - 0.22 * w, y0 + 0.22 * h, 0.16 * h
    draw.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 255, 255),
                 outline=(180, 60, 60), width=2)
    draw.arc([bx - br + 4, by - br + 6, bx + 8, by + br - 6], start=90, end=270,
             fill=(200, 40, 40), width=3)
    draw.arc([bx - 8, by - br + 6, bx + br - 4, by + br - 6], start=270, end=90,
             fill=(200, 40, 40), width=3)


# ---------------------------------------------------------------- page build

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 30
    rx = W - mx

    # frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)

    # ---- masthead
    f_mast = font(SERIF_B, 58)
    d.text(((W - d.textlength("THE WORLD IN ONE DAY", font=f_mast)) / 2, 24),
           "THE WORLD IN ONE DAY", font=f_mast, fill=INK)
    f_date = font(SANS_B, 21)
    date = "FRIDAY, 20 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 92), date, font=f_date,
           fill=RED)
    f_tag = font(SANS, 14)
    tag = "ONE DAY  ·  ONE PICTURE  ·  ALL THE NEWS THAT MATTERED"
    d.text(((W - d.textlength(tag, font=f_tag)) / 2, 122), tag, font=f_tag,
           fill=GREY)
    rule(d, mx, rx, 146, 3)
    rule(d, mx, rx, 151, 1)

    # ---- lead story: Kyiv
    ly = 166
    f_kick = font(SANS_B, 16)
    d.text((mx, ly), "UKRAINE  —  KYIV UNDER FIRE", font=f_kick, fill=RED)
    f_head = font(SANS_B, 47)
    d.text((mx, ly + 26), "MISSILES RAIN", font=f_head, fill=INK)
    d.text((mx, ly + 76), "ON KYIV", font=f_head, fill=INK)
    f_body = font(SERIF, 18)
    body = ("Russia fired missiles and drones across the capital "
            "overnight, killing three people and wounding nine. "
            "Three bridges were hit, power was cut, and the blasts "
            "damaged the Austrian and Dutch embassies and a cathedral.")
    y = para(d, mx, ly + 138, body, f_body, 462, 25)
    f_note = font(SERIF_I, 15)
    para(d, mx, y + 10, "The daytime barrage blew out windows at two "
         "embassies.", f_note, 462, 21, color=GREY)
    # lead photo
    px0, py0, px1, py1 = 516, 166, 994, 428
    d.rectangle([px0, py0, px1, py1], outline=INK, width=2)
    art_kyiv(d, (px0 + 2, py0 + 2, px1 - 2, py1 - 2))
    f_cap = font(SERIF_I, 14)
    para(d, px0, py1 + 8,
         "A night barrage over Kyiv: missiles streak in as smoke rises "
         "over the skyline.", f_cap, px1 - px0, 19, color=GREY)

    rule(d, mx, rx, 486, 2)

    # ---- row 2: two tiles with art on top
    ty = 500
    tw = 467
    th = 208
    tiles2 = [
        (mx, "RIYADH", "HOUTHI MISSILE HITS RIYADH TOWER",
         "A missile hit the capital's tallest skyscraper, blowing out "
         "windows across eight floors.", art_riyadh),
        (527, "DIPLOMACY", "PEACE DECLARATION, A DAY AFTER THE SUMMIT",
         "Trump, Xi and Putin publish a joint declaration: no nuclear war, "
         "UN reform, more fuel — but no arms cuts.", art_flags),
    ]
    f_tile_k = font(SANS_B, 14)
    f_tile_h = font(SANS_B, 23)
    f_tile_b = font(SERIF, 16)
    for tx, kick, head, body, art in tiles2:
        d.text((tx, ty), kick, font=f_tile_k, fill=RED)
        d.rectangle([tx, ty + 22, tx + tw, ty + 110], outline=INK, width=2)
        art(d, (tx + 2, ty + 24, tx + tw - 2, ty + 108))
        hy = ty + 118
        for line in wrap(d, head, f_tile_h, tw):
            d.text((tx, hy), line, font=f_tile_h, fill=INK)
            hy += 28
        para(d, tx, hy + 2, body, f_tile_b, tw, 20)

    rule(d, mx, rx, 722, 2)

    # ---- row 3: two tiles, art left, text right
    ty3 = 736
    tiles3 = [
        (mx, "CLIMATE", "CLIMATE DEAL DROPS FOSSIL FUELS",
         "The near-final COP31 draft scrubs the fossil-fuel transition as "
         "the talks wrap up.", art_globe),
        (527, "SPORT", "TRUMP PARDONS PETE ROSE",
         "The late baseball great is pardoned posthumously, decades after "
         "his ban from the game.", art_baseball),
    ]
    f_t3_h = font(SANS_B, 22)
    f_t3_b = font(SERIF, 15)
    for tx, kick, head, body, art in tiles3:
        d.text((tx, ty3), kick, font=f_tile_k, fill=RED)
        ax0, ay0 = tx, ty3 + 24
        d.rectangle([ax0, ay0, ax0 + 196, ay0 + 158], outline=INK, width=2)
        art(d, (ax0 + 2, ay0 + 2, ax0 + 194, ay0 + 156))
        bx = tx + 212
        hy = ty3 + 26
        for line in wrap(d, head, f_t3_h, tw - 212):
            d.text((bx, hy), line, font=f_t3_h, fill=INK)
            hy += 26
        para(d, bx, hy + 4, body, f_t3_b, tw - 212, 20)

    rule(d, mx, rx, 934, 2)

    # ---- ticker
    f_tick = font(SANS, 15)
    f_tick_b = font(SANS_B, 15)
    d.text((mx, 946), "ALSO TODAY:", font=f_tick_b, fill=RED)
    tick = ("UK and EU agree a youth-mobility deal  ·  Britain pledges £260m "
            "of drones for Ukraine  ·  Six killed in a gas blast in Georgia  ·  "
            "Trump: no rush on new Iran strikes  ·  Denmark backs a US–Greenland "
            "security deal")
    para(d, mx + 118, 946, tick, f_tick, rx - mx - 118, 20)

    # ---- footer
    f_foot = font(SERIF_I, 13)
    foot = "Every story on this page was first reported on Friday 20 November 2026."
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 994), foot, font=f_foot,
           fill=GREY)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = build()
    img.save(out, format="PNG")
    print(f"wrote {out}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
