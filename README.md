# Denver Street Occupancy Permits - a Machine Readable data brief

Across 259,284 duration-valid segment records in Denver's street occupancy register (permits beginning 2017 to October 30, 2026), the median segment permit runs 3 days, while the 4,537 records running over 90 days (1.8 percent of records) account for 898,253 of the register's 2,595,960 segment-days (34.6 percent). A segment-day is one segment record multiplied by its permitted duration; it measures permitted time, not observed closure time. Register pulled October 30, 2026.

Part of Machine Readable: https://adowlen.github.io/machine-readable/

## Contents

- brief-draft.md - the brief (publishable text)
- stats.json - every figure used in the brief, produced by code/build_stats.py
- verification.md - Section 10 pre-flight audit record and methods checklist (AUDIT PASSED)
- verification-ledger-independent.md - the independent verifier's recomputation ledger
- reviewer-notes.md - claims most likely challenged, checks not completed, flags
- sources.md - dataset citations and the per-figure source audit
- social-drafts.md - LinkedIn draft (held for a future Friday synthesis under the Friday-only rule; Machine Readable never posts to X)
- hero.png - hero graphic (generated illustration, headline figure composited)
- charts/ - chart_segment_days_by_year.png, chart_duration_concentration.png, chart_purpose_segment_days.png, chart_top_streets_segment_days.png
- data/ - permits_raw.parquet (full attribute pull) and permits_raw.csv.gz (the same pull as CSV, gzipped for repository size limits; gunzip it to obtain permits_raw.csv, the independent verifier's input), street_panel.csv (per-street records, segment-days, foot-days), pull_log.json, raw_aggregates.json, audit_output.txt, verify_independent_output.json
- code/ - pull_data.py, build_stats.py, audit_section10.py, verify_independent.py, charts.py, hero_composite.py

## Dependencies (match code imports)

Python standard library; matplotlib; pandas; Pillow.

## Reuse and citation

Licensed CC-BY-4.0 (see LICENSE). Cite as: Machine Readable, "Denver's street occupancy permits: the median permit runs 3 days, but 1.8 percent of segment permits hold 34.6 percent of all occupied time" (2026), https://github.com/adowlen/denver-street-occupancy-data-brief
