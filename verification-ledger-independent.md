# Independent verification ledger - Denver street occupancy permits brief (2026-10-30)

Verifier: code/verify_independent.py, Python standard library only.
It reads data/permits_raw.csv (the raw attribute dump from the pull),
never the builder's parquet, panel, or stats code, converts dates with
zoneinfo America/Denver, and recomputes each figure below. Result:
19 checks, all reproduced exactly, none corrected.

| Check | Independent | stats.json | Result |
|---|---|---|---|
| rows_total | 260061 | 260061 | PASS |
| distinct_permit_numbers | 97538 | 97538 | PASS |
| valid_records | 259284 | 259284 | PASS |
| total_segment_days | 2595960 | 2595960 | PASS |
| median_days | 3.0 | 3.0 | PASS |
| over_90_records | 4537 | 4537 | PASS |
| over_90_segment_days | 898253 | 898253 | PASS |
| over_90_segment_day_share_pct | 34.6 | 34.6 | PASS |
| same_day_records | 39933 | 39933 | PASS |
| active_on_pull_date | 631 | 631 | PASS |
| purpose_known_2018 | 1 | 1 | PASS |
| purpose_known_2020 | 23972 | 23972 | PASS |
| purpose_known_2021 | 40756 | 40756 | PASS |
| records_2021_plus | 187411 | 187411 | PASS |
| top_purpose_by_segment_days | ROW Construction | ROW Construction | PASS |
| top_purpose_segment_days | 421330 | 421330 | PASS |
| top_purpose_records | 22166 | 22166 | PASS |
| top_street_by_segment_days | 16TH ST | 16TH ST | PASS |
| top_street_segment_days | 51335 | 51335 | PASS |

Crash-fusion figures (Finding 9) are recomputed by the audit's join
section instead: the verifier has no access to the crash parquet (the
standard library cannot read parquet), so Finding 9 rests on the
audit's two-method comparison (first-leg exact vs both-legs
normalized) and the Broadway worked example, both printed in
verification.md. The builder's fusion block was additionally
recomputed in an exploratory pass with the same result (85,238
matched reports; 129,040 mentions; top-10 shares 14.2 percent of
segment-days and 10.3 percent of mentions; KSI shares 2.56 vs 2.74
percent).
