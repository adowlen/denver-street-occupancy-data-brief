# Sources - Denver street occupancy permits brief (2026-10-30)

Every figure in the brief traces to one of the sources below. Derived
figures are labeled derived and state their inputs.

## Street occupancy register (Findings 1-8, 10)

- Source: City and County of Denver open data,
  ODC_DEV_STREETOCCUPANCYPPERMITS_L ("street occupancy permits"),
  ArcGIS FeatureServer layer 297, services1.arcgis.com/zdB7qR0BtYrg0Xpl.
  Service description: "This layer shows the locations of street
  occupancy permits extracted from the Accela permit database. The
  dataset includes expired, currently active, and future scheduled
  permits. A single permit may encompass multiple closures across
  several street segments and affect different portions of the
  street - such as the sidewalk, a turn lane, or all lanes. The data
  is maintained by the Department of Transportation and
  Infrastructure and processed daily by the Technology Services GIS
  group."
- Pull: October 30, 2026, full layer, attributes (data/permits_raw.parquet
  and data/permits_raw.csv.gz, the CSV pull gzipped for repository
  size limits; pull record in data/pull_log.json;
  server-side counters in data/raw_aggregates.json). Server count
  260,061 and local count 260,061, equal. The same service reported
  259,891 records on October 29, 2026 (lead verification).
- Service vintage: editingInfo.lastEditDate 1793357158944 =
  October 30, 2026, 04:45 MDT, as reported by the service.
- Figures taken directly: total 260,061; distinct PERMIT_NUMBER
  97,538 plus 1 null; PURPOSE counter (44 non-null values, 47,978
  null in the full pull); ASIT_TYPE counter (23 non-null values, 239
  null); COMPANY 4,952 distinct non-null strings in the full pull,
  48,043 null; GIS_LOAD_TYPE counter (Simple street search 183,838;
  Connected segments SQL 76,201; null 22); X_COORD present 66,481;
  Shape__Length sum 209,147,057 feet.
- Derived: rows per permit (median 2, max 94, 44,294 single-row
  permits); segment length in miles (39,611.2); all durations,
  segment-days, foot-days, shares, medians, and per-year, per-purpose,
  per-company, per-ASIT, and per-street tables (inputs: BEGIN_DATE and
  END_DATE as Denver calendar dates, ASIT_TYPE, PURPOSE, COMPANY,
  STREET, Shape__Length, on the populations stated with each figure;
  full results in stats.json and data/street_panel.csv).

## Date handling and window (Finding 2)

- Derived by this brief's stated rules: dates converted from epoch
  milliseconds to America/Denver calendar dates; duration = END minus
  BEGIN in days; window = BEGIN between January 1, 2017
  and October 30, 2026, END present, END >= BEGIN,
  END <= December 31, 2027. Class counts: BEGIN null 3; END null 1;
  BEGIN before 2017: 16; BEGIN after pull: 665 (650 future-scheduled
  valid; 13 begin after 2027; 2 with END a year before BEGIN - begin
  April 21, 2027, end April 22, 2026); in-window END before BEGIN: 68;
  in-window END after cap: 25; raw END before BEGIN anywhere: 83;
  raw BEGIN range September 29, 1902 to December 11, 2901; raw END
  maximum December 30, 2099. Duration-valid population: 259,284.

## Vintage break (Finding 3)

- Derived: purpose-known and company-known counts by begin year on
  the duration-valid population (stats.json vintage_break_by_year):
  purpose known 2018: 1 of 9,771; 2019: 87 of 26,185; 2020: 23,972 of
  35,852; 2021: 40,756 of 40,793. Records with both fields null:
  47,775 of 259,284.

## Purpose and company (Findings 6 and 7), 2021+ basis

