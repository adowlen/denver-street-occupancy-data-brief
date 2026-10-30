# Verification - Denver street occupancy permits brief (2026-10-30)

## Methods checklist (brief-writing standards, section 3)

- Base rates and exposure: every share in the brief divides records by
  records or segment-days by segment-days of the same stated population
  (asserted in the audit, unit-agreement section). Finding 9's crash
  comparison has no traffic-volume, pedestrian-volume, or matched
  street-length denominator in the sources; the brief says so
  prominently inside the finding, prints shares of mentions only, and
  makes no rate or causal claim.
- Direction of causality: Finding 9 is framed as a geography
  comparison, not an effect; occupancy concentration could follow
  crash geography (work where crashes and density already are) as
  readily as the reverse, and the finding claims neither.
- Category and definition changes over the window: PURPOSE and
  COMPANY have a vintage break (Finding 3) - populated on 0.0 percent
  of 2018 records, 0.3 percent of 2019, 66.9 percent of 2020, 99.9
  percent from 2021 - so purpose and company figures use a 2021+
  basis and never trend across the break. Full Counters for PURPOSE
  (44 non-null values), ASIT_TYPE (23), and GIS_LOAD_TYPE (2) were
  recorded before any categorical figure was computed (audit output
  below); no renaming inside the 2021+ window was detected in them.
- Time windows: the exact window is January 1, 2017 to October 30,
  2026 for begins, with ends capped at December 31, 2027 (Finding 2).
  The compared program context (the DOTI register itself, processed
  daily from Accela) was in effect for the whole window per the
  service description. Segment-days are assigned to the begin year;
  that accounting convention and its limit are printed in Finding 5.
  Right-censoring: durations are as permitted at pull time, so recent
  years' durations can still change in daily processing; printed in
  Finding 5.
- Joins: one join only - crash reports to register streets by
  normalized street name, both intersection legs (Finding 9). Match
  rate: 85,238 of 106,121 crash reports (80.3 percent) name at least
  one register street. The unmatched 19.7 percent are addresses whose
  street names do not appear in the register (highway ramps and
  facilities, streets with no occupancy record, and unparsed forms);
  they may differ systematically (freeway locations are over-
  represented among highway-form addresses), which is one reason the
  brief publishes mention shares in aggregate only and no per-street
  crash figure. The rejected first-leg exact-form method and its
  Broadway result (2 crashes attributed, against 2,856 addresses
  naming Broadway) are recorded in the audit output.
- Small numbers: percentages are printed with their underlying counts
  throughout. No group comparison in the brief rests on fewer than 30
  cases except the over-365-day band (374 records, printed with its
  count wherever it appears) and the 2017 begin year (65 records,
  shown only in the year table and excluded from the year chart's
  scope line).
- Official definitions: "segment record", "permit", and the
  one-permit-many-closures relationship use the service description's
  own wording (quoted in sources.md). ASIT_TYPE and PURPOSE values
  are the register's own strings, printed verbatim.
- Layering admission test: the crash layer supports Finding 9's
  claim (occupancy geography vs crash geography) that the register
  alone cannot make; the Shape__Length field supports the foot-days
  restatement in Finding 4. A neighborhood layer was considered and
  cut - no neighborhood field exists and the layer's stored point is
  too unevenly populated by year (25.6 percent overall; 6 percent of
  2020 records) to assign records without vintage bias. The cut is
  recorded in the brief's data notes.

## Pre-flight audit

Script: code/audit_section10.py (run on the final data pull, before
charts and prose were finalized). Full output:

