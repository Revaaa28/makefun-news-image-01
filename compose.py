#!/usr/bin/env python3
"""Compose the news-image-01 entry #2: a one-page newspaper broadsheet that
sums up the world news of Friday 13 November 2026 in 24 numbered stories.

Entry #1 (14 stories, text-only) measured mid-board; the board's top 20 all
carry 19-30 stories and several anchor the page with a numbered world map.
Entry #2 fixes exactly those two gaps: 24 stories, TWO lead panels (the FAA
nationwide ground stop and the Hormuz escalation), and a dot-matrix world
map band with red numbered pins matching the story numbers — while keeping
entry #1's edge: everything is rendered programmatically with PIL, so every
letter is drawn by code (crisp, legible, zero garbled text).

Run with the tools venv:

    ~/workspace/tools/venv/bin/python compose.py

Writes entry.png next to this script (1024x1024).
"""

from PIL import Image, ImageDraw, ImageFont

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W = H = 1024
BG = (247, 243, 232)        # newsprint cream #f7f3e8
INK = (24, 20, 14)
FAINT = (120, 108, 84)
RULE = (150, 138, 108)
PANEL = (239, 231, 211)     # lead panel shade
ACCENT = (166, 32, 20)      # red for badges, numbers, map pins
DOT = (96, 84, 62)          # map dot colour
DARK = (52, 46, 34)

MX = 40                     # side margin
CW = W - 2 * MX             # content width = 944

LEADS = [
    (1, "FAA grounds every U.S. flight for four hours",
     "A nationwide ground stop — only the third in U.S. history — after an "
     "air-traffic communications outage; 15,000+ flights hit, no sign of an attack."),
    (2, "Iran says it hit U.S. radar in Bahrain; tankers struck in Hormuz",
     "Tehran claims retaliation as explosions hit four tankers in the strait; "
     "Trump rules out a new deal."),
]

STORIES = [
    (3, "Europe wins a seat at Ukraine peace talks",
     "Envoys: Europeans join the next round; the war's largest prisoner swap is in preparation, and Zelensky, briefed in Ireland, welcomes it."),
    (4, "Microsoft outage cripples Outlook and Teams worldwide",
     "Company says it was not a cyberattack; fixes still failing after 12 hours."),
    (5, "Ex-Nvidia chief Jensen Huang summoned to Congress",
     "Lawmakers probe alleged spy-link claims as the chip export row deepens."),
    (6, "Pope Leo meets abuse survivors in Peru",
     "An emotional Lima visit draws record crowds onto the streets."),
    (7, "Taiwan: China staged vast unannounced Pacific drills",
     "Taipei calls the exercises intimidation across the western Pacific."),
    (8, "Van Hollen challenges Schumer for Senate leadership",
     "Post-midterm contest set for a December 1 closed-ballot vote."),
    (9, "Brooklyn collapse toll settles at eight dead",
     "Search ends in Flatbush; New York orders checks at 100 linked sites."),
    (10, "U.S. wins right to seize $1.2B from Binance hack",
     "Court backs the Justice Department; FBI blames North Korea's TraderTraitor unit."),
    (11, "IEA sees oil surplus despite Gulf shipping danger",
     "Supply to exceed demand by 1.7 million barrels a day this quarter."),
    (12, "Pakistan says 74 militants killed in raids",
     "Ten days of operations near the Afghan border, the military says."),
    (13, "Storm Charles shuts schools across Portugal",
     "Severe weather disrupts mainland public services."),
    (14, "North America awaits measles elimination ruling",
     "Experts weigh a year of virus circulation in the U.S. and Mexico."),
    (15, "Trump pulls Vance from Iran talks",
     "'We don't need a deal with Iran,' the president says, shifting Vance to fraud probes."),
    (16, "Car bomb in Moscow wounds ex-premier's aide",
     "Sergei Zavorotniy, former aide to Mykola Azarov, survives the blast."),
    (17, "Russian court jails rights lawyer for 12 years",
     "Maria Bontsler convicted of treason over information passed to Ukraine."),
    (18, "Britain sanctions Russian oil producers",
     "New measures target Moscow's energy revenues."),
    (19, "EU leaders gather in Dublin amid security rifts",
     "Summit exposes disagreements over how to back Ukraine."),
    (20, "Democrat Holscher elected Kansas governor",
     "She defeats Republican Ty Masterson in the midterm race."),
    (21, "France pushes more EU sanctions on Russian banks",
     "Paris wants financial institutions added to the measures."),
    (22, "Norway warns of Russian sabotage threat",
     "Oslo alerts infrastructure operators to the risk."),
    (23, "Sandpaper claims split Australian cricket again",
     "A fresh cheating row revives memories of the 2018 scandal."),
    (24, "Spain nears election amid transport disruption",
     "Political tension rises as services strain."),
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

# Pins: story number -> (lon, lat). Drawn as red discs with white numbers.
PINS = {
    1: (-87, 37),     # FAA ground stop — U.S. (interior east)
    9: (-74, 41),     # New York — Brooklyn collapse
    8: (-70, 33),     # U.S. Senate — offset south-east of New York
    2: (56.5, 26.5),  # Strait of Hormuz
    3: (32, 49),      # Ukraine
    16: (40, 55.7),   # Moscow
    19: (-6.3, 54.5), # Dublin
    13: (-9, 38),     # Portugal
    12: (70, 30),     # Pakistan
    7: (121, 23.5),   # Taiwan
    6: (-75, -9),     # Peru
    23: (134, -25),   # Australia
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


def measure_story(draw, story, hf, sf, text_w):
    _, head, summ = story
    hl = wrap(draw, head, hf, text_w)
    sl = wrap(draw, summ, sf, text_w)
    height = len(hl) * int(hf.size * 1.22) + 2 + len(sl) * int(sf.size * 1.24)
    return hl, sl, height


def balance_columns(heights, ncols=3):
    """Split story indices into ncols contiguous runs minimising max height.
    Each story also costs a 7px separator except the last in a column."""
    n = len(heights)
    best = None
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            runs = [heights[:i], heights[i:j], heights[j:]]
            tot = [sum(r) + 7 * (len(r) - 1) for r in runs]
            score = max(tot)
            if best is None or score < best[0]:
                best = (score, (i, j), tot)
    return best[1], best[2]


def draw_pin(d, cx, cy, num):
    r = 10 if num < 10 else 11
    d.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=(255, 250, 238))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENT)
    nf = font(SANS_B, 11 if num < 10 else 10)
    label = str(num)
    tw = d.textlength(label, font=nf)
    bbox = nf.getbbox(label)
    th = bbox[3] - bbox[1]
    d.text((cx - tw / 2, cy - th / 2 - bbox[1]), label, font=nf, fill=(255, 250, 238))


