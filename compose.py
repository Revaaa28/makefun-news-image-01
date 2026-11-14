#!/usr/bin/env python3
"""Compose the news-image-01 entry: a one-page newspaper broadsheet that sums
up the world news of Friday 13 November 2026 in 14 numbered stories.

Everything is rendered programmatically with PIL so every letter is drawn by
code (crisp, legible, no model-generated text). Run with the tools venv:

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
ACCENT = (138, 42, 30)      # deep red for story numbers

MX = 40                     # side margin
CW = W - 2 * MX             # content width = 944

LEAD = (
    "Iran says it hit U.S. radar in Bahrain; tankers struck in Hormuz",
    "Tehran claims retaliation as explosions hit shipping in the strait; "
    "Trump rules out a new deal with Iran.",
)

STORIES = [
    (2, "Europe wins a seat at Ukraine peace talks",
     "Envoys: Europeans join the next round; the war's largest prisoner swap is in preparation."),
    (3, "Microsoft outage cripples Outlook and Teams worldwide",
     "Company says it was not a cyberattack; fixes still failing after 12 hours."),
    (4, "Ex-Nvidia chief Jensen Huang summoned to Congress",
     "Lawmakers probe alleged spy-link claims as the chip export row deepens."),
    (5, "U.S. wins right to seize $1.2B from Binance hack",
     "Court backs the Justice Department; FBI blames North Korea's TraderTraitor unit."),
    (6, "Pope Leo meets abuse survivors in Peru",
     "An emotional Lima visit draws record crowds onto the streets."),
    (7, "Taiwan: China staged vast unannounced Pacific drills",
     "Taipei calls the exercises intimidation across the western Pacific."),
    (8, "Van Hollen challenges Schumer for Senate leadership",
     "Post-midterm contest set for a December 1 closed-ballot vote."),
    (9, "Brooklyn collapse toll settles at eight dead",
     "Search ends in Flatbush; New York orders checks at 100 linked sites."),
    (10, "IEA sees oil surplus despite Gulf shipping danger",
     "Supply to exceed demand by 1.7 million barrels a day this quarter."),
    (11, "North America awaits measles elimination ruling",
     "Experts weigh a year of virus circulation in the U.S. and Mexico."),
    (12, "Pakistan says 74 militants killed in raids",
     "Ten days of operations near the Afghan border, the military says."),
    (13, "Storm Charles shuts schools across Portugal",
     "Severe weather disrupts mainland public services."),
    (14, "Sandpaper claims split Australian cricket again",
     "A fresh cheating row revives memories of the 2018 scandal."),
]


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
    """Return (headline_lines, summary_lines, height) for one grid story."""
    _, head, summ = story
    hl = wrap(draw, head, hf, text_w)
    sl = wrap(draw, summ, sf, text_w)
    height = len(hl) * int(hf.size * 1.22) + 2 + len(sl) * int(sf.size * 1.24)
    return hl, sl, height


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.line([(MX, 26), (W - MX, 26)], fill=INK, width=2)
    title_f = font(SERIF_B, 57)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 36), title, font=title_f, fill=INK)
    sub_f = font(SANS, 21)
    sub = "Friday 13 November 2026 · 14 stories · 6 continents"
    sw = d.textlength(sub, font=sub_f)
    d.text(((W - sw) / 2, 108), sub, font=sub_f, fill=(70, 60, 44))
    d.line([(MX, 142), (W - MX, 142)], fill=INK, width=4)
    d.line([(MX, 149), (W - MX, 149)], fill=INK, width=1)

    # ---------- lead story ----------
    lead_top = 164
    lead_hf = font(SERIF_B, 35)
    lead_sf = font(SERIF, 20)
    badge_w = 64
    lead_text_w = CW - badge_w - 36
    lead_hl = wrap(d, LEAD[0], lead_hf, lead_text_w)
    lead_sl = wrap(d, LEAD[1], lead_sf, lead_text_w)
    lead_h = 20 + len(lead_hl) * 43 + 8 + len(lead_sl) * 26 + 18
    d.rectangle([MX, lead_top, W - MX, lead_top + lead_h], fill=PANEL, outline=INK, width=2)
    # number badge
    bx, by = MX + 16, lead_top + 18
    d.rectangle([bx, by, bx + 46, by + 46], fill=ACCENT)
    num_f = font(SANS_B, 30)
    nw = d.textlength("1", font=num_f)
    d.text((bx + (46 - nw) / 2, by + 5), "1", font=num_f, fill=(255, 250, 238))
    tx = MX + badge_w + 16
    y = draw_lines(d, lead_hl, tx, lead_top + 18, lead_hf, INK, 43)
    y = draw_lines(d, lead_sl, tx, y + 8, lead_sf, (52, 46, 34), 26)
    grid_top = lead_top + lead_h + 16

    # ---------- story grid (2 columns, auto-fit) ----------
    footer_top = H - 56
    avail = footer_top - 10 - grid_top
    gutter = 30
    col_w = (CW - gutter) // 2
    num_gutter = 30
    text_w = col_w - num_gutter
    col_a = STORIES[:7]   # stories 2-8
    col_b = STORIES[7:]   # stories 9-14

    chosen = None
    for hsize, ssize in [(18, 15), (17, 15), (17, 14), (16, 14), (16, 13), (15, 13)]:
        hf, sf = font(SERIF_B, hsize), font(SANS, ssize)
        ha = sum(measure_story(d, s, hf, sf, text_w)[2] for s in col_a) + 6 * 7
        hb = sum(measure_story(d, s, hf, sf, text_w)[2] for s in col_b) + 5 * 7
        if max(ha, hb) <= avail:
            chosen = (hf, sf, ha, hb)
            break
    if chosen is None:
        print("ERROR: stories do not fit the grid at any size", file=sys.stderr)
        return 1
    hf, sf, ha, hb = chosen
    nf = font(SANS_B, hf.size)

    def draw_column(stories, x0, y0):
        y = y0
        for i, story in enumerate(stories):
            n, head, summ = story
            hl, sl, height = measure_story(d, story, hf, sf, text_w)
            d.text((x0, y), str(n), font=nf, fill=ACCENT)
            yy = draw_lines(d, hl, x0 + num_gutter, y, hf, INK, int(hf.size * 1.22))
            yy = draw_lines(d, sl, x0 + num_gutter, yy + 2, sf, (56, 50, 38), int(sf.size * 1.24))
            y += height
            if i < len(stories) - 1:
                d.line([(x0, y + 3), (x0 + col_w, y + 3)], fill=RULE, width=1)
            y += 7
        return y

    draw_column(col_a, MX, grid_top)
    draw_column(col_b, MX + col_w + gutter, grid_top)
    mid_x = MX + col_w + gutter // 2
    d.line([(mid_x, grid_top - 4), (mid_x, grid_top + max(ha, hb) + 2)], fill=RULE, width=1)

    # ---------- footer ----------
    d.line([(MX, footer_top), (W - MX, footer_top)], fill=INK, width=2)
    foot_f = font(SANS, 16)
    foot = "Compiled from the day's reports · Friday 13 November 2026"
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, footer_top + 12), foot, font=foot_f, fill=FAINT)

    img.save(OUT, optimize=True)
    print(f"wrote {OUT}: {os.path.getsize(OUT)} bytes; grid fonts "
          f"headline={hf.size} summary={sf.size}; column heights A={ha} B={hb} (avail {avail})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
