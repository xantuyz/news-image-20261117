#!/usr/bin/env python3
"""Render the world news of Tuesday 17 November 2026 as a one-page
newspaper front page (1024x1024 PNG).

Pure PIL drawing: flat vector-style illustrations, no text inside the
illustrations, all copy set in DejaVu. Run: python3 render.py
Writes entry.png next to this script.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (163, 51, 39)
GRAY = (107, 101, 92)
LIGHT_RULE = (200, 192, 176)
SEA = (46, 95, 122)
SEA_LIGHT = (120, 165, 185)
SKY = (223, 233, 236)
STEEL = (74, 84, 92)
SMOKE = (150, 150, 146)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

MX = 36                      # side margin
CW = W - 2 * MX              # content width = 952


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap, returns list of lines."""
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, s, f, max_w, leading, color=INK):
    """Draw wrapped paragraph, return y after last line."""
    for line in wrap(draw, s, f, max_w):
        draw.text((x, y), line, font=f, fill=color)
        y += leading
    return y


def fit_font(lines, max_w, size, name="DejaVuSans-Bold.ttf"):
    """Largest bold size <= size whose lines all fit max_w."""
    for s in range(size, 17, -1):
        f = font(name, s)
        if all(d.textlength(ln, font=f) <= max_w for ln in lines):
            return f, s
    return font(name, 18), 18


def hrule(y, color=INK, width=1):
    d.line([(MX, y), (W - MX, y)], fill=color, width=width)


def story_mid(x, y, kick, head_lines, body, art):
    """Two-column middle story: text left (300px), art right (142px)."""
    kicker(x, y, kick, 18)
    hy = y + 28
    for i, line in enumerate(head_lines):
        d.text((x, hy + i * 34), line, font=F_SANS_B(28), fill=INK)
    para(d, x, hy + len(head_lines) * 34 + 6, body, F_SANS(20), 300, 25)
    art(x + 322, y + 28, 142, 162)


def kicker(x, y, s, size=19):
    d.text((x, y), s, font=F_SANS_B(size), fill=RED)


# ---------------------------------------------------------------- masthead
title = "THE WORLD TODAY"
tf = F_SERIF_B(62)
d.text(((W - text_w(d, title, tf)) / 2, 26), title, font=tf, fill=INK)
d.rectangle([MX, 104, W - MX, 108], fill=RED)
d.line([(MX, 114), (W - MX, 114)], fill=INK, width=1)

date = "Tuesday, 17 November 2026"
df = F_SANS_B(32)
d.text(((W - text_w(d, date, df)) / 2, 126), date, font=df, fill=INK)
sub = "Six stories that defined the day"
sf = F_SANS(20)
d.text(((W - text_w(d, sub, sf)) / 2, 164), sub, font=sf, fill=GRAY)
hrule(192)

# ---------------------------------------------------------------- lead story
LY = 206
kicker(MX, LY, "UKRAINE  ·  CONFLICT", 20)
# headline, two lines, left column (width 500)
hy = LY + 30
for i, line in enumerate(["Ukraine strikes", "Kerch Bridge again"]):
    d.text((MX, hy + i * 52), line, font=F_SANS_B(44), fill=INK)
by = hy + 2 * 52 + 8
para(d, MX, by, "A road span collapses in the second straight day of "
     "strikes on the Crimea link \u2014 as Russia hits bridges in Kyiv.",
     F_SANS(21), 500, 27)

# lead illustration: Kerch Bridge over the strait, one span down
BX, BY, BW, BH = 570, LY + 6, 418, 232
d.rectangle([BX, BY, BX + BW, BY + BH], fill=SKY)
d.rectangle([BX, BY + BH - 62, BX + BW, BY + BH], fill=SEA)
# sun / haze
d.ellipse([BX + 330, BY + 14, BX + 366, BY + 50], fill=(240, 224, 178))
# far shore
d.rectangle([BX, BY + BH - 78, BX + BW, BY + BH - 62], fill=(176, 176, 160))
# towers
for tx in (BX + 92, BX + 292):
    d.rectangle([tx, BY + 34, tx + 14, BY + BH - 62], fill=STEEL)
    d.rectangle([tx - 6, BY + 34, tx + 20, BY + 44], fill=STEEL)
# deck: left level, middle span collapsed into the water, right level
deck_y = BY + 96
d.rectangle([BX, deck_y, BX + 150, deck_y + 10], fill=INK)
d.polygon([(BX + 156, deck_y), (BX + 252, deck_y + 62),
           (BX + 252, deck_y + 72), (BX + 156, deck_y + 10)],
          fill=(90, 92, 96))