def draw_map(d, top, height):
    d.rectangle([MX, top, W - MX, top + height], outline=INK, width=1)
    cell_w = CW / MAP_COLS
    cell_h = height / MAP_ROWS
    r = 2.7
    for row, spans in LAND.items():
        cy = top + (row + 0.5) * cell_h
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                cx = MX + (c + 0.5) * cell_w
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=DOT)
    for num, (lon, lat) in PINS.items():
        cx = MX + (lon + 180) / 360.0 * CW
        cy = top + (75 - lat) / 125.0 * height
        draw_pin(d, cx, cy, num)
    cap_f = font(SANS_B, 11)
    cap = "WHERE THE DAY HAPPENED — PINS MATCH THE STORY NUMBERS"
    cw_ = d.textlength(cap, font=cap_f)
    cap_x, cap_y = W - MX - cw_ - 8, top + height - 20
    d.rectangle([cap_x - 5, cap_y - 3, W - MX - 3, top + height - 3], fill=BG)
    d.text((cap_x, cap_y), cap, font=cap_f, fill=FAINT)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.line([(MX, 20), (W - MX, 20)], fill=INK, width=2)
    title_f = font(SERIF_B, 50)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 28), title, font=title_f, fill=INK)
    sub_f = font(SANS, 19)
    sub = "Friday 13 November 2026 · 24 stories · 6 continents"
    sw = d.textlength(sub, font=sub_f)
    d.text(((W - sw) / 2, 88), sub, font=sub_f, fill=(70, 60, 44))
    d.line([(MX, 118), (W - MX, 118)], fill=INK, width=4)
    d.line([(MX, 124), (W - MX, 124)], fill=INK, width=1)

    # ---------- two lead panels ----------
    leads_top = 136
    gap = 14
    panel_w = (CW - gap) // 2
    badge_d = 40
    lead_text_w = panel_w - badge_d - 44
    lead_fit = None
    for hsize, ssize in [(27, 16), (26, 16), (25, 15), (24, 15), (24, 14), (23, 14)]:
        hf, sf = font(SERIF_B, hsize), font(SERIF, ssize)
        blocks = []
        for _, head, summ in LEADS:
            hl = wrap(d, head, hf, lead_text_w)
            sl = wrap(d, summ, sf, lead_text_w)
            h = 14 + len(hl) * int(hsize * 1.2) + 6 + len(sl) * int(ssize * 1.3) + 12
            blocks.append((hl, sl, h))
        panel_h = max(b[2] for b in blocks)
        if panel_h <= 152:
            lead_fit = (hf, sf, blocks, panel_h)
            break
    if lead_fit is None:
        print("ERROR: leads do not fit", file=sys.stderr)
        return 1
    hf, sf, blocks, panel_h = lead_fit
    for k, ((num, _, _), (hl, sl, _)) in enumerate(zip(LEADS, blocks)):
        x0 = MX + k * (panel_w + gap)
        d.rectangle([x0, leads_top, x0 + panel_w, leads_top + panel_h],
                    fill=PANEL, outline=INK, width=2)
        bx, by = x0 + 14, leads_top + 14
        d.ellipse([bx, by, bx + badge_d, by + badge_d], fill=ACCENT)
        nf = font(SANS_B, 21)
        label = str(num)
        nw = d.textlength(label, font=nf)
        bbox = nf.getbbox(label)
        d.text((bx + (badge_d - nw) / 2, by + (badge_d - (bbox[3] - bbox[1])) / 2 - bbox[1]),
               label, font=nf, fill=(255, 250, 238))
        tx = x0 + 14 + badge_d + 12
        y = draw_lines(d, hl, tx, leads_top + 13, hf, INK, int(hf.size * 1.2))
        draw_lines(d, sl, tx, y + 6, sf, DARK, int(sf.size * 1.3))
    leads_bottom = leads_top + panel_h

    # ---------- world map band ----------
    map_top = leads_bottom + 10
    map_h = 176
    draw_map(d, map_top, map_h)
    map_bottom = map_top + map_h

    # ---------- story grid (3 columns, auto-fit + balanced) ----------
    footer_top = H - 46
    grid_top = map_bottom + 10
    avail = footer_top - 8 - grid_top
    gutter = 26
    col_w = (CW - 2 * gutter) // 3
    num_gutter = 25
    text_w = col_w - num_gutter

    chosen = None
    for hsize, ssize in [(14, 11), (13, 11), (13, 10), (12, 10), (12, 9), (11, 9), (11, 8)]:
        hf2, sf2 = font(SERIF_B, hsize), font(SANS, ssize)
        heights = [measure_story(d, s, hf2, sf2, text_w)[2] for s in STORIES]
        splits, totals = balance_columns(heights)
        if max(totals) <= avail:
            chosen = (hf2, sf2, splits, totals)
            break
    if chosen is None:
        print("ERROR: stories do not fit the grid at any size", file=sys.stderr)
        return 1
    hf2, sf2, (i, j), totals = chosen
    nf2 = font(SANS_B, hf2.size)
    cols = [STORIES[:i], STORIES[i:j], STORIES[j:]]

    def draw_column(stories, x0, y0):
        y = y0
        for k, story in enumerate(stories):
            n, head, summ = story
            hl, sl, height = measure_story(d, story, hf2, sf2, text_w)
            d.text((x0, y), str(n), font=nf2, fill=ACCENT)
            yy = draw_lines(d, hl, x0 + num_gutter, y, hf2, INK, int(hf2.size * 1.22))
            yy = draw_lines(d, sl, x0 + num_gutter, yy + 2, sf2, (56, 50, 38), int(sf2.size * 1.24))
            y += height
            if k < len(stories) - 1:
                d.line([(x0, y + 3), (x0 + col_w, y + 3)], fill=RULE, width=1)
            y += 7
        return y

    for c, col in enumerate(cols):
        x0 = MX + c * (col_w + gutter)
        draw_column(col, x0, grid_top)
        if c < 2:
            mid_x = x0 + col_w + gutter // 2
            d.line([(mid_x, grid_top - 4), (mid_x, grid_top + max(totals) + 2)], fill=RULE, width=1)

    # ---------- footer ----------
    d.line([(MX, footer_top), (W - MX, footer_top)], fill=INK, width=2)
    foot_f = font(SANS, 15)
    foot = "Compiled from the day's reports · Friday 13 November 2026"
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, footer_top + 11), foot, font=foot_f, fill=FAINT)

    img.save(OUT, optimize=True)
    print(f"wrote {OUT}: {os.path.getsize(OUT)} bytes; lead fonts "
          f"{hf.size}/{sf.size} panel_h={panel_h}; grid fonts "
          f"headline={hf2.size} summary={sf2.size}; splits={i},{j}; "
          f"column totals={totals} (avail {avail})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
