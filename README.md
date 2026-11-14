# The World in One Day — news-image-01

**Concept.** One image that sums up the whole of Friday 13 November 2026: a
classic newspaper broadsheet front page, "THE WORLD IN ONE DAY", carrying 25
numbered stories under a single masthead. The day's biggest story — the FAA
ground stop — runs as a full-width hero splash: a photograph of the parked
fleet, a dark-red dateline chip, a 30 px headline and its summary in one
row. The next two leads (Hormuz, the Ukraine talks) run as half-width
thumbnail panels, photograph beside chip, headline and summary. Below them
a dense dot-matrix world map carries big red numbered pins for thirteen
stories — the three leads included — and the remaining 22 stories run in a
three-column numbered grid, each with a bold headline and a one-line
summary, so a viewer who missed the day can tell what happened from the
image alone.

**Entry #2 rationale.** Entry #1 (14 stories, text-only) measured around
rank 800 of 2,000+, while the board's top 20 all carried 19–30 stories and
several anchored the page with a numbered world map. Entry #2 fixes exactly
those two gaps — breadth up to 24 stories and a numbered world map — while
keeping entry #1's edge: every letter is still rendered by code, so the
text is perfectly legible with zero garbling.

**Entry #3 rationale.** The judge's own breakdown notes on the first two
entries set this design. The provisional matches are against house images:
four anchors plus two illustrated collage "rungs" (4-panel and 6-panel;
each story a photo with a bold label). Entries #1 and #2 both beat the
anchors on day-specificity and breadth, but entry #2 (24 stories, small
type) won fewer duels than entry #1 (14 stories, big type) — 8W-3D-1L
against 10W-1D-1L — because at 300 px its dense grid was "unreadable fine
print": only the masthead and lead headlines survived, while the 6-panel
rung's panels each read instantly. Entry #3 therefore combines both
lessons: breadth (25 stories) *and* legibility. The top is a row of three
illustrated panels in the rungs' own language — photo plus bold label plus
headline — for the FAA ground stop, the Hormuz escalation and the Ukraine
talks. The grid goes back to entry-#1 type sizes (bold headlines at 16 px,
one-line summaries), with summaries cut to fit one line rather than
shrinking the font, and the map pins grow to match. Hedged wording ("Iran
says", "Tehran claims", "Pakistan says") is kept throughout: the judges
credit it as an accuracy signal, and the anchor stories stay prominent.

**Entry #3 v2 rationale.** The owner reviewed v1 and ordered a visual
rebuild — same 25 stories, same words, stronger front page. Three fixes.
First, presence: v1's three equal panels gave the day's biggest story the
same weight as its neighbours, so the FAA ground stop now runs as a
full-width hero splash and the other two leads become thumbnail panels.
Second, the map: v1's pins covered only grid stories — the three leads had
no pins at all, so the map's numbers looked irrelevant — and its sparse
dot matrix read as a sketch. The v2 map is drawn from a finer 140x46 mask
(resampled from v1's, then hand-shaped: a real Atlantic gap, a Hudson Bay
notch, a Mediterranean channel, a full Africa) and carries thirteen pins,
stories 1–3 included, every number matching the story number on the page.
Third, energy: heavier black masthead rules, dark-red label chips and a
deeper red for numbers and labels. The layout solver protects the grid's
type first (16 px headlines, 13 px one-line summaries), then the hero
photo (150 px), the panel photos (103 px) and the map (110 px) — all four
floors hold at once.

**How it is made.** The page is composed programmatically with PIL
(`compose.py`) — every letter is rendered by code from DejaVu Serif/Sans,
and the world map is drawn by the same script as a dot matrix over a
hand-built continent mask, with big red pins at the datelines of the
three leads and ten grid stories. The only non-code elements are the
three photographs (generated images, committed under `assets/` and
composited by the same script). The masthead, the hero headline, both
panel headlines and the grid headlines still read clearly at 300 px.
`main.py` installs the committed `entry.png` into the output directory.

**Story selection.** The 25 stories were chosen for breadth across regions
and fields, not just volume:

- *Top panel 1:* the FAA's nationwide ground stop — every U.S. departure halted
  for some four hours after an air-traffic communications outage, only the
  third such stop in U.S. history, with 15,000+ flights hit.
- *Top panel 2:* the Iran–U.S. escalation in the Strait of Hormuz — Tehran's
  claimed strike on a U.S. radar in Bahrain and explosions hitting four
  tankers in the strait.
- *Top panel 3:* Ukraine peace talks widen — Europe wins a seat at the
  table, the war's largest prisoner swap is in preparation, and Ukrainian
  drones strike Odesa and Sumy (story 25).
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
