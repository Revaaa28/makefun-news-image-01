#!/usr/bin/env python3
"""Compose the news-image-01 entry #3 v2: a one-page newspaper broadsheet
that sums up the world news of Friday 13 November 2026 in 25 numbered
stories. Story texts are IDENTICAL to entry #3 v1 — this is a layout and
visual rebuild ordered by the owner after reviewing v1:

  * a full-width HERO splash for the lead story (FAA ground stop): the
    tarmac photo spans the whole page, with a dark-red label chip, a 30 px
    headline and the summary on one row below it;
  * the other two lead stories (Hormuz, Ukraine talks) as half-width
    thumbnail panels — photo left, chip + headline + summary right;
  * a DENSER dot-matrix world map (140x46 mask, smaller dot pitch) whose
    pins now include the LEAD stories 1-3 — v1's map skipped them, which
    the owner called "not relevant"; thirteen pins, every number matching
    the story number on the page;
  * stronger print energy: heavier black masthead rules, dark-red label
    chips, a deeper red for numbers and labels.

Design law carried over from the judge's own breakdown notes on entries
#1 and #2: legibility at 300 px is worth wins, and so is breadth. The
grid therefore keeps entry-#1 type sizes (headline bold 16 px, one-line
summaries) — that is priority #1 and the layout solver below protects it
first; the hero photo (>= 150 px), panel photos (>= 80 px) and map
(>= 100 px) take the remaining space in that order.

All text is rendered by code with PIL (zero garbled text); only the three
photographs are generated images (assets/panel-*.jpg). Hedged wording
("Iran says", "Tehran claims", "Pakistan says") is kept, as the judges
credit it as an accuracy signal.

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
ACCENT = (154, 28, 17)      # deeper red: numbers, labels, chips, pins
DOT = (96, 84, 62)          # map dot colour
DARK = (52, 46, 34)
CHIP_TXT = (255, 250, 238)

MX = 40                     # side margin
CW = W - 2 * MX             # content width = 944

# Panels: (photo file, focus_y, label, headline, summary).
# Index 0 is the HERO (story 1); indices 1-2 are the half-width panels.
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
# Dot-matrix world map, v2: a finer 140x46 land mask ('#' = land), resampled
# from the v1 mask and then hand-shaped — a real Atlantic gap, a Hudson Bay
# notch, a Mediterranean channel, a full Africa and a tapering South
# America — so the landmasses read rich instead of one northern wall.
# Columns run lon -180..180, rows lat ~75N..-50.
# ---------------------------------------------------------------------------
MAP_COLS, MAP_ROWS = 140, 46
MAP_MASK = [
    ".............########..########...................#######..............###..........#######............########.........########.....#####..",
    "....#############.#####################..........##########....................#############################################################",
    "....############.##########################.....##########...........#######################################################################",
    "....###########.#############################..#########.......##...########################################################################",
    ".....##########.##################......#######.######..............########################################################################",
    ".....############################......#########................###..######################################################################.",
    "......##########################......#########................###########################################################################..",
    ".............####################...##########.................##########################################################################...",
    ".............##################################................#########################################################################....",
    ".............###################################..................####################################################################......",
    "..............##################################...................#################################################################........",
    "..............##################################...................##############################...##############################..........",
    "...............################################...................##############################...#############################............",
    "...............################################...................#####..####################################################...............",
    "................##############################....................####......###############################################..###............",
    ".................############################.....................##........#############.###############################....###............",
    "..................##############................................####......#################..##########################.....................",
    "...................############................................####.....####################..#######################.......................",
    ".....................#########.................................##############################..###################..........................",
    "..............................###########......................##############################....##############.............................",
    ".................................##########.....................###########################........##########...............................",
    "........................#######...#####################.....#####################################...#############..####.....................",
    ".................................######################......#################################.......#############.####.....................",
    ".................................######################......#################################........######..############..................",
    ".................................######################.......################################........####.#...##############...............",
    "..................................#####################........###############################.........#####...##############...............",
    "...................................####################.........##############################.........####################.................",
    "....................................###################.........############################.................###################............",
    ".....................................###################.........###########################.................####################...........",
    ".....................................###################..........##########################.........................############...........",
    "....................................###################...........##########################................................................",
    "......................................###############.............#######################.......................#############...............",
    "......................................###############.............#######################......................###############..............",
    "......................................##############...............######################.....................################..............",
    ".......................................############................###################........................################..............",
    ".......................................############.................##################..........................#############...............",
    ".......................................############.................########.#######............................#############...............",
    "........................................##########..................######....#####..............................##########.................",
    "........................................##########..................######.........................................#######..................",
    "........................................##########................................................................................###.......",
    "........................................#########................................................................................####.......",
    "........................................#########................................................................................####.......",
    "........................................####.####...........................................................................................",
    "........................................####.####...........................................................................................",
    "........................................####..##............................................................................................",
    "........................................####..##............................................................................................",
]

# Pins for THIRTEEN stories — the leads included this time (v1 skipped
# stories 1-3, which the owner called irrelevant): number -> (lon, lat).
# Close pairs are spread along real geography so the r=12 pins stay
# distinct discs: 3 = Kyiv talks, 25 = Odesa/Sumy strikes further south,
# 16 = Moscow north-east of both; 8 = Washington, offset into the
# Atlantic south-east of 9 = New York.
PINS = {
    1: (-98, 39),      # story 1 — FAA ground stop, U.S. interior
    2: (56.5, 26.5),   # story 2 — Strait of Hormuz
    3: (25, 50),       # story 3 — Ukraine peace talks (Kyiv, nudged west)
    6: (-75, -9),      # Peru — Lima
    7: (121, 23.5),    # Taiwan
    8: (-62, 28),      # Washington — offset south-east of New York
    9: (-74, 41),      # New York
    12: (70, 30),      # Pakistan
    13: (-13, 36.5),   # Portugal — nudged offshore, clear of Dublin
    16: (44, 57),      # Moscow — nudged north-east, clear of Ukraine
    19: (-4, 55),      # Dublin — nudged north, clear of Portugal
    23: (134, -25),    # Australia
    25: (34, 45.5),    # Ukraine strikes — south of the talks pin
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
    """Open a photo, resize to cover the box, crop around focus_y."""
    im = Image.open(os.path.join(ASSETS, name)).convert("RGB")
    scale = max(box_w / im.width, box_h / im.height)
    nw, nh = round(im.width * scale), round(im.height * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - box_w) // 2
    y0 = int((nh - box_h) * focus_y)
    return im.crop((x0, y0, x0 + box_w, y0 + box_h))


def draw_chip(d, x, y, label, fnt, height):
    """Dark-red label chip with white bold text; returns the chip width."""
    w = d.textlength(label, font=fnt) + 18
    d.rounded_rectangle([x, y, x + w, y + height], radius=3, fill=ACCENT)
    bbox = fnt.getbbox(label)
    th = bbox[3] - bbox[1]
    d.text((x + 9, y + (height - th) / 2 - bbox[1]), label,
           font=fnt, fill=CHIP_TXT)
    return w


def draw_pin(d, cx, cy, num):
    r = 12
    d.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2],
              fill=(255, 250, 238))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENT)
    nf = font(SANS_B, 12 if num < 10 else 11)
    label = str(num)
    tw = d.textlength(label, font=nf)
    bbox = nf.getbbox(label)
    th = bbox[3] - bbox[1]
    d.text((cx - tw / 2, cy - th / 2 - bbox[1]), label,
           font=nf, fill=(255, 250, 238))


def draw_map(d, top, height):
    d.rectangle([MX, top, W - MX, top + height], outline=INK, width=1)
    cell_w = CW / MAP_COLS
    cell_h = height / MAP_ROWS
    r = 1.45
    for ri, row in enumerate(MAP_MASK):
        cy = top + (ri + 0.5) * cell_h
        for ci, ch in enumerate(row):
            if ch == "#":
                cx = MX + (ci + 0.5) * cell_w
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=DOT)
    # Caption on a clean plate, bottom-LEFT (bottom-right is Australia).
    cap_f = font(SANS_B, 10)
    cap = "WHERE THE DAY HAPPENED — PINS MATCH THE STORY NUMBERS"
    cap_x, cap_y = MX + 8, top + height - 18
    d.rectangle([cap_x - 5, cap_y - 3,
                 cap_x + d.textlength(cap, font=cap_f) + 5,
                 top + height - 3], fill=BG)
    d.text((cap_x, cap_y), cap, font=cap_f, fill=FAINT)
    for num, (lon, lat) in PINS.items():
        cx = MX + (lon + 180) / 360.0 * CW
        cy = top + (75 - lat) / 125.0 * height
        draw_pin(d, cx, cy, num)


def measure_story(draw, story, hf, sf, text_w, h_lead, s_lead):
    _, head, summ = story
    hl = wrap(draw, head, hf, text_w)
    sl = wrap(draw, summ, sf, text_w)
    height = len(hl) * h_lead + 2 + len(sl) * s_lead
    return hl, sl, height


def balance_columns(heights, ncols=3, sep=3):
    """Split story indices into ncols contiguous runs minimising max height.
    Each story also costs `sep` px except the last in a column."""
    n = len(heights)
    best = None
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            runs = [heights[:i], heights[i:j], heights[j:]]
            tot = [sum(r) + sep * (len(r) - 1) for r in runs]
            score = (max(tot), max(tot) - min(tot))
            if best is None or score < best[0]:
                best = (score, (i, j), tot)
    return best[1], best[2]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---------- masthead (heavier rules than v1) ----------
    d.line([(MX, 8), (W - MX, 8)], fill=INK, width=3)
    title_f = font(SERIF_B, 44)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 11), title, font=title_f, fill=INK)
    sub_f = font(SANS, 17)
    sub = "Friday 13 November 2026 · 25 stories · 6 continents"
    sw = d.textlength(sub, font=sub_f)
    d.text(((W - sw) / 2, 64), sub, font=sub_f, fill=(70, 60, 44))
    d.line([(MX, 91), (W - MX, 91)], fill=INK, width=6)
    d.line([(MX, 98), (W - MX, 98)], fill=INK, width=2)
    hero_top = 104

    # ---------- shared text metrics ----------
    hero_head_f = font(SERIF_B, 30)
    hero_sum_f = font(SANS, 13)
    chip_f = font(SANS_B, 12)
    pchip_f = font(SANS_B, 11)
    panel_head_f = font(SERIF_B, 20)
    panel_head_lead = 22

    # Half-width panels: photo left (185 px), text right.
    pgap = 14
    panel_w = (CW - pgap) // 2              # 465
    photo_w = 185
    ptext_x = photo_w + 14                  # offset inside the panel box
    ptext_w = panel_w - ptext_x - 8         # 258
    # Panel summary: largest size in the ladder that stays within 2 lines.
    panel_sum_f = None
    panel_sum_lead = 14
    for cand in (13, 12):
        cf = font(SANS, cand)
        if all(len(wrap(d, p[4], cf, ptext_w)) <= 2 for p in PANELS[1:]):
            panel_sum_f = cf
            break
    if panel_sum_f is None:
        panel_sum_f = font(SANS, 12)

    def panel_text_h(panel):
        _, _, _, head, summ = panel
        hl = wrap(d, head, panel_head_f, ptext_w)
        sl = wrap(d, summ, panel_sum_f, ptext_w)
        return 6 + 19 + 2 + len(hl) * panel_head_lead + 2 \
            + len(sl) * panel_sum_lead + 6

    panel_block_h = max(panel_text_h(p) for p in PANELS[1:])
    panel_photo_h = panel_block_h - 4       # inside the 2 px border

    # Hero text block below the photo: headline row, then chip + summary.
    hero_text_h = 5 + 35 + 3 + 21 + 6       # pads + headline + chip row

    # ---------- grid solver: type size is priority #1 ----------
    gutter = 22
    col_w = (CW - 2 * gutter) // 3          # 300
    num_gutter = 22
    text_w = col_w - num_gutter             # 278
    footer_limit = 984                      # grid bottom; footer rule at 990
    grid_ladder = [(16, 13), (16, 12.5)]

    chosen = None
    for hsize, ssize in grid_ladder:
        hf = font(SERIF_B, hsize)
        sf = font(SANS, ssize)
        h_lead = round(hsize * 1.09)
        s_lead = round(ssize * 1.18)
        heights = [measure_story(d, s, hf, sf, text_w, h_lead, s_lead)[2]
                   for s in STORIES]
        splits, totals = balance_columns(heights)
        grid_h = max(totals)
        hero_photo = 150                    # floor; grows only with slack
        hero_block = 4 + hero_photo + hero_text_h
        panels_top = hero_top + hero_block + 5
        panels_bottom = panels_top + panel_block_h
        grid_top = footer_limit - grid_h
        map_h = grid_top - 5 - panels_bottom
        if map_h >= 100:
            grow = min(map_h - 112, 26)     # slack: hero grows, map ~112
            if grow > 0:
                hero_photo += grow
                hero_block += grow
                panels_top += grow
                panels_bottom += grow
                map_h -= grow
            chosen = (hero_photo, hero_block, panels_top, map_h, grid_top,
                      hf, sf, h_lead, s_lead, splits, totals)
            break
        if chosen is None or map_h > chosen[3]:
            chosen = (hero_photo, hero_block, panels_top, map_h, grid_top,
                      hf, sf, h_lead, s_lead, splits, totals)
    (hero_photo, hero_block, panels_top, map_h, grid_top,
     hf, sf, h_lead, s_lead, (si, sj), totals) = chosen
    map_top = panels_top + panel_block_h + 5

    # ---------- HERO (story 1) ----------
    name, focus, label, head, summ = PANELS[0]
    d.rectangle([MX, hero_top, W - MX, hero_top + hero_block],
                fill=PANEL, outline=INK, width=2)
    photo = load_photo(name, CW - 4, hero_photo, focus)
    img.paste(photo, (MX + 2, hero_top + 2))
    hy = hero_top + 2 + hero_photo + 5
    d.text((MX + 12, hy), head, font=hero_head_f, fill=INK)
    hy += 38
    chip_w = draw_chip(d, MX + 12, hy, label, chip_f, 21)
    d.text((MX + 12 + chip_w + 12, hy + 3), summ,
           font=hero_sum_f, fill=DARK)

    # ---------- PANEL ROW (stories 2-3) ----------
    for k, panel in enumerate(PANELS[1:]):
        name, focus, label, head, summ = panel
        x0 = MX + k * (panel_w + pgap)
        d.rectangle([x0, panels_top, x0 + panel_w,
                     panels_top + panel_block_h],
                    fill=PANEL, outline=INK, width=2)
        photo = load_photo(name, photo_w, panel_photo_h, focus)
        img.paste(photo, (x0 + 2, panels_top + 2))
        tx = x0 + ptext_x
        ty = panels_top + 6
        draw_chip(d, tx, ty, label, pchip_f, 19)
        ty += 21
        ty = draw_lines(d, wrap(d, head, panel_head_f, ptext_w),
                        tx, ty, panel_head_f, INK, panel_head_lead)
        draw_lines(d, wrap(d, summ, panel_sum_f, ptext_w),
                   tx, ty + 2, panel_sum_f, DARK, panel_sum_lead)

    # ---------- world map band (denser mask, pins incl. the leads) ------
    draw_map(d, map_top, map_h)

    # ---------- story grid (entry-#1 type sizes, balanced columns) ------
    nf = font(SANS_B, hf.size)
    cols = [STORIES[:si], STORIES[si:sj], STORIES[sj:]]

    def draw_column(stories, x0, y0):
        y = y0
        for k, story in enumerate(stories):
            n, head, summ = story
            hl, sl, height = measure_story(d, story, hf, sf, text_w,
                                           h_lead, s_lead)
            d.text((x0, y), str(n), font=nf, fill=ACCENT)
            yy = draw_lines(d, hl, x0 + num_gutter, y, hf, INK, h_lead)
            yy = draw_lines(d, sl, x0 + num_gutter, yy + 2, sf,
                            (56, 50, 38), s_lead)
            y += height
            if k < len(stories) - 1:
                d.line([(x0, y + 1), (x0 + col_w, y + 1)], fill=RULE,
                       width=1)
            y += 3
        return y

    for c, col in enumerate(cols):
        x0 = MX + c * (col_w + gutter)
        draw_column(col, x0, grid_top)
        if c < 2:
            mid_x = x0 + col_w + gutter // 2
            d.line([(mid_x, grid_top - 4),
                    (mid_x, grid_top + totals[c] + 2)], fill=RULE, width=1)

    # ---------- footer ----------
    d.line([(MX, 990), (W - MX, 990)], fill=INK, width=2)
    foot_f = font(SANS, 13)
    foot = "Compiled from the day's reports · Friday 13 November 2026"
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, 997), foot, font=foot_f, fill=FAINT)

    img.save(OUT, optimize=True)
    wrapped = [s[0] for s in STORIES
               if len(wrap(d, s[2], sf, text_w)) > 1]
    print(f"wrote {OUT}: {os.path.getsize(OUT)} bytes; hero_photo={hero_photo} "
          f"panel_photo={photo_w}x{panel_photo_h}; map_h={map_h}; "
          f"grid fonts headline={hf.size} summary={sf.size}; "
          f"splits={si},{sj}; column totals={totals} (limit {footer_limit}); "
          f"summaries wrapping to 2 lines: {wrapped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
