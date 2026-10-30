"""Build stats.json and the street panel for the Denver street
occupancy permits brief (2026-10-30).

Unit of observation: one row of ODC_DEV_STREETOCCUPANCYPPERMITS_L is
one permit-segment record. The service description states a single
permit may encompass multiple closures across several street segments
and affect different portions of the street, so rows are never called
permits and permits are never called closures.

Dates: BEGIN_DATE / END_DATE arrive as epoch milliseconds (UTC).
They are converted to America/Denver calendar dates. Duration is
END minus BEGIN in calendar days. A segment-day is one segment record
times one day of its duration.

Analysis window (duration-valid records): BEGIN_DATE between
2017-01-01 and the pull date 2026-10-30 inclusive, END_DATE present,
END >= BEGIN, END <= 2027-12-31. Every exclusion is counted in
stats.json under date_classes.

PURPOSE and COMPANY are populated on essentially no 2018-2019 records
(a vintage break in the register, measured in this build), so purpose
and company tables use the 2021+ valid records as their population
and state that basis wherever they are used.
"""
import json, pathlib, re
from collections import Counter

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent.parent
DATA = HERE / "data"
PULL_DATE = pd.Timestamp("2026-10-30")
WIN_START = pd.Timestamp("2017-01-01")
END_CAP = pd.Timestamp("2027-12-31")


def local_dates(s):
    return (pd.to_datetime(s, unit="ms", errors="coerce", utc=True)
            .dt.tz_convert("America/Denver").dt.normalize().dt.tz_localize(None))


def pct(n, d, nd=1):
    return round(100.0 * n / d, nd) if d else None


