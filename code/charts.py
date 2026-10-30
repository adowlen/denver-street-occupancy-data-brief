"""Data charts for the Denver street occupancy brief. Brand palette:
dark charcoal background, amber + teal, white text. Every chart labels
its scope and basis on the graphic itself. All figures come from
stats.json; no figure from a different scope or basis is juxtaposed
without its label printed on the graphic.
"""
import json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = pathlib.Path(__file__).resolve().parent.parent
s = json.loads((root / "stats.json").read_text())
BG, AMBER, TEAL, FG = "#1c1c1e", "#e8a33d", "#2a9d8f", "#f2f2f2"
plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG,
                     "text.color": FG, "axes.labelcolor": FG,
                     "xtick.color": FG, "ytick.color": FG,
                     "axes.edgecolor": "#555555", "font.size": 10})

# 1. Segment-days by begin year (valid window)
yrs = [y for y in s["duration"]["by_begin_year"] if y != "2017"]
vals = [s["duration"]["by_begin_year"][y]["segment_days"] for y in yrs]
recs = [s["duration"]["by_begin_year"][y]["records"] for y in yrs]
fig, ax = plt.subplots(figsize=(8.6, 5.0))
ax.bar(yrs, vals, color=TEAL)
for i, (v, r) in enumerate(zip(vals, recs)):
    ax.text(i, v + 9000, f"{v:,}\n({r:,} records)", ha="center", fontsize=7.8)
ax.set_ylim(0, 430000)
ax.set_ylabel("Segment-days (segment records x duration in days)")
ax.set_xlabel("Permit begin year (2026 is partial: Jan 1 to Oct 30, 2026)")
ax.set_title("Street occupancy segment-days by begin year\n"
             f"Scope: {s['date_classes']['valid_records']:,} duration-valid segment records in the window; "
             "2018-2026 charted (2017 adds 65 records and 1,176 segment-days), pulled Oct 30, 2026",
             loc="left", fontsize=10.5)
fig.tight_layout(); fig.savefig(root / "charts" / "chart_segment_days_by_year.png", dpi=200)
plt.close(fig)

# 2. Duration concentration: record share vs segment-day share by band
bands = s["duration"]["duration_bands"]
labels = [b["band"] for b in bands]
fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.8))
ax = axes[0]
vals = [b["record_share_pct"] for b in bands]
ax.barh(labels, vals, color="#888888")
ax.invert_yaxis()
for i, (v, b) in enumerate(zip(vals, bands)):
    ax.text(v + 1, i, f"{v}% ({b['records']:,})", va="center", fontsize=9)
ax.set_xlim(0, 72)
ax.set_title("Share of segment records", fontsize=10)
ax = axes[1]
vals = [b["segment_day_share_pct"] for b in bands]
ax.barh(labels, vals, color=AMBER)
ax.invert_yaxis()
for i, (v, b) in enumerate(zip(vals, bands)):
    ax.text(v + 0.7, i, f"{v}% ({b['segment_days']:,})", va="center", fontsize=9)
ax.set_xlim(0, 40)
ax.set_title("Share of segment-days", fontsize=10)
fig.suptitle("Duration concentration: most permits are short; most occupied time is not\n"
             f"Same population both panels: {s['date_classes']['valid_records']:,} duration-valid segment records, "
             f"{s['duration']['total_segment_days']:,} segment-days, 2017-2026 window",
             fontsize=10.5, x=0.02, ha="left")
fig.tight_layout(rect=[0, 0, 1, 0.90]); fig.savefig(root / "charts" / "chart_duration_concentration.png", dpi=200)
plt.close(fig)

# 3. Purpose by segment-days, 2021+ basis only (vintage break)
top = s["purpose_2021_plus_by_segment_days"][:8]
labels = [p["purpose"] for p in top][::-1]
vals = [p["segment_days"] for p in top][::-1]
meds = [p["median_days"] for p in top][::-1]
fig, ax = plt.subplots(figsize=(8.8, 5.2))
ax.barh(labels, vals, color=TEAL)
for i, (v, m) in enumerate(zip(vals, meds)):
    ax.text(v + 9000, i, f"{v:,}  (median {m:.0f} d)", va="center", fontsize=9)
ax.set_xlim(0, 580000)
ax.set_xlabel("Segment-days")
ax.set_title("Segment-days by permit purpose - 2021 and later permits only\n"
             f"Basis: {s['basis_2021_plus']['purpose_known']:,} records with a recorded purpose\n"
             f"(of {s['basis_2021_plus']['records_2021_plus_valid']:,} valid 2021+ records); purpose is blank on\n"
             "essentially all 2018-2019 records, so earlier years are excluded",
             loc="left", fontsize=10)
fig.tight_layout(); fig.savefig(root / "charts" / "chart_purpose_segment_days.png", dpi=200)
plt.close(fig)

# 4. Top streets by segment-days (exact STREET values)
top = s["streets_top_by_segment_days"][:10]
labels = [t["street"] for t in top][::-1]
vals = [t["segment_days"] for t in top][::-1]
recs = [t["records"] for t in top][::-1]
fig, ax = plt.subplots(figsize=(8.8, 5.2))
ax.barh(labels, vals, color=AMBER)
for i, (v, r) in enumerate(zip(vals, recs)):
    ax.text(v + 900, i, f"{v:,}  ({r:,} records)", va="center", fontsize=9)
ax.set_xlim(0, 68000)
ax.set_xlabel("Segment-days")
ax.set_title("Top 10 streets by occupancy segment-days (register's exact street names)\n"
             f"Scope: {s['date_classes']['valid_records']:,} duration-valid segment records, 2017-2026 window, "
             "pulled Oct 30, 2026",
             loc="left", fontsize=10)
fig.tight_layout(); fig.savefig(root / "charts" / "chart_top_streets_segment_days.png", dpi=200)
plt.close(fig)
print("charts done")
