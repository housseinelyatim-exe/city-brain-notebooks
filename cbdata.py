"""Find dataset files for the notebooks.

Looks first in this repo's data/ folder (small samples), then in the folder named
by the CITY_BRAIN_DATA environment variable (the full downloads, same layout).
"""

from __future__ import annotations

import os
from pathlib import Path

REPO_DATA = Path(__file__).resolve().parent / "data"

DOWNLOAD = {
    "traffic/utd19": "UTD19: register at https://utd19.ethz.ch (free, academic use) and download utd19_u.csv, "
                     "detectors_public.csv, links.csv. The Torino extract is made in notebook 01.",
    "power/smartgrid-attack": "IEEE DataPort 'SmartGrid Cyber-Physical Attack Dataset' (DOI 10.21227/symr-bz19).",
    "fire/fire-incident-calls": "git clone https://github.com/UrbanInfoLab/FireIncidentData",
}


def path(rel: str) -> Path:
    """Return the path of a dataset file, sample first, full download second."""
    candidates = [REPO_DATA / rel]
    if os.environ.get("CITY_BRAIN_DATA"):
        candidates.append(Path(os.environ["CITY_BRAIN_DATA"]) / rel)
    for p in candidates:
        if p.exists():
            return p
    hint = next((v for k, v in DOWNLOAD.items() if rel.startswith(k)), "see the notebook header")
    raise FileNotFoundError(
        f"{rel} not found. This dataset is not redistributed in the repo. {hint} "
        "Then set CITY_BRAIN_DATA to the folder that contains it."
    )
