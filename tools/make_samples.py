"""Build the small samples in data/ from the full dataset folder.

Usage: python tools/make_samples.py /path/to/city-brain-datasets

Only datasets whose licence allows redistribution get a sample. UTD19, the two
IEEE DataPort sets, the Kaggle smoke set and the Fire & Smoke Twin calls do not;
their notebooks explain how to download them.
"""

from __future__ import annotations

import csv
import gzip
import io
import shutil
import sys
import zipfile
from pathlib import Path

SRC = Path(sys.argv[1])
OUT = Path(__file__).resolve().parents[1] / "data"


def copy(rel: str, dest: str | None = None) -> None:
    src, dst = SRC / rel, OUT / (dest or rel)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        shutil.copy2(src, dst)


def gz_filter(rel: str, dest: str, keep, header: bool = True, sep: str = ",") -> None:
    """Copy the rows of a text file for which keep(row) is true, gzipped."""
    dst = OUT / dest
    dst.parent.mkdir(parents=True, exist_ok=True)
    src = SRC / rel
    opener = gzip.open if src.suffix == ".gz" else open
    with opener(src, "rt", encoding="utf-8", errors="replace") as f, gzip.open(dst, "wt", encoding="utf-8") as g:
        for i, line in enumerate(f):
            if (header and i == 0) or keep(line.rstrip("\n").split(sep)):
                g.write(line)


# NYC Open Data, USGS: open / public domain.
copy("flood/floodnet/events.csv")
copy("flood/floodnet/sensors.csv")
copy("flood/usgs-raritan/raritan_2021.rdb")
copy("calls/nyc-311")
copy("accidents/nyc-collisions")
copy("traffic/nyc-dot-speeds")

# DOE Eagle-I (CC BY 4.0): NY + NJ, 15 Aug - 15 Sep 2021 only.
gz_filter("power/eaglei-outages/nynj_2021.csv", "power/eaglei-outages/nynj_aug_sep_2021.csv.gz",
          lambda r: "2021-08-15" <= r[-1][:10] <= "2021-09-15")

# EPA AirNow (public): New York and New Jersey agencies only.
gz_filter("air-quality/airnow-smoke/pm25_jun2023.dat", "air-quality/airnow-smoke/pm25_jun2023_nynj.dat.gz",
          lambda r: len(r) > 8 and ("New York" in r[8] or "New Jersey" in r[8]), header=False, sep="|")

# UCI ElectricityLoadDiagrams (CC BY 4.0): 2013 only, aggregate of all clients + 6 clients.
CLIENTS = ["MT_010", "MT_100", "MT_200", "MT_300", "MT_362", "MT_124"]
dst = OUT / "power/uci-load/uci_2013_sample.csv.gz"
dst.parent.mkdir(parents=True, exist_ok=True)
with open(SRC / "power/uci-load/LD2011_2014.txt", encoding="utf-8") as f, gzip.open(dst, "wt") as g:
    head = [h.strip('"') for h in f.readline().rstrip("\n").split(";")]
    idx = [head.index(c) for c in CLIENTS]
    g.write("timestamp,aggregate_kw," + ",".join(CLIENTS) + "\n")
    for line in f:
        if not line.startswith('"2013'):
            continue
        p = line.rstrip("\n").split(";")
        vals = [float(x.replace(",", ".")) for x in p[1:]]
        g.write(f"{p[0].strip(chr(34))},{sum(vals):.1f}," + ",".join(f"{vals[i - 1]:.3f}" for i in idx) + "\n")

# FARS 2024 (US government, public): accident table with the columns we use.
COLS = ["ST_CASE", "STATENAME", "MONTH", "DAY_WEEK", "HOUR", "MINUTE", "RUR_URBNAME", "FUNC_SYSNAME",
        "LATITUDE", "LONGITUD", "HARM_EVNAME", "MAN_COLLNAME", "LGT_CONDNAME", "WEATHERNAME",
        "NOT_HOUR", "NOT_MIN", "ARR_HOUR", "ARR_MIN", "HOSP_HR", "HOSP_MN", "PERSONS", "FATALS"]
with zipfile.ZipFile(SRC / "accidents/fars-2024/FARS2024NationalCSV.zip") as z:
    name = next(n for n in z.namelist() if n.endswith("/accident.csv"))
    rows = csv.DictReader(io.TextIOWrapper(z.open(name), encoding="latin-1"))
    dst = OUT / "accidents/fars-2024/accident_2024_sample.csv.gz"
    dst.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(dst, "wt", newline="") as g:
        w = csv.DictWriter(g, COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

# Intel Berkeley Lab (open): 8 motes, all readings.
MOTES = {"1", "2", "7", "13", "22", "31", "40", "49"}
gz_filter("sensor-faults/intel-lab/data.txt.gz", "sensor-faults/intel-lab/intel_8motes.txt.gz",
          lambda r: len(r) > 3 and r[3] in MOTES, header=False, sep=" ")
copy("sensor-faults/intel-lab/mote_locs.txt")

# NAB (MIT licence): the series we use + labels.
for d in ("realTraffic", "artificialNoAnomaly", "realKnownCause"):
    copy(f"anomaly-benchmark/nab/data/{d}")
copy("anomaly-benchmark/nab/labels/combined_windows.json")
copy("anomaly-benchmark/nab/LICENSE.txt")

# NIST smoke alarm data (US government, public domain): room tests + summary workbook.
copy("fire/nist-smoke-alarms/Room Data", "fire/nist-smoke-alarms/room")
copy("fire/nist-smoke-alarms/summary_nistsmokebox_roomresults.xlsx")

total = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
print(f"samples written to {OUT}: {total / 1e6:.1f} MB")
