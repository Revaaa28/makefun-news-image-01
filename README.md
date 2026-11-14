# The World in One Day — news-image-01

**Concept.** One image that sums up the whole of Friday 13 November 2026: a
classic newspaper broadsheet front page, "THE WORLD IN ONE DAY", carrying 14
numbered stories under a single masthead. The lead story sits in a shaded
front-page panel; the other 13 run in a two-column numbered grid, each with a
bold headline and a one-line summary, so a viewer who missed the day can tell
what happened from the image alone.

**How it is made.** The page is composed programmatically with PIL
(`compose.py`) — every letter is rendered by code from DejaVu Serif/Sans, so
the text is perfectly legible with zero garbling at full size and the
masthead, lead headline and grid structure still read clearly at 300 px.
`main.py` installs the committed `entry.png` into the output directory.

**Story selection.** The 14 stories were chosen for breadth across regions
and fields, not just volume:

- *Lead:* the Iran–U.S. escalation in the Strait of Hormuz — the day's
  biggest story, touching energy markets and Gulf security at once.
- *War & diplomacy:* Ukraine peace talks and the prisoner swap, Taiwan's
  warning over Chinese Pacific drills, Pakistan's border raids.
- *Technology & finance:* the worldwide Microsoft outage, the ex-Nvidia
  chief's summons to Congress, and the $1.2B Binance-hack seizure ruling.
- *Politics & society:* the U.S. Senate leadership challenge, the Brooklyn
  collapse toll, the Pope's meeting with abuse survivors in Peru.
- *Health, energy, weather, sport:* the North America measles ruling, the
  IEA oil-surplus call, Storm Charles in Portugal, and Australia's
  sandpaper row in cricket.

Together they span the Middle East, Europe, Asia-Pacific, North and South
America and Australia — the whole world, in one day, on one page.
