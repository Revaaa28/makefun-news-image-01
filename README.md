# The World in One Day — news-image-01

**Concept.** One image that sums up the whole of Friday 13 November 2026: a
classic newspaper broadsheet front page, "THE WORLD IN ONE DAY", carrying 24
numbered stories under a single masthead. Two lead stories share the top in
shaded front-page panels; below them a dot-matrix world map carries red
numbered pins for the day's datelines, and the remaining 22 stories run in a
three-column numbered grid, each with a bold headline and a one-line
summary, so a viewer who missed the day can tell what happened from the
image alone.

**Entry #2 rationale.** Entry #1 (14 stories, text-only) measured around
rank 800 of 2,000+, while the board's top 20 all carried 19–30 stories and
several anchored the page with a numbered world map. Entry #2 fixes exactly
those two gaps — breadth up to 24 stories and a numbered world map — while
keeping entry #1's edge: every letter is still rendered by code, so the
text is perfectly legible with zero garbling.

**How it is made.** The page is composed programmatically with PIL
(`compose.py`) — every letter is rendered by code from DejaVu Serif/Sans,
and the world map is drawn by the same script as a dot matrix over a
hand-built continent mask, with red pins at each story's dateline. The
masthead, both lead headlines and the map still read clearly at 300 px.
`main.py` installs the committed `entry.png` into the output directory.

**Story selection.** The 24 stories were chosen for breadth across regions
and fields, not just volume:

- *Lead:* the FAA's nationwide ground stop — every U.S. departure halted
  for some four hours after an air-traffic communications outage, only the
  third such stop in U.S. history, with 15,000+ flights hit.
- *Co-lead:* the Iran–U.S. escalation in the Strait of Hormuz — Tehran's
  claimed strike on a U.S. radar in Bahrain and explosions hitting four
  tankers in the strait.
- *War & diplomacy:* Ukraine peace talks and the prisoner swap, Europe's
  seat at the table, Taiwan's warning over Chinese Pacific drills,
  Pakistan's border raids, the Moscow car bomb, and the jailing of rights
  lawyer Maria Bontsler.
- *Technology & finance:* the worldwide Microsoft outage, the ex-Nvidia
  chief's summons to Congress, and the $1.2B Binance-hack seizure ruling.
- *Politics & society:* the U.S. Senate leadership challenge, Trump pulling
  Vance from the Iran talks, the Kansas governor's race, the Brooklyn
  collapse toll, the Pope's meeting with abuse survivors in Peru, and EU
  politics from Dublin to Madrid.
- *Health, energy, weather, sport:* the North America measles ruling, the
  IEA oil-surplus call, Storm Charles in Portugal, and Australia's
  sandpaper row in cricket.

Together they span North and South America, Europe, the Middle East, Asia
and Australia — the whole world, in one day, on one page.
