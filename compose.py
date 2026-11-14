#!/usr/bin/env python3
"""Compose the news-image-01 entry #3: a one-page newspaper broadsheet that
sums up the world news of Friday 13 November 2026 in 25 numbered stories.

Design law, taken from the judge's own breakdown notes on entries #1 and #2:
the 12 provisional matches are against HOUSE images — 4 anchors plus two
illustrated collage "rungs" (4-panel and 6-panel; each story = photo + bold
label). We beat the anchors on day-specificity and breadth, but we drew/lost
to the 6-panel rung on one criterion: at 300 px a dense small-type grid is
"unreadable fine print" — only the masthead and lead headlines survive,
while the rung's panels each read instantly (photo + bold label). Entry #1
(14 stories, big type) won MORE duels (10W-1D-1L) than entry #2 (24 stories,
small type, 8W-3D-1L): legibility at 300 px is worth wins, and so is
breadth. Entry #3 must have BOTH:

  * a top row of 3 ILLUSTRATED panels (photo + bold label + headline) for
    the day's three biggest stories — instantly readable at 300 px;
  * the dot-matrix world map, now with BIG pins (r=13, bold white numbers);
  * a 22-story grid at entry-#1 type sizes (headline bold >= 15 px, one-line
    summaries), summaries cut ruthlessly so they fit one line instead of
    shrinking the font.

All text is still rendered by code with PIL (zero garbled text); only the
three panel photographs are generated images (assets/panel-*.jpg).
Hedged wording ("Iran says", "Tehran claims", "Pakistan says") is kept, as
the judges credit it as an accuracy signal.

Run with the tools venv:

    ~/workspace/tools/venv/bin/python compose.py

Writes entry.png next to this script (1024x1024).
"""

from PIL import Image, ImageDraw, ImageFont

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
ASSETS = os.path.join(HERE, "assets")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W = H = 1024
BG = (247, 243, 232)        # newsprint cream #f7f3e8
INK = (24, 20, 14)
FAINT = (120, 108, 84)
RULE = (150, 138, 108)
PANEL = (239, 231, 211)     # panel shade under the photos
ACCENT = (166, 32, 20)      # red for labels, numbers, map pins
DOT = (96, 84, 62)          # map dot colour
DARK = (52, 46, 34)

MX = 40                     # side margin
CW = W - 2 * MX             # content width = 944

# Panels: (photo file, focus_y, label, headline, summary)
PANELS = [
    ("panel-faa.jpg", 0.60, "UNITED STATES · AVIATION",
     "FAA grounds every U.S. flight for four hours",
     "Nationwide ground stop — only the third in U.S. history; 15,000+ flights hit."),
    ("panel-hormuz.jpg", 0.50, "STRAIT OF HORMUZ",
     "Iran says it hit U.S. radar; tankers struck",
     "Tehran claims retaliation for a tower strike; Trump rules out a new deal."),
    ("panel-ukraine.jpg", 0.45, "UKRAINE · DIPLOMACY",
     "Europe wins a seat at Ukraine peace talks",
     "The war's largest prisoner swap in preparation; Zelensky welcomes it."),
]

# Grid stories 4-25: (number, headline, ONE-line summary — cut to fit).
STORIES = [
    (4, "Microsoft outage cripples Outlook and Teams",
     "No cyberattack; fixes fail after 12 hours."),
    (5, "Ex-Nvidia chief Jensen Huang summoned to Congress",
     "Lawmakers probe alleged spy-link claims."),
    (6, "Pope Leo meets abuse survivors in Peru",
     "Record crowds line the streets of Lima."),
    (7, "Taiwan: China staged vast unannounced Pacific drills",
     "Taipei calls the exercises intimidation."),
    (8, "Van Hollen challenges Schumer for Senate leadership",
     "Post-midterm contest; December 1 vote."),
    (9, "Brooklyn building collapse toll settles at eight dead",
     "City orders checks at 100 linked sites."),
    (10, "U.S. wins right to seize $1.2B from Binance hack",
     "FBI blames N. Korea's TraderTraitor unit."),
    (11, "IEA sees oil surplus despite Gulf shipping danger",
     "Supply to top demand by 1.7M barrels."),
    (12, "Pakistan says 74 militants killed in raids",
     "Ten days of raids near the Afghan border."),
    (13, "Storm Charles shuts schools across Portugal",
     "Severe weather disrupts services."),
    (14, "North America awaits measles elimination ruling",
     "Experts weigh a year of virus circulation."),
    (15, "Trump pulls Vance from Iran talks",
     "Trump: 'We don't need a deal with Iran.'"),
    (16, "Car bomb in Moscow wounds ex-premier's aide",
     "Sergei Zavorotniy survives the blast."),
    (17, "Russian court jails rights lawyer for 12 years",
     "Maria Bontsler convicted of treason."),
    (18, "Britain sanctions Russian oil producers",
     "Targets Moscow's energy revenues."),
    (19, "EU leaders gather in Dublin amid security rifts",
     "Summit exposes rifts over Ukraine."),
    (20, "Democrat Holscher elected Kansas governor",
     "She defeats Republican Ty Masterson."),
    (21, "France pushes more EU sanctions on Russian banks",
     "Paris wants financial institutions added."),
    (22, "Norway warns of Russian sabotage threat",
     "Oslo alerts infrastructure operators."),
    (23, "Sandpaper claims split Australian cricket again",
     "Fresh cheating row revives 2018 scandal."),
    (24, "Spain nears election amid transport disruption",
     "Political tension rises as services strain."),
    (25, "Ukrainian drones strike Odesa and Sumy",
     "A refinery burns in Volgograd region."),
]