def main():
    df = pd.read_parquet(DATA / "permits_raw.parquet")
    raw_n = len(df)
    df["b"] = local_dates(df["BEGIN_DATE"])
    df["e"] = local_dates(df["END_DATE"])

    # ---- date classes (raw) ----
    dc = {}
    dc["rows_total"] = raw_n
    dc["begin_null"] = int(df["b"].isna().sum())
    dc["end_null"] = int(df["e"].isna().sum())
    dc["begin_before_2017"] = int((df["b"] < WIN_START).sum())
    dc["begin_after_pull"] = int((df["b"] > PULL_DATE).sum())
    dc["end_before_begin_raw"] = int((df["e"] < df["b"]).sum())
    fut = df[df["b"] > PULL_DATE]
    dc["future_scheduled_valid"] = int(((fut["b"] <= END_CAP) & (fut["e"] >= fut["b"])
                                        & (fut["e"] <= END_CAP)).sum())
    dc["begin_after_2027"] = int((df["b"] > END_CAP).sum())
    inwin = df[(df["b"] >= WIN_START) & (df["b"] <= PULL_DATE)]
    dc["in_window_begin"] = int(len(inwin))
    dc["in_window_end_before_begin"] = int((inwin["e"] < inwin["b"]).sum())
    dc["in_window_end_after_cap"] = int((inwin["e"] > END_CAP).sum())
    dc["in_window_end_null"] = int(inwin["e"].isna().sum())

    valid = inwin[(inwin["e"] >= inwin["b"]) & (inwin["e"] <= END_CAP)].copy()
    valid["dur"] = (valid["e"] - valid["b"]).dt.days
    assert len(valid) + dc["in_window_end_before_begin"] + dc["in_window_end_after_cap"] \
        + dc["in_window_end_null"] == len(inwin)
    dc["valid_records"] = int(len(valid))
    dc["excluded_from_window_total"] = raw_n - len(valid)

    s = {"pull_date": "2026-10-30", "date_classes": dc}

    # ---- register composition ----
    comp = {}
    comp["distinct_permit_numbers"] = int(df["PERMIT_NUMBER"].nunique(dropna=True))
    comp["permit_number_null"] = int(df["PERMIT_NUMBER"].isna().sum())
    rows_per = df.groupby(df["PERMIT_NUMBER"].fillna("<null>")).size()
    comp["rows_per_permit_median"] = float(rows_per.median())
    comp["rows_per_permit_max"] = int(rows_per.max())
    comp["permits_with_one_row"] = int((rows_per == 1).sum())
    comp["permits_with_one_row_share_pct"] = pct(int((rows_per == 1).sum()), len(rows_per))
    comp["segment_length_total_ft_all_rows"] = float(df["Shape__Length"].sum())
    comp["segment_length_total_miles_all_rows"] = round(float(df["Shape__Length"].sum()) / 5280, 1)
    comp["xy_present_rows"] = int(df["X_COORD"].notna().sum())
    comp["xy_present_share_pct"] = pct(int(df["X_COORD"].notna().sum()), raw_n)
    comp["gis_load_type_counter"] = Counter(df["GIS_LOAD_TYPE"].fillna("<null>")).most_common()
    s["register"] = comp

    # ---- vintage break: purpose/company population by begin year ----
    vb = {}
    for y in range(2018, 2027):
        sub = valid[valid["b"].dt.year == y]
        vb[str(y)] = {
            "records": int(len(sub)),
            "purpose_known": int(sub["PURPOSE"].notna().sum()),
            "purpose_known_share_pct": pct(int(sub["PURPOSE"].notna().sum()), len(sub)),
            "company_known": int(sub["COMPANY"].notna().sum()),
            "company_known_share_pct": pct(int(sub["COMPANY"].notna().sum()), len(sub)),
        }
    s["vintage_break_by_year"] = vb
    both_null = valid[valid["PURPOSE"].isna() & valid["COMPANY"].isna()]
    s["purpose_and_company_both_null_valid"] = int(len(both_null))

    # ---- duration and segment-days (valid window) ----
    d = {}
    d["total_segment_days"] = int(valid["dur"].sum())
    d["median_days"] = float(valid["dur"].median())
    d["mean_days"] = round(float(valid["dur"].mean()), 2)
    d["p75_days"] = float(valid["dur"].quantile(0.75))
    d["p90_days"] = float(valid["dur"].quantile(0.90))
    d["p99_days"] = float(valid["dur"].quantile(0.99))
    d["max_days"] = int(valid["dur"].max())
    d["same_day_records"] = int((valid["dur"] == 0).sum())
    d["same_day_share_pct"] = pct(int((valid["dur"] == 0).sum()), len(valid))
    bands = [(0, 0, "0 days"), (1, 7, "1-7 days"), (8, 30, "8-30 days"),
             (31, 90, "31-90 days"), (91, 365, "91-365 days"), (366, 10**9, "over 365 days")]
    d["duration_bands"] = []
    for lo, hi, label in bands:
        sub = valid[(valid["dur"] >= lo) & (valid["dur"] <= hi)]
        d["duration_bands"].append({
            "band": label, "records": int(len(sub)),
            "record_share_pct": pct(len(sub), len(valid)),
            "segment_days": int(sub["dur"].sum()),
            "segment_day_share_pct": pct(int(sub["dur"].sum()), int(valid["dur"].sum())),
        })
    over90 = valid[valid["dur"] > 90]
    d["over_90_records"] = int(len(over90))
    d["over_90_record_share_pct"] = pct(len(over90), len(valid), 2)
    d["over_90_segment_days"] = int(over90["dur"].sum())
    d["over_90_segment_day_share_pct"] = pct(int(over90["dur"].sum()), int(valid["dur"].sum()))
    over365 = valid[valid["dur"] > 365]
    d["over_365_records"] = int(len(over365))
    d["over_365_segment_days"] = int(over365["dur"].sum())
    d["over_365_segment_day_share_pct"] = pct(int(over365["dur"].sum()), int(valid["dur"].sum()))
    d["foot_days_total"] = float((valid["dur"] * valid["Shape__Length"]).sum())
    d["by_begin_year"] = {}
    for y, sub in valid.groupby(valid["b"].dt.year):
        d["by_begin_year"][str(int(y))] = {
            "records": int(len(sub)), "segment_days": int(sub["dur"].sum()),
            "median_days": float(sub["dur"].median()),
        }
    s["duration"] = d

    # ---- snapshot: active on pull date, and future ----
    act = valid[(valid["b"] <= PULL_DATE) & (valid["e"] >= PULL_DATE)]
    s["snapshot"] = {
        "active_on_pull_date_records": int(len(act)),
        "active_median_duration_days": float(act["dur"].median()),
        "active_over_90_share_records": int((act["dur"] > 90).sum()),
        "active_top_purposes": Counter(act["PURPOSE"].fillna("<null>")).most_common(5),
        "active_top_companies": Counter(act["COMPANY"].fillna("<null>")).most_common(5),
        "future_scheduled_valid_records": dc["future_scheduled_valid"],
    }

    # ---- purpose and company, 2021+ basis ----
    v21 = valid[valid["b"] >= "2021-01-01"].copy()
    basis = {"records_2021_plus_valid": int(len(v21)),
             "purpose_known": int(v21["PURPOSE"].notna().sum()),
             "purpose_null": int(v21["PURPOSE"].isna().sum()),
             "company_known": int(v21["COMPANY"].notna().sum()),
             "company_null": int(v21["COMPANY"].isna().sum())}
    s["basis_2021_plus"] = basis
    pk = v21[v21["PURPOSE"].notna()]
    purp = []
    for name, sub in pk.groupby("PURPOSE"):
        purp.append({"purpose": name, "records": int(len(sub)),
                     "record_share_of_known_pct": pct(len(sub), len(pk)),
                     "segment_days": int(sub["dur"].sum()),
                     "segment_day_share_of_known_pct": pct(int(sub["dur"].sum()), int(pk["dur"].sum())),
                     "median_days": float(sub["dur"].median())})
    purp.sort(key=lambda r: -r["segment_days"])
    s["purpose_2021_plus_by_segment_days"] = purp
    purp_rec = sorted(purp, key=lambda r: -r["records"])
    s["purpose_2021_plus_by_records"] = purp_rec
    ck = v21[v21["COMPANY"].notna()]
    comp_rows = []
    for name, sub in ck.groupby("COMPANY"):
        comp_rows.append({"company": name, "records": int(len(sub)),
                          "segment_days": int(sub["dur"].sum()),
                          "median_days": float(sub["dur"].median())})
    s["company_2021_plus_top_by_records"] = sorted(comp_rows, key=lambda r: -r["records"])[:10]
    s["company_2021_plus_top_by_segment_days"] = sorted(comp_rows, key=lambda r: -r["segment_days"])[:10]
    s["company_distinct_strings_2021_plus"] = int(v21["COMPANY"].nunique(dropna=True))
    xc = v21[v21["COMPANY"].fillna("").str.contains("XCEL", case=False)]
    s["xcel_strings"] = {"distinct_strings_containing_xcel": int(xc["COMPANY"].nunique()),
                         "records": int(len(xc)), "segment_days": int(xc["dur"].sum()),
                         "top_strings": Counter(xc["COMPANY"]).most_common(3)}

    # ---- ASIT (portion of street), full valid window ----
    asit = []
    for name, sub in valid.groupby(valid["ASIT_TYPE"].fillna("<null>")):
        asit.append({"asit_type": name, "records": int(len(sub)),
                     "record_share_pct": pct(len(sub), len(valid)),
                     "segment_days": int(sub["dur"].sum()),
                     "segment_day_share_pct": pct(int(sub["dur"].sum()), int(valid["dur"].sum())),
                     "median_days": float(sub["dur"].median())})
    asit.sort(key=lambda r: -r["segment_days"])
    s["asit_by_segment_days"] = asit
    sw = valid[valid["ASIT_TYPE"].fillna("").str.startswith("Sidewalk")]
    s["sidewalk_classes"] = {"records": int(len(sw)), "segment_days": int(sw["dur"].sum()),
                             "segment_day_share_pct": pct(int(sw["dur"].sum()), int(valid["dur"].sum()))}
    full = valid[valid["ASIT_TYPE"].fillna("").str.contains("Full")]
    s["full_closure_classes"] = {"records": int(len(full)), "segment_days": int(full["dur"].sum()),
                                 "segment_day_share_pct": pct(int(full["dur"].sum()), int(valid["dur"].sum()))}

    # ---- streets (exact STREET values), valid window ----
    panel = (valid.groupby(valid["STREET"].fillna("<null>"))
             .agg(records=("dur", "size"), segment_days=("dur", "sum"),
                  median_days=("dur", "median"),
                  segment_ft=("Shape__Length", "sum"))
             .reset_index().rename(columns={"STREET": "street"}))
    panel["foot_days"] = (valid.groupby(valid["STREET"].fillna("<null>"))
                          .apply(lambda g: float((g["dur"] * g["Shape__Length"]).sum()), include_groups=False)
                          .values)
    panel = panel.sort_values("segment_days", ascending=False)
    panel.to_csv(DATA / "street_panel.csv", index=False)
    s["streets_top_by_segment_days"] = panel.head(10).to_dict("records")
    s["streets_top_by_foot_days"] = panel.sort_values("foot_days", ascending=False).head(5).to_dict("records")
    s["distinct_street_values"] = int(valid["STREET"].nunique(dropna=True))
    top10_share = float(panel.head(10)["segment_days"].sum() / valid["dur"].sum() * 100)
    s["top10_streets_segment_day_share_pct"] = round(top10_share, 1)
    mall = valid[valid["STREET"] == "16TH ST"]
    s["street_16th"] = {"records": int(len(mall)), "segment_days": int(mall["dur"].sum()),
                        "median_days": float(mall["dur"].median()),
                        "mean_days": round(float(mall["dur"].mean()), 1),
                        "top_company": Counter(mall["COMPANY"].fillna("<null>")).most_common(1),
                        "top_company_records_share_note": "CCD (CPM Trans) & PCL records in the full pull"}

    # ---- crash fusion (street-name mentions, both legs) ----
    crash = pd.read_parquet(HERE.parent / "stack" / "denver" / "layers" / "traffic_accidents_clean.parquet")
    SUF = {"ST", "AVE", "BLVD", "DR", "RD", "PKWY", "HWY", "CT", "LN", "PL", "CIR", "WAY"}

    def norm(name):
        if not isinstance(name, str):
            return None
        t = re.sub(r"^(N|S|E|W)\s+", "", name.strip().upper())
        parts = t.split()
        if parts and parts[-1] in SUF:
            parts = parts[:-1]
        return " ".join(parts)

    valid["sn"] = valid["STREET"].map(norm)
    occ_names = set(valid["sn"].dropna())

    def legs(addr):
        if not isinstance(addr, str):
            return []
        a = addr.strip().upper()
        if " BLOCK " in a:
            return [a.split(" BLOCK ", 1)[1].strip()]
        return [p.strip() for p in a.split(" / ")]

    crash["leg_norms"] = crash["incident_address"].map(lambda a: [norm(x) for x in legs(a)])
    crash["matched"] = crash["leg_norms"].map(lambda ls: any(x in occ_names for x in ls))
    mentions = Counter()
    ksi_mentions = Counter()
    for ls, k in zip(crash["leg_norms"], crash["ksi_crash_count_basis"]):
        for x in set(ls):
            if x in occ_names:
                mentions[x] += 1
                ksi_mentions[x] += int(bool(k))
    v21n = valid[valid["b"] >= "2021-01-01"]
    top10n = v21n.groupby("sn")["dur"].sum().sort_values(ascending=False).head(10)
    fu = {
        "crash_panel_records": int(len(crash)),
        "crashes_naming_a_register_street": int(crash["matched"].sum()),
        "match_share_pct": pct(int(crash["matched"].sum()), len(crash)),
        "total_street_mentions": int(sum(mentions.values())),
        "top10_occupancy_streets_segment_day_share_2021_plus_pct": round(float(top10n.sum() / v21n["dur"].sum() * 100), 1),
        "top10_crash_mentions": int(sum(mentions[x] for x in top10n.index)),
        "top10_crash_mention_share_pct": round(100.0 * sum(mentions[x] for x in top10n.index) / sum(mentions.values()), 1),
        "ksi_share_top10_mentions_pct": round(100.0 * sum(ksi_mentions[x] for x in top10n.index) / sum(mentions[x] for x in top10n.index), 2),
        "ksi_share_all_mentions_pct": round(100.0 * sum(ksi_mentions.values()) / sum(mentions.values()), 2),
        "colfax_mentions": int(mentions["COLFAX"]), "colfax_ksi": int(ksi_mentions["COLFAX"]),
        "broadway_mentions": int(mentions["BROADWAY"]), "broadway_ksi": int(ksi_mentions["BROADWAY"]),
        "first_leg_only_match_share_pct_note": "see verification.md polarity sample",
    }
    s["crash_fusion"] = fu

    (HERE / "stats.json").write_text(json.dumps(s, indent=1))
    print(json.dumps({"valid": len(valid), "segment_days": d["total_segment_days"],
                      "over90_share": d["over_90_segment_day_share_pct"]}, indent=1))


if __name__ == "__main__":
    main()