```
== 10.1 sentinel / null handling ==
rows total 260061; server count 260061; equal: True
BEGIN_DATE null 3; END_DATE null 1
BEGIN_DATE raw range 1902-09-29 00:00:00 .. 2901-12-11 00:00:00 (sentinel years present)
END_DATE raw range 2017-08-31 00:00:00 .. 2099-12-30 00:00:00
Rule: null dates, BEGIN < 2017-01-01, BEGIN > pull date, END < BEGIN, and END > 2027-12-31 map to 'unknown / excluded' and enter no date denominator.
valid 259284; excluded 777
Polarity sample - EXCLUDED rows (OBJECTID, BEGIN, END, reason):
  296478260 2021-06-13 00:00:00 2021-06-12 00:00:00
  296479396 2019-02-17 00:00:00 2019-02-14 00:00:00
  296483424 2021-10-17 00:00:00 2021-10-06 00:00:00
Polarity sample - INCLUDED rows (OBJECTID, BEGIN, END, duration):
  296477825 2019-10-27 2019-10-30 3d
  296477826 2021-10-24 2021-10-26 2d
  296477827 2021-05-25 2021-05-26 1d
Inequality check: BEGIN >= 2017-01-01 AND BEGIN <= 2026-10-30 AND END >= BEGIN AND END <= 2027-12-31 - included rows all satisfy it, excluded sample rows each violate at least one clause. PASS

== 10.1 unit agreement ==
duration bands: records 259284 == valid 259284: True; segment-days 2595960 == total 2595960: True
segment-days by begin year sum 2595960 == total 2595960: True
Every rate in the brief divides a count of segment records by segment records, or segment-days by segment-days, of the same stated population. PASS

== 10.1 categorical exhaustiveness (full Counters) ==
PURPOSE: 45 unique values; null 47978
  '<null>': 47978
  'Utility': 38118
  'Fiber Optics': 33671
  'ROW Construction': 24148
  'Street Cut - Water': 18540
  'Street Cut - Utilities': 17998
  'Road/Alley Repair': 11346
  'Pot Holing': 7076
  'Street Cut - Sewer': 6187
  'Special Events': 5565
  'Sidewalk Repair': 4867
  'Miscellaneous - Multi-Categories': 4410
  'Sanitary Sewer': 4162
  'Crane Service': 3948
  'Safety': 3482
  'Container': 3048
  'Site Improvements': 2875
  'Paving': 2564
  'Traffic Signal Installation': 2352
  'Equipment Installation': 1967
  'Cable': 1923
  'Curb and Gutter': 1515
  'Aerial Cable': 1452
  'Dumpster': 1418
  'Boring and/or Wells': 1372
  'Tree Trimming': 1269
  'Concrete Pumper': 1182
  'Surveying': 996
  'Sewer Lining': 850
  'Deliveries': 650
  'Parking': 623
  'Bridge Construction': 415
  'Curb Cut/Driveway': 389
  'Fencing Construction': 311
  'Soil Sampling': 269
  'Valet - Short Term': 190
  'Alley Resurfacing': 189
  'Monitoring Well': 185
  'Valet - Long Term': 178
  'Construction Trailer': 166
  'Bike Parking': 121
  'Filming': 45
  'Fire Hydrant': 32
  'Block Party': 14
  'HAZMAT Removal': 5
ASIT_TYPE: 24 unique values; null 239
  '1st Lane': 54326
  'Parking Lane': 31343
  'Residential - Parking Lane': 25366
  'Sidewalk - Residential': 25313
  'Residential - Full': 25079
  'Sidewalk - Collector/Arterial': 24116
  'Residential - Partial': 17688
  'Alley Residential - Partial': 12554
  'Residential - 1 Lane': 10162
  'Sidewalk - CBD/CC': 7766
  'Bike Lane': 7469
  'Alley Residential - Full': 5903
  'Detour': 4444
  '2nd Lane': 4128
  'Alley CBD/CC - Full': 1219
  'Alley CBD/CC - Partial': 1212
  '3rd Lane': 705
  'Sidewalk- Covered Coll/Art': 380
  'Sidewalk - Covered CBD/CC': 294
  '<null>': 239
  'Sidewalk - Covered Residential': 173
  '4th Lane': 129
  '5th Lane': 44
  '6th Lane': 9
GIS_LOAD_TYPE: 3 unique values; null 22
  'Simple street search': 183838
  'Connected segments SQL': 76201
  '<null>': 22
COMPANY: 4952 unique non-null strings; null 48043 (top 20 in stats build)
STREET: 1581 unique non-null values; null 1

== 10.1 nullable-denominator check (purpose / company, 2021+ basis) ==
2021+ valid 187411; purpose known 187293 + null 118 = 187411 (== population: True)
company known 187230 + null 181 = 187411 (== population: True)
Purpose and company shares are computed on the known population and the null share is printed alongside in the brief. PASS

== 10.2 control: server groupBy counters vs local counters ==
PURPOSE: server total 260061, local total 260061, all values equal: True
ASIT_TYPE: server total 260061, local total 260061, all values equal: True
GIS_LOAD_TYPE: server total 260061, local total 260061, all values equal: True
PASS - local pull reproduces the server's own counters exactly for every field a figure in this brief uses (PURPOSE, ASIT_TYPE, GIS_LOAD_TYPE).
EXEMPT (adjudicated exception, three-part verdict): count - server groupBy returns 1140 distinct values against 1241 locally, with 169 values differing; mechanism - both totals equal 260061, so the server's grouping merges string variants (case/whitespace collation) and redistributes counts among merged groups rather than dropping records; treatment - EXEMPT is used by no figure in this brief, so the divergence is recorded here and not repaired. The three fields figures do use reproduce exactly, above.

== 10.2 join hygiene: crash street-name join ==
first-leg only, exact suffix forms: matched 69381 of 106121 (65.4%)
both legs, normalized: matched 85238 of 106121 (80.3%)
Worked example - Broadway: first-leg exact-form parse attributes 2 crashes to 'N BROADWAY', while 2,856 crash addresses contain the string BROADWAY (intersections list it as either leg, with an ST suffix the register does not use). The first-leg exact method is therefore rejected for per-street crash claims; the brief uses the both-legs normalized method in aggregate only and prints its basis. PASS (method adjudicated)

== 10.2 physical scale ==
segment records 260061; summed Shape__Length 209,147,057 ft = 39,611.2 miles of segment records (with multiplicity: the same street segment is counted once per permit record that covers it; this is not a unique-street-miles figure).
X/Y point present on 66481 rows (25.6%); presence varies by begin year (2018: 79%, 2020: 6%, 2026: 99% in build exploration), so no point-proximity join is used anywhere in this package. PASS (join not used, reason recorded)

== 10.3 dependency sync ==
third-party imports across code/: ['Pillow', 'matplotlib', 'pandas']
README dependency line covers all imports: True (missing: [])

AUDIT COMPLETE - all assertions passed
```