d.polygon([(BX + 252, deck_y + 62), (BX + 262, deck_y + 66),
           (BX + 262, deck_y + 76), (BX + 252, deck_y + 72)],
          fill=(64, 66, 70))
d.rectangle([BX + 268, deck_y, BX + BW, deck_y + 10], fill=INK)
# cables
for cx in (BX + 60, BX + 110, BX + 310, BX + 360):
    d.line([(cx, BY + 44), (cx, deck_y)], fill=STEEL, width=2)
# smoke over the fallen span
for cx, cy, r in ((BX + 210, BY + 52, 26), (BX + 238, BY + 30, 32),
                  (BX + 268, BY + 54, 22)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
# waves
for wy in (BY + BH - 46, BY + BH - 26, BY + BH - 10):
    for wx in range(BX + 8, BX + BW - 20, 44):
        d.arc([wx, wy, wx + 34, wy + 14], 180, 360, fill=SEA_LIGHT, width=3)
# caption-free frame
d.rectangle([BX, BY, BX + BW, BY + BH], outline=INK, width=2)

hrule(464)

# ---------------------------------------------------------------- stories 2-3
RY = 478
COLW = 464
GAP = 24


def globe(x, y, w, h):
    cx, cy, r = x + w // 2, y + h // 2, 74
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 110, 150))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)
    # meridians (kept inside the disc)
    for k in (0.45, 0.85):
        d.ellipse([cx - int(r * k), cy - r, cx + int(r * k), cy + r],
                  outline=(180, 210, 225), width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(180, 210, 225), width=2)
    # landmass blobs (abstract)
    d.ellipse([cx - 52, cy - 46, cx - 6, cy - 8], fill=(96, 150, 96))
    d.ellipse([cx + 8, cy + 6, cx + 54, cy + 46], fill=(96, 150, 96))
    # small plane
    px, py = cx + 30, cy - 62
    d.polygon([(px, py), (px + 34, py + 8), (px, py + 12)], fill=RED)
    d.polygon([(px + 10, py + 4), (px + 22, py + 14), (px + 16, py + 16)],
              fill=RED)


def tanker(x, y, w, h):
    # sea + sky
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h - 46, x + w, y + h], fill=SEA)
    # hull
    hx, hy = x + 8, y + h - 88
    d.polygon([(hx, hy + 26), (hx + w - 16, hy + 26),
               (hx + w - 34, hy + 52), (hx + 14, hy + 52)], fill=(40, 40, 44))
    d.rectangle([hx + 8, hy, hx + 44, hy + 26], fill=(120, 60, 44))
    d.rectangle([hx + 52, hy + 8, hx + 96, hy + 26], fill=(90, 90, 94))
    # explosion burst on the bow, half-overlapping the hull
    ex, ey = x + w - 30, y + h - 84
    for dx, dy in ((0, -12), (9, -9), (12, 0), (9, 9), (0, 12),
                   (-9, 9), (-12, 0), (-9, -9)):
        d.line([(ex, ey), (ex + dx, ey + dy)], fill=(224, 122, 26), width=4)
    d.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=(240, 180, 60))
    d.ellipse([ex - 14, ey - 26, ex + 2, ey - 10], fill=SMOKE)
    # mines in the water
    for mx, my in ((x + 26, y + h - 22), (x + 96, y + h - 12)):
        d.ellipse([mx - 6, my - 6, mx + 6, my + 6], fill=INK)
        for dx, dy in ((0, -9), (7, -7), (9, 0), (7, 7),
                       (0, 9), (-7, 7), (-9, 0), (-7, -7)):
            d.line([(mx, my), (mx + dx, my + dy)], fill=INK, width=2)
    # waves
    for wx in range(x + 4, x + w - 16, 34):
        d.arc([wx, y + h - 34, wx + 28, y + h - 22], 180, 360,
              fill=SEA_LIGHT, width=3)


story_mid(MX, RY, "ASIA  ·  SUMMIT",
          ["Trump lands in", "Manila for ASEAN", "summit"],
          "Xi\u2013Trump\u2013Putin trilateral set for Thursday in Shenzhen.",
          globe)
story_mid(MX + COLW + GAP, RY, "IRAN  ·  HORMUZ",
          ["Tankers hit mines", "near Hormuz"],
          "Iran fires drones at a US radar site in Bahrain \u2014 the third "
          "strike on US targets there in days.", tanker)

hrule(700)

# ---------------------------------------------------------------- stories 4-6
BY3 = 714
COL3 = 301
GAP3 = 24


