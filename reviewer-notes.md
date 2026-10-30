# Reviewer notes - Denver street occupancy permits brief (2026-10-30)

Package state: built in full during the 2026-10-30 morning run (the
October 29 evening pick was recorded in leads_log.md, but no
overnight package existed at run start; the run built it). Brief,
stats, charts, hero, audit, and independent verification are final
and in sync; Section 10 audit PASSED after a one-item fix loop
(EXEMPT adjudication, recorded in verification.md); independent
verifier reproduced all 19 of its checks exactly. Hero composited
from the generated illustration and inspected - headline "34.6%"
legible on the clean dark top field, scene intact.

## Claims most likely to be challenged

1. "Segment-days" is this brief's own constructed measure (records x
   permitted duration). The brief defines it in the opening, states
   everywhere that it measures permitted time rather than observed
   closure, and prints the strongest alternative (permitted windows
   cover scheduling slack; standing uses are mixed with work permits)
   in What this might mean. A challenger can dispute the measure's
   meaning but not its arithmetic: the audit asserts the partitions
   close exactly.
2. The duration definition counts a same-day permit as 0 days, so
   the 39,933 same-day records (15.4 percent) contribute nothing to
   segment-days. An inclusive count (end minus begin plus one) would
   raise the total and lower the over-90 share slightly. The
   definition is printed in the data notes, and the same-day count
   is printed with it so a reader can recompute either way.
3. Finding 9's street-name join merges directional variants and
   street-type namesakes under normalization (16TH ST and 16TH AVE
   both become 16TH), and intersection crashes count for both
   streets. The brief publishes only aggregate mention shares on
   that basis, names the merged Colfax and Broadway groups as
   groups, and prints the rejected first-leg method's Broadway
   failure (2 crashes) as the reason per-street crash figures are
   not published. This is the package's softest join and it is
   fenced accordingly.
4. The 2021+ basis for purpose and company will read as a choice; it
   is a measured constraint (purpose known on 1 of 9,771 records in
   2018). The vintage table is printed in Finding 3 so the basis
   cannot be mistaken for a preference.
5. 16TH ST's mean duration (42.8 days against a median of 3) rests
   partly on one joint program string (CCD (CPM Trans) & PCL, 378 of
   1,200 records). The brief names the string and the count rather
   than attributing the street's total to the program alone.

## Dataset-quality items, and whom they reflect on (Section 11.3)

- PURPOSE and COMPANY are unpopulated for essentially all permits
  beginning before 2021 in a register DOTI maintains and DenverGIS
  publishes; the layer's documentation does not explain the gap.
  The brief reports the population pattern, assigns no cause, and
  addresses the fix (document or backfill; add a holder identifier)
  to DOTI and the open data program in Who can act. This touches a
  named department, so it is flagged here for extra care; the
  brief's language stays at the published record's contents.
- The raw date fields carry sentinel and erroneous values (begins in
  1902 and 2901, ends in 2099, 83 records ending before they begin).
  Reported as counted facts with the window rules printed; no claim
  about how the values entered the system.
- EXEMPT's server-side grouping does not reproduce its local counter
  (adjudicated in the audit). No figure uses EXEMPT.

## Checks not completed

- Observed occupancy: no source records actual closure or reopening,
  so permitted time is the only duration the record supports. This
  is the brief's governing limit, printed in the opening definitions
  and in What this might mean.
- Per-intersection or per-street-mile occupancy: the layer's stored
  point is present on 25.6 percent of records with a year-varying
  pattern, and no network join was attempted; street figures are
  name groups, not measured street segments.
- Crash-fusion recomputation by the stdlib verifier: the crash panel
  is parquet, which the standard library cannot read, so Finding 9
  rests on the audit's two-method comparison and worked example
  (see verification-ledger-independent.md).
- No field verification of any individual permit, segment, or street
  was performed; the two future records with an end date a year
  before their begin date are reported as printed in the register.

## Surprises worth knowing

- The server count moved between the evening lead verification
  (259,891 on October 29) and the morning pull (260,061), and the
  service's last-edit timestamp is October 30, 04:45 MDT - the
  register was reprocessed hours before the pull. All figures are
  stamped to the pull.
- Bike Parking is a top-8 purpose by segment-days (76,881) on 121
  records with a median duration of 585 days: standing micromobility
  corrals sit in the same register and the same duration measure as
  three-day utility cuts.
- The active-on-pull-date count (631 segment records) is small next
  to the register's size, and 185 of the 631 are long records - on
  any given day, the street-level footprint of the program is
  dominated by its long cohort even more than the segment-day totals
  suggest.
- Crash mentions concentrate on Colfax (4,387) at roughly double
  Broadway (2,434), while their occupancy segment-days are similar
  in scale - the clearest single-street illustration of Finding 9's
  aggregate result.
