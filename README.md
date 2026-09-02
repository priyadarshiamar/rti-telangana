# RTI Telangana

Reproducible sampling, RA assignments, and a tracking dashboard for filing
RTI applications to Telangana public authorities. This is the Telangana
extension of the Tamil Nadu pipeline in
[in-rolls/rti](https://github.com/in-rolls/rti) (branch
`restructure-pipeline`), whose design it follows: a frozen frame, one seeded
draw, randomized treatment assignment, balanced RA worklists, and a static
GitHub Pages viewer.

**Dashboard:** https://priyadarshiamar.github.io/rti-telangana/

## The batch

Batch `tg2026q3_01`, seed `20260902`, draws **250** of the **3,325**
Telangana offices listed on the state RTI portal
([rti.telangana.gov.in](https://rti.telangana.gov.in)). The frame comes from
the project's `state_department` classification file (Telangana rows only);
its SHA-256 is frozen in `out/tg2026q3_01/batch_meta.json`.

The Telangana list is flat — no department/tier tree like Tamil Nadu's —
so stratification is by **department group**, derived from the office name
(text before the first comma or parenthesis, normalised). Allocation across
strata is proportional to stratum size with a floor of 1 and a cap of 15,
so every substantial department is represented and none dominates. Groups
with fewer than 5 offices are pooled into a single OTHER stratum.

Within the draw:

- **Treatment:** 175 plain letters, 75 legal-salience (70/30), assigned by
  seeded shuffle. The legal-salience letter is byte-identical to the plain
  one except for the pre-specified Section 7(1)/20 paragraph.
- **RAs:** RA1–RA4, balanced within treatment arm (63/63/62/62 overall,
  legal split 19/19/19/18).

Re-running `python3 scripts/sample.py` reproduces the batch byte-for-byte.
A new wave means a new `batch_id` **and** a new seed.

## What RAs do

1. Open the dashboard, download your worklist (`out/tg2026q3_01/worklists/`).
2. File each row on [rti.telangana.gov.in](https://rti.telangana.gov.in),
   choosing the row's `office_name` in the portal's Public Authority
   dropdown.
3. Paste the letter matching the row's `treatment` from
   `out/tg2026q3_01/templates/` (fill only the `[FILER ...]` placeholders;
   filer details are private and never committed here).
4. Record every attempt in the filing form — including offices that could
   not be filed to. The "could not file" rows preserve the denominator.

## Repository layout

```
config/batch.yaml        frozen batch design
data/frame_telangana.csv the 3,325-office Telangana frame
scripts/sample.py        the seeded draw (stdlib only, no dependencies)
out/tg2026q3_01/         assignments.csv, batch_meta.json, worklists/, templates/
docs/                    the GitHub Pages dashboard (copies of the above)
```

## Privacy

No filer names, addresses, emails, phone numbers, or evidence links are
committed. Letters contain placeholders. Filing records with personal
details live outside this repository.