def bank(x, y, s=84):
    # pediment + columns, all offsets scaled to s
    k = s / 84.0

    def P(v):
        return int(round(v * k))

    d.polygon([(x, y + P(26)), (x + P(42), y), (x + s, y + P(26))],
              fill=STEEL)
    d.rectangle([x, y + P(26), x + s, y + P(32)], fill=INK)
    for i in range(4):
        cx = x + P(8 + i * 10.67)
        d.rectangle([cx, y + P(34), cx + P(8), y + P(66)], fill=STEEL)
    d.rectangle([x, y + P(66), x + s, y + P(72)], fill=INK)
    d.rectangle([x - P(4), y + P(74), x + s + P(4), y + P(80)], fill=STEEL)


def chip(x, y, s=84):
    c = (34, 120, 74)
    k = s / 84.0

    def P(v):
        return int(round(v * k))

    d.rectangle([x + P(12), y + P(12), x + s - P(12), y + s - P(12)],
                fill=c, outline=INK, width=2)
    d.rectangle([x + P(28), y + P(28), x + s - P(28), y + s - P(28)],
                fill=(120, 190, 150), outline=INK, width=1)
    for i in range(3):
        off = P(22 + i * 20)
        d.line([(x + P(12), y + off), (x, y + off)], fill=INK, width=3)
        d.line([(x + s - P(12), y + off), (x + s, y + off)], fill=INK,
               width=3)
        d.line([(x + off, y + P(12)), (x + off, y)], fill=INK, width=3)
        d.line([(x + off, y + s - P(12)), (x + off, y + s)], fill=INK,
               width=3)


def rocket(x, y, s=84):
    cx = x + s // 2
    k = s / 84.0

    def P(v):
        return int(round(v * k))

    # smoke trail
    for sx, sy, r in ((cx - P(16), y + P(62), P(12)),
                      (cx + P(12), y + P(70), P(14)),
                      (cx - P(2), y + P(76), P(10))):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=SMOKE)
    # body
    d.polygon([(cx, y + P(2)), (cx + P(14), y + P(22)),
               (cx + P(14), y + P(56)), (cx - P(14), y + P(56)),
               (cx - P(14), y + P(22))], fill=(236, 236, 230), outline=INK)
    d.polygon([(cx, y + P(2)), (cx + P(14), y + P(22)),
               (cx - P(14), y + P(22))], fill=RED)
    d.polygon([(cx - P(14), y + P(44)), (cx - P(26), y + P(60)),
               (cx - P(14), y + P(58))], fill=RED)
    d.polygon([(cx + P(14), y + P(44)), (cx + P(26), y + P(60)),
               (cx + P(14), y + P(58))], fill=RED)
    # flame
    d.polygon([(cx - P(8), y + P(56)), (cx + P(8), y + P(56)),
               (cx, y + P(76))], fill=(224, 122, 26))
    # debris dots
    for dx, dy in ((x + P(6), y + P(18)), (x + s - P(8), y + P(30)),
                   (x + P(10), y + P(48))):
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=INK)


def story3(x, y, kick, head_lines, body, art):
    kicker(x, y, kick, 17)
    art(x + COL3 - 48, y - 2, 48)
    hf, hs = fit_font(head_lines, COL3, 25)
    hy = y + 30
    for i, line in enumerate(head_lines):
        d.text((x, hy + i * (hs + 5)), line, font=hf, fill=INK)
    para(d, x, hy + len(head_lines) * (hs + 5) + 4, body, F_SANS(18),
         COL3, 23)


story3(MX, BY3, "WALL STREET  ·  BANKING",
       ["JPMorgan blames", "bug for outage"],
       "Monday's banking outage was a software bug, the bank says \u2014 "
       "not a cyberattack.", bank)
story3(MX + COL3 + GAP3, BY3, "TECH  ·  EARNINGS",
       ["Nvidia reports", "after the close"],
       "First results since Jensen Huang's resignation as chief "
       "executive.", chip)
story3(MX + 2 * (COL3 + GAP3), BY3, "SPACE  ·  LAUNCH",
       ["Vulcan fails;", "40 satellites lost"],
       "ULA's Vulcan fails in flight, destroying 40 Amazon Leo internet "
       "satellites.", rocket)

hrule(892)

# ---------------------------------------------------------------- footer briefs
FY = 904
d.text((MX, FY), "ALSO TODAY", font=F_SANS_B(17), fill=RED)
briefs = [
    "Estonia to close all Russia border crossings from 1 Dec after a "
    "foiled sabotage plot.",
    "Five European governments plan a joint Rwanda returns hub.",
    "Microsoft blames a latent defect for a global outage.",
]
for i, b in enumerate(briefs):
    para(d, MX + i * (COL3 + GAP3), FY + 26, b, F_SANS(16), COL3, 20,
         color=(60, 58, 52))

img.save(OUT, optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
