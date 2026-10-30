"""Independent verifier for the Denver street occupancy brief.

Standard library only. Reads data/permits_raw.csv (the raw attribute
dump, never the builder's parquet or stats) and recomputes the
decisive figures with its own date handling (zoneinfo America/Denver)
and statistics.median. Writes data/verify_independent_output.json and
prints a PASS/FAIL line per check against stats.json.
"""
import csv, json, pathlib, statistics
from collections import Counter
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

HERE = pathlib.Path(__file__).resolve().parent.parent
DATA = HERE / "data"
DEN = ZoneInfo("America/Denver")
PULL = datetime(2026, 10, 30).date()
WIN = datetime(2017, 1, 1).date()
CAP = datetime(2027, 12, 31).date()


def ldate(ms):
    if ms in ("", None):
        return None
    return datetime.fromtimestamp(int(float(ms)) / 1000, tz=timezone.utc).astimezone(DEN).date()


def main():
    stats = json.loads((HERE / "stats.json").read_text())
    rows = list(csv.DictReader(open(DATA / "permits_raw.csv", newline="", encoding="utf-8")))
    checks = []

    def check(name, mine, theirs):
        ok = mine == theirs
        checks.append({"check": name, "independent": mine, "stats_json": theirs, "pass": ok})
        print(("PASS " if ok else "FAIL ") + f"{name}: {mine} vs {theirs}")

    check("rows_total", len(rows), stats["date_classes"]["rows_total"])
    permits = Counter(r["PERMIT_NUMBER"] for r in rows if r["PERMIT_NUMBER"])
    check("distinct_permit_numbers", len(permits), stats["register"]["distinct_permit_numbers"])

    valid = []
    for r in rows:
        b, e = ldate(r["BEGIN_DATE"]), ldate(r["END_DATE"])
        if b and e and WIN <= b <= PULL and e >= b and e <= CAP:
            valid.append((r, b, e, (e - b).days))
    check("valid_records", len(valid), stats["date_classes"]["valid_records"])
    total_sd = sum(d for _, _, _, d in valid)
    check("total_segment_days", total_sd, stats["duration"]["total_segment_days"])
    med = statistics.median(d for _, _, _, d in valid)
    check("median_days", float(med), stats["duration"]["median_days"])
    over90 = [d for _, _, _, d in valid if d > 90]
    check("over_90_records", len(over90), stats["duration"]["over_90_records"])
    check("over_90_segment_days", sum(over90), stats["duration"]["over_90_segment_days"])
    share = round(100.0 * sum(over90) / total_sd, 1)
    check("over_90_segment_day_share_pct", share, stats["duration"]["over_90_segment_day_share_pct"])
    same_day = sum(1 for _, _, _, d in valid if d == 0)
    check("same_day_records", same_day, stats["duration"]["same_day_records"])
    active = sum(1 for _, b, e, _ in valid if b <= PULL <= e)
    check("active_on_pull_date", active, stats["snapshot"]["active_on_pull_date_records"])

    for y in (2018, 2020, 2021):
        sub = [(r, d) for r, b, e, d in valid if b.year == y]
        known = sum(1 for r, _ in sub if r["PURPOSE"])
        check(f"purpose_known_{y}", known, stats["vintage_break_by_year"][str(y)]["purpose_known"])

    v21 = [(r, d) for r, b, e, d in valid if b >= datetime(2021, 1, 1).date()]
    check("records_2021_plus", len(v21), stats["basis_2021_plus"]["records_2021_plus_valid"])
    purp = Counter()
    purp_sd = Counter()
    for r, d in v21:
        if r["PURPOSE"]:
            purp[r["PURPOSE"]] += 1
            purp_sd[r["PURPOSE"]] += d
    top = purp_sd.most_common(1)[0]
    theirs = stats["purpose_2021_plus_by_segment_days"][0]
    check("top_purpose_by_segment_days", top[0], theirs["purpose"])
    check("top_purpose_segment_days", top[1], theirs["segment_days"])
    check("top_purpose_records", purp[top[0]], theirs["records"])

    streets = Counter()
    street_sd = Counter()
    for r, b, e, d in valid:
        streets[r["STREET"]] += 1
        street_sd[r["STREET"]] += d
    check("top_street_by_segment_days", street_sd.most_common(1)[0][0],
          stats["streets_top_by_segment_days"][0]["street"])
    check("top_street_segment_days", street_sd.most_common(1)[0][1],
          stats["streets_top_by_segment_days"][0]["segment_days"])

    out = {"checks": checks, "all_pass": all(c["pass"] for c in checks)}
    (DATA / "verify_independent_output.json").write_text(json.dumps(out, indent=1))
    print("ALL PASS" if out["all_pass"] else "SOME CHECKS FAILED")


if __name__ == "__main__":
    main()