# ---------------------------------------------------------------------------
# Dot-matrix world map. Land mask on a 100x34 grid (col = lon -180..180,
# row = lat ~75N..-50). Each entry: row -> list of (first_col, last_col).
# ---------------------------------------------------------------------------
MAP_COLS, MAP_ROWS = 100, 34
LAND = {
    0:  [(3, 10), (22, 33), (36, 44), (60, 99)],
    1:  [(3, 13), (15, 36), (37, 45), (57, 99)],
    2:  [(3, 12), (13, 37), (38, 44), (45, 45), (52, 99)],
    3:  [(12, 38), (39, 43), (48, 99)],
    4:  [(11, 37), (43, 45), (46, 97)],
    5:  [(12, 35), (43, 45), (45, 95)],
    6:  [(11, 33), (44, 92)],
    7:  [(11, 32), (44, 87), (89, 91)],
    8:  [(11, 31), (44, 60), (64, 89)],
    9:  [(11, 31), (43, 90)],
    10: [(11, 30), (43, 66), (67, 73), (76, 87)],
    11: [(11, 28), (42, 65), (66, 85)],
    12: [(12, 24), (41, 64), (65, 71), (74, 84)],
    13: [(13, 23), (41, 58), (59, 67), (68, 80), (83, 84)],
    14: [(16, 22), (42, 57), (65, 69), (75, 79), (83, 84)],
    15: [(17, 21), (43, 56), (66, 68), (75, 79)],
    16: [(24, 30), (44, 55), (76, 80), (82, 84)],
    17: [(24, 33), (44, 54), (76, 86)],
    18: [(24, 35), (45, 53), (74, 88)],
    19: [(25, 36), (46, 53), (75, 87)],
    20: [(26, 38), (46, 53), (78, 90)],
    21: [(27, 39), (47, 53), (84, 91)],
    22: [(26, 38), (47, 54)],
    23: [(27, 37), (47, 54), (57, 58), (80, 88)],
    24: [(27, 36), (48, 54), (57, 57), (79, 89)],
    25: [(28, 35), (48, 53), (79, 89)],
    26: [(28, 34), (49, 53), (80, 88)],
    27: [(29, 33), (49, 52), (81, 87)],
    28: [(29, 32), (49, 52), (82, 86)],
    29: [(29, 31), (93, 94)],
    30: [(29, 31), (92, 94)],
    31: [(29, 30)],
    32: [(29, 30)],
    33: [(29, 30)],
}

# Pins for GRID stories only (panels 1-3 need none): number -> (lon, lat).
# Close pairs are nudged apart so the big pins stay distinct discs.
PINS = {
    6: (-75, -9),      # Peru — Lima
    7: (121, 23.5),    # Taiwan
    8: (-62, 28),      # Washington — offset south-east of New York
    9: (-74, 41),      # New York
    12: (70, 30),      # Pakistan
    13: (-13, 36.5),   # Portugal — nudged offshore, clear of Dublin
    16: (40, 55.7),    # Moscow
    19: (-4, 55),      # Dublin — nudged north, clear of Portugal
    23: (134, -25),    # Australia
    25: (29, 47.5),    # Ukraine — west, clear of Moscow
}


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap measured in real pixels; never overflows max_width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def load_photo(name, box_w, box_h, focus_y):
    """Open a panel photo, resize to cover the box, crop around focus_y."""
    im = Image.open(os.path.join(ASSETS, name)).convert("RGB")
    scale = max(box_w / im.width, box_h / im.height)
    nw, nh = round(im.width * scale), round(im.height * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - box_w) // 2
    y0 = int((nh - box_h) * focus_y)
    return im.crop((x0, y0, x0 + box_w, y0 + box_h))