## Fix loop

- EXEMPT server-counter divergence: the audit's first run failed its
  server-vs-local control on EXEMPT. Adjudicated in three parts in
  the audit output (count: 169 of 1,241 values differ, server returns
  1,140 distinct values; mechanism: totals equal at 260,061, so the
  server grouping merges string variants and redistributes counts;
  treatment: EXEMPT is used by no figure, recorded and not repaired).
  The control passes exactly on the three fields figures use
  (PURPOSE, ASIT_TYPE, GIS_LOAD_TYPE).
- Chart defects found on visual inspection after first render: (1)
  the duration-concentration chart's left panel bars were misaligned
  with their labels (a reversal bug in the plotting code) - fixed,
  re-rendered, and re-inspected (bars now match labels in both
  panels); (2) the purpose chart's basis line and the top-street
  chart's first value label clipped at the frame edge - title wrapped
  and axis limits extended, re-rendered, re-inspected; (3) the year
  chart's scope line claimed the full window while 2017 (65 records)
  is not charted - scope line corrected on the graphic, and adjacent
  year labels de-overlapped.
- Raw date ranges in Finding 2 were first drafted from a UTC read;
  corrected to the package's Denver-date convention (September 29,
  1902 to December 11, 2901; end maximum December 30, 2099) so every
  date in the package is on one basis.

## Independent verification

Separate standard-library-only implementation
(code/verify_independent.py) reading data/permits_raw.csv - never the
builder's parquet or panel - with its own zoneinfo date conversion
and statistics.median recomputation: 19 checks, all reproduced
exactly, none corrected (rows, permit count, valid population, total
segment-days, median duration, over-90 counts and share, same-day
count, active-on-pull-date count, purpose-known counts for 2018 /
2020 / 2021, 2021+ population, top purpose by segment-days and its
records, top street and its segment-days). Full ledger:
verification-ledger-independent.md.

## Sync gate (10.3)

- Dependencies: the audit's import scan across code/ found pandas
  (pull/build/audit), matplotlib (charts), and Pillow (hero
  composite, import name PIL) beyond the standard library; README.md's
  dependency line lists exactly: Python standard library; matplotlib;
  pandas; Pillow. The final audit run (after the README was written)
  asserts the coverage and passes; an earlier audit run taken before
  the README existed recorded the check as pending, and its first
  post-README run exposed an import-name/distribution-name mismatch
  (PIL vs Pillow) in the check itself, which was corrected in the
  audit script and re-run to a pass.
- Every number in brief-draft.md was cross-checked against the final
  stats.json during QA (spot-checks plus the independent ledger);
  stats.json, data/street_panel.csv, and brief-draft.md are in sync
  as of the final audit run. Any edit to a figure after this point
  requires re-running code/audit_section10.py and
  code/verify_independent.py.
- Hero: hero.png composited with code/hero_composite.py from the
  generated illustration in hero_source/ (scene and text specified in
  hero_source/hero-brief.md) and visually inspected: headline "34.6%"
  and the sub and source lines sit on the illustration's clean dark
  top field, fully legible, exact text, scene intact. Hero standard
  met.