- Derived on the 187,411 duration-valid records with BEGIN on or
  after January 1, 2021: purpose known 187,293, company known
  187,230. Purpose by segment-days: ROW Construction 421,330
  (22,166 records, median 8 days); Utility 216,518 (34,645, median
  4); Safety 175,848 (2,599, median 16); Street Cut - Water 150,532
  (17,036, median 5); Street Cut - Utilities 112,034 (17,037, median
  4); Miscellaneous - Multi-Categories 108,330 (3,996, median 4);
  Fiber Optics 80,484 (25,465, median 2); Bike Parking 76,881 (121,
  median 585). Company exact strings: DENVER WATER BOARD 21,205
  records / 207,816 segment-days; XCEL ENERGY-CENTRAL METRO 20,263 /
  95,099; PAULEY CONSTRUCTION LLC 10,397 records; CCD (CPM Trans) &
  PCL 1,203 records / 56,048 segment-days. Strings containing XCEL:
  179 distinct strings, 37,451 records, 209,891 segment-days (derived
  by substring match, printed as a string statistic, never as a
  holder total).

## Portion of street and streets (Finding 8)

- Derived on the full duration-valid window: ASIT classes 1st Lane
  54,234 records / 461,970 segment-days; Parking Lane 412,385
  segment-days; sidewalk classes combined 57,837 records / 724,266
  segment-days; full-closure classes 32,052 / 306,751; Bike Lane
  7,450 / 51,344. Streets (exact STREET values, 1,562 distinct):
  16TH ST 1,200 records / 51,335 segment-days / median 3 / mean 42.8;
  LARIMER ST 1,697 / 42,928; BLAKE ST 1,744 / 28,525; E COLFAX AVE
  2,364 / 27,647 and 64,124,408 foot-days; N BROADWAY 1,781 / 25,739;
  15TH ST 2,389 records. Top-10 street share of segment-days: 11.3
  percent. 16TH ST largest company string: CCD (CPM Trans) & PCL,
  378 records. Full panel: data/street_panel.csv.

## Crash fusion (Finding 9)

- Source: Machine Readable traffic accidents layer
  (stack/denver/layers/traffic_accidents_clean.parquet), built from
  Denver open data crash reports (ODC_CRIME_TRAFFICACCIDENTS5YR_P
  lineage, as built for the 2026-10-18 traffic accidents brief):
  reported date in America/Denver on or after January 1, 2021,
  deduplicated on offense_id, through October 15, 2026; 106,121
  reports.
- Derived by this brief's street-name join (normalization and
  both-legs counting as printed in Finding 9 and the audit record):
  85,238 of 106,121 reports (80.3 percent) name at least one register
  street; 129,040 total street mentions; the 10 normalized street
  groups with the most 2021+ occupancy segment-days hold 14.2 percent
  of 2021+ segment-days and 13,240 mentions (10.3 percent); KSI share
  of mentions (ksi_crash_count_basis, crash-count basis): top-10
  groups 2.56 percent, all mentions 2.74 percent; COLFAX group 4,387
  mentions / 132 KSI; BROADWAY group 2,434 / 64.
- Rejected method, recorded: first-leg exact-form address parsing
  attributes 2 crashes to "N BROADWAY" while 2,856 crash addresses
  contain the string BROADWAY. No per-street crash figure is
  published from either method.

## Snapshot (Finding 10)

- Derived: records with BEGIN <= October 30, 2026 <= END on the
  duration-valid population: 631 active; median total duration 31
  days; 185 with duration over 90 days; top purposes ROW Construction
  197, Street Cut - Water 75, Street Cut - Utilities 63; top company
  strings KRAEMER NORTH AMERICA LLC 54, DENVER WATER BOARD 43,
  HOOPER CORPORATION 29. Future-scheduled valid records: 650.

## Not used (deliberate exclusions)

- X_COORD / Y_COORD point proximity: the stored point is present on
  only 25.6 percent of records and its presence varies by begin year
  (79 percent of 2018 records, 6 percent of 2020, 99 percent of 2026),
  so any proximity join would be biased by the load vintage.
- EXEMPT: populated on 72,330 records; used by no figure. Its
  server-side groupBy does not reproduce the local counter (server
  returns 1,140 distinct values against 1,241 locally, totals equal);
  adjudicated in the audit record.
- Neighborhood assignment: no neighborhood field exists in the
  layer, and the uneven point population bars a point-based
  assignment. Cut per the layering admission test and recorded in
  the brief's data notes.