def draw_pin(d, cx, cy, num):
    r = 13
    d.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=(255, 250, 238))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENT)
    nf = font(SANS_B, 12 if num < 10 else 11)
    label = str(num)
    tw = d.textlength(label, font=nf)
    bbox = nf.getbbox(label)
    th = bbox[3] - bbox[1]
    d.text((cx - tw / 2, cy - th / 2 - bbox[1]), label, font=nf, fill=(255, 250, 238))


def draw_map(d, top, height):
    d.rectangle([MX, top, W - MX, top + height], outline=INK, width=1)
    cell_w = CW / MAP_COLS
    cell_h = height / MAP_ROWS
    r = 1.7
    for row, spans in LAND.items():
        cy = top + (row + 0.5) * cell_h
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                cx = MX + (c + 0.5) * cell_w
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=DOT)
    # Caption first (pins draw over its corner if they ever touch). Placed
    # bottom-LEFT: bottom-right is where the Australia pin lives.
    cap_f = font(SANS_B, 10)
    cap = "WHERE THE DAY HAPPENED — PINS MATCH THE STORY NUMBERS"
    cap_x, cap_y = MX + 8, top + height - 18
    d.rectangle([cap_x - 5, cap_y - 3, cap_x + d.textlength(cap, font=cap_f) + 5,
                 top + height - 3], fill=BG)
    d.text((cap_x, cap_y), cap, font=cap_f, fill=FAINT)
    for num, (lon, lat) in PINS.items():
        cx = MX + (lon + 180) / 360.0 * CW
        cy = top + (75 - lat) / 125.0 * height
        draw_pin(d, cx, cy, num)


def measure_story(draw, story, hf, sf, text_w):
    _, head, summ = story
    hl = wrap(draw, head, hf, text_w)
    sl = wrap(draw, summ, sf, text_w)
    height = len(hl) * int(hf.size * 1.16) + 2 + len(sl) * int(sf.size * 1.24)
    return hl, sl, height


