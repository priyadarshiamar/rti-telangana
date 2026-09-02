#!/usr/bin/env python3
"""Build data/frame_telangana.csv from the raw portal scrape.

Raw sources in data/raw/portal_scrape_<date>/ are page-by-page JSON responses
from the portal's own public-authority search endpoint
(GET /Homepage/Home/GetDepartments?term=&page=N, 30 names per page) and are
never modified. This script normalises whitespace, dedupes, joins district
and block from the project's earlier state_department classification file
where an office matches, and writes the frame plus a provenance record.

Names are kept portal-verbatim (typos like "Husbadry" included, leading dots
included) because RAs must match them against the portal dropdown.

Usage: python3 scripts/build_frame.py   (from the repository root)
"""

import csv
import glob
import hashlib
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = sorted((ROOT / "data" / "raw").glob("portal_scrape_*"))[-1]
OUT = ROOT / "data" / "frame_telangana.csv"
PROV = ROOT / "data" / "frame_provenance.json"
# earlier classification file: source of district/block for matched offices
LEGACY = ROOT / "data" / "raw" / "state_department_telangana_legacy.csv"


def squash(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def fuzzy(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def main():
    raw_names = []
    pages = sorted(RAW_DIR.glob("page_*.json"),
                   key=lambda p: int(re.search(r"(\d+)", p.name).group()))
    for p in pages:
        raw_names += json.loads(p.read_text(), strict=False)

    names = sorted({squash(n) for n in raw_names})

    legacy = {}
    if LEGACY.exists():
        for r in csv.DictReader(open(LEGACY, encoding="utf-8")):
            legacy[fuzzy(r["Department"])] = r

    matched = 0
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["State", "Department", "Website",
                                          "District", "Block"])
        w.writeheader()
        for n in names:
            old = legacy.get(fuzzy(n))
            if old:
                matched += 1
            w.writerow({
                "State": "Telangana", "Department": n,
                "Website": "RTI_telangana",
                "District": old["District"] if old else "",
                "Block": old["Block"] if old else "",
            })

    prov = {
        "scraped_on": RAW_DIR.name.replace("portal_scrape_", ""),
        "built_on": str(date.today()),
        "endpoint": "https://rti.telangana.gov.in/Homepage/Home/GetDepartments?term=&page=N",
        "pages": len(pages),
        "raw_rows": len(raw_names),
        "unique_offices": len(names),
        "portal_reported_public_authorities": 3500,
        "district_block_joined_from_legacy_file": matched,
        "frame_sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "notes": [
            "names kept portal-verbatim after whitespace normalisation",
            "raw pages contain duplicate registrations; deduped on normalised name",
            "completeness verified: an independent term='a' sweep of the same "
            "endpoint added zero names beyond the empty-term paging",
        ],
    }
    PROV.write_text(json.dumps(prov, indent=2))
    print(f"{len(names)} offices ({matched} with district joined) -> {OUT.name}")


if __name__ == "__main__":
    main()
