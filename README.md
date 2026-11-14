# The World in One Day — news-image-01

**Concept.** One image that sums up the whole of Friday 13 November 2026:
a classic newspaper broadsheet front page, "THE WORLD IN ONE DAY",
carrying 25 stories under a single masthead in a 1 + 5 + 19 structure.
One big story runs as the HIGHLIGHT — the FAA ground stop as a full-width
splash: photograph of the parked fleet, a 32 px headline, a dark-red
dateline chip and its summary. Five more stories run pictured, each a
photograph with a bold label, headline and one-line summary (Hormuz, the
Ukraine talks and China's Pacific drills in a row of three; the Huang
summons and the Pope in Peru in a row of two). The remaining nineteen
stories run as a compact two-column bullet digest — a red number, a bold
headline and a short summary tail — so a viewer who missed the day can
still tell what happened from the image alone. There is deliberately no
map in this variant.

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

**Entry #3 v3 rationale (owner's variant).** After reviewing v2, the
owner asked to see a different structure before deciding: one big
highlight, a handful of pictured stories, the rest as bullet points —
and no map. V3 is that variant, built to be looked at, not yet chosen.
The FAA ground stop stays the splash, now with a 32 px headline. The
pictured bench grows from two to five — Taiwan's warning over China's
Pacific drills, the ex-Nvidia chief's summons to Congress and the Pope's
Peru visit join Hormuz and the Ukraine talks, each with its own
photograph — because in the judge's notes a photo with a bold label is
what reads instantly at thumbnail size. The other nineteen stories give
up their grid cells for a two-column bullet digest (red number, bold
headline, summary as a tail on the same flow), which keeps every headline
at digest size or better — the solver landed on 16.5 px headlines with
13 px summaries — instead of v2's smaller three-column grid. The map
band is removed entirely, per the owner's call: its space goes to the
photographs and the type. Story texts are unchanged from v2; hedged
wording stays throughout.

**Entry #3 v4 rationale (high-contrast "night edition").** Reviewing v3,
the owner found the cream page not striking enough and directed a
high-contrast palette — the competition's rules leave colour entirely
free (the gate checks only format and size; the judge's craft criterion
asks for one clear composition, legible at ~300 px, no garbled text).
V4 therefore changes nothing but the colours: v3's structure, story
texts and type sizes are carried over byte for byte in the layout, and
the page is re-inked as a night edition. The ground is a near-black ink
(#101418); headlines are a warm off-white (#F7F3EA); summaries are a
light grey (#C7CBD4) that stays clearly readable on the black; the
accent red goes vivid (#E5322D) on the label chips, the story numbers
and the masthead's lower rule, with a single amber touch (#F2B134) on
the masthead subline. Panels sit one step above the page (#1A2027)
behind a #3A4350 border so the six photographs separate cleanly and
pop. White on black is the strongest thumbnail combination the page can
offer: at 300 px the masthead, the hero headline, the panel headlines
and the bullet headlines all still read.

**How it is made.** The page is composed programmatically with PIL
(`compose.py`) — every letter is rendered by code from DejaVu Serif/Sans.
The only non-code elements are the six photographs (generated images,
committed under `assets/` and composited by the same script). A layout
solver protects the bullet headlines first (16.5 px as built), then the
hero photograph (160 px), then the panel photographs (99–135 px), then
the summary size. The masthead, the hero headline, all five panel
headlines and the bullet headlines still read at 300 px. `main.py`
installs the committed `entry.png` into the output directory.

**Story selection.** The 25 stories were chosen for breadth across regions
and fields, not just volume:

- *Highlight:* the FAA's nationwide ground stop — every U.S. departure halted
  for some four hours after an air-traffic communications outage, only the
  third such stop in U.S. history, with 15,000+ flights hit.
- *Pictured:* the Iran–U.S. escalation in the Strait of Hormuz — Tehran's
  claimed strike on a U.S. radar in Bahrain and explosions hitting four
  tankers in the strait; Ukraine peace talks widening, with Europe winning
  a seat at the table and the war's largest prisoner swap in preparation;
  China's vast unannounced Pacific drills, as warned by Taiwan; the
  ex-Nvidia chief's summons to Congress; and the Pope's meeting with abuse
  survivors in Peru.
- *Also on the page:* Ukrainian drones strike Odesa and Sumy (story 25).
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