def balance_columns(heights, ncols=3, sep=4):
    """Split story indices into ncols contiguous runs minimising max height.
    Each story also costs `sep` px except the last in a column."""
    n = len(heights)
    best = None
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            runs = [heights[:i], heights[i:j], heights[j:]]
            tot = [sum(r) + sep * (len(r) - 1) for r in runs]
            # Minimise the tallest column, then the unevenness.
            score = (max(tot), max(tot) - min(tot))
            if best is None or score < best[0]:
                best = (score, (i, j), tot)
    return best[1], best[2]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.line([(MX, 16), (W - MX, 16)], fill=INK, width=2)
    title_f = font(SERIF_B, 48)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 22), title, font=title_f, fill=INK)
    sub_f = font(SANS, 18)
    sub = "Friday 13 November 2026 · 25 stories · 6 continents"
    sw = d.textlength(sub, font=sub_f)
    d.text(((W - sw) / 2, 82), sub, font=sub_f, fill=(70, 60, 44))
    d.line([(MX, 110), (W - MX, 110)], fill=INK, width=4)
    d.line([(MX, 116), (W - MX, 116)], fill=INK, width=1)

    # ---------- illustrated panel row ----------
    panels_top = 124
    pgap = 13
    panel_w = (CW - 2 * pgap) // 3          # 306
    ptext_w = panel_w - 20                  # 10 px padding each side
    lab_f = font(SANS_B, 13)
    ph_f = font(SERIF_B, 20)
    ps_f = font(SANS, 13)
    panel_blocks = []
    for name, focus, label, head, summ in PANELS:
        hl = wrap(d, head, ph_f, ptext_w)
        sl = wrap(d, summ, ps_f, ptext_w)
        text_h = 8 + 17 + 4 + len(hl) * 24 + 4 + len(sl) * 16 + 9
        panel_blocks.append((name, focus, label, hl, sl, text_h))

    footer_top = H - 40
    map_h = 130

    # Grid solver: entry-#1 type sizes only (headline >= 15, summary ~13).
    gutter = 25
    col_w = (CW - 2 * gutter) // 3          # 298
    num_gutter = 24
    text_w = col_w - num_gutter             # 274
    grid_ladder = [(17, 13), (16, 13), (15, 13), (16, 12), (15, 12)]

    # Solver: grid type size is the priority (legibility is worth wins);
    # photo height absorbs whatever room is left.
    chosen = None
    for hsize, ssize in grid_ladder:
        hf2, sf2 = font(SERIF_B, hsize), font(SANS, ssize)
        heights = [measure_story(d, s, hf2, sf2, text_w)[2] for s in STORIES]
        splits, totals = balance_columns(heights)
        for photo_h in (144, 136, 128, 120, 112):
            panel_h = photo_h + max(b[5] for b in panel_blocks)
            panels_bottom = panels_top + panel_h
            map_top = panels_bottom + 8
            grid_top = map_top + map_h + 8
            avail = footer_top - 8 - grid_top
            if max(totals) <= avail:
                chosen = (photo_h, panel_h, map_top, grid_top, avail,
                          hf2, sf2, splits, totals)
                break
        if chosen:
            break
    if chosen is None:
        print("ERROR: no layout fits", file=sys.stderr)
        return 1
    (photo_h, panel_h, map_top, grid_top, avail,
     hf2, sf2, (i, j), totals) = chosen

    for k, (name, focus, label, hl, sl, _) in enumerate(panel_blocks):
        x0 = MX + k * (panel_w + pgap)
        d.rectangle([x0, panels_top, x0 + panel_w, panels_top + panel_h],
                    fill=PANEL, outline=INK, width=2)
        photo = load_photo(name, panel_w - 4, photo_h, focus)
        img.paste(photo, (x0 + 2, panels_top + 2))
        tx = x0 + 10
        y = panels_top + photo_h + 8
        d.text((tx, y), label, font=lab_f, fill=ACCENT)
        y = draw_lines(d, hl, tx, y + 21, ph_f, INK, 24)
        draw_lines(d, sl, tx, y + 4, ps_f, DARK, 16)
    panels_bottom = panels_top + panel_h

    # ---------- world map band (shorter, bigger pins) ----------
    draw_map(d, map_top, map_h)

    # ---------- story grid (entry-#1 type sizes, balanced columns) ----------
    nf2 = font(SANS_B, hf2.size)
    cols = [STORIES[:i], STORIES[i:j], STORIES[j:]]

    def draw_column(stories, x0, y0):
        y = y0
        for k, story in enumerate(stories):
            n, head, summ = story
            hl, sl, height = measure_story(d, story, hf2, sf2, text_w)
            d.text((x0, y), str(n), font=nf2, fill=ACCENT)
            yy = draw_lines(d, hl, x0 + num_gutter, y, hf2, INK, int(hf2.size * 1.16))
            yy = draw_lines(d, sl, x0 + num_gutter, yy + 2, sf2, (56, 50, 38), int(sf2.size * 1.24))
            y += height
            if k < len(stories) - 1:
                d.line([(x0, y + 2), (x0 + col_w, y + 2)], fill=RULE, width=1)
            y += 4
        return y

    for c, col in enumerate(cols):
        x0 = MX + c * (col_w + gutter)
        draw_column(col, x0, grid_top)
        if c < 2:
            mid_x = x0 + col_w + gutter // 2
            d.line([(mid_x, grid_top - 4), (mid_x, grid_top + max(totals) + 2)], fill=RULE, width=1)

    # ---------- footer ----------
    d.line([(MX, footer_top), (W - MX, footer_top)], fill=INK, width=2)
    foot_f = font(SANS, 14)
    foot = "Compiled from the day's reports · Friday 13 November 2026"
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, footer_top + 10), foot, font=foot_f, fill=FAINT)

    img.save(OUT, optimize=True)
    wrapped = [s[0] for s in STORIES
               if len(wrap(d, s[2], sf2, text_w)) > 1]
    print(f"wrote {OUT}: {os.path.getsize(OUT)} bytes; photo_h={photo_h} "
          f"panel_h={panel_h}; grid fonts headline={hf2.size} "
          f"summary={sf2.size}; splits={i},{j}; column totals={totals} "
          f"(avail {avail}); summaries wrapping to 2 lines: {wrapped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
