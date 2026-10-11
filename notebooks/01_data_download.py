# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 01 — Data download
#
# This chain tests one finding of the **Logroño flood-adaptation scenarios** analysis
# (Fouilloux 2026, release **v0.1.0**, Zenodo
# [10.5281/zenodo.23298913](https://doi.org/10.5281/zenodo.23298913)). That analysis
# computes building-level pluvial flood risk for every REACHOUT scenario; its archived
# release contains the code, the result tables and the figures.
#
# By default this notebook downloads the release (checked against the MD5 Zenodo
# publishes) and uses its **committed result tables**: each number in this chain then
# traces to an archived, citable set of results. Set `RERUN_ANALYSIS = True` to run the
# analysis pipeline itself first (about 45 minutes, its own pinned environment; without
# DestinE credentials its Climate DT step shows its committed results) and use the
# tables it produces instead.
#
# The map of where the planned scenario changes the water (04) needs the flood depths
# themselves, so the REACHOUT archive (Staccione and Pal, Zenodo
# [10.5281/zenodo.14035876](https://doi.org/10.5281/zenodo.14035876), CC BY 4.0, 254 MB)
# is downloaded too, checked against Zenodo's MD5; its rasters are read in place, never
# extracted.

# %%
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import time
import zipfile
from pathlib import Path

import requests

# %%
RERUN_ANALYSIS = False

RAW_DIR = Path("../data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)
ANALYSIS = {
    "name": "logrono-flood-adaptation-scenarios",
    "version": "v0.1.0",
    "doi": "10.5281/zenodo.23298913",
    "concept_doi": "10.5281/zenodo.23298912",
    "record": "23298913",
    "file": "annefou/logrono-flood-adaptation-scenarios-v0.1.0.zip",
    "license": "MIT (code); data under their own licences",
}
ANALYSIS_DIR = RAW_DIR / "analysis"
HEADERS = {"User-Agent": "logrono-planned-nbs-flood-risk (+https://github.com/annefou/logrono-planned-nbs-flood-risk)"}


def get(url: str, attempts: int = 6, **kw) -> requests.Response:
    """GET with retries and growing back-off: Zenodo throttles and answers 504 / empty bodies."""
    for i in range(attempts):
        try:
            r = requests.get(url, timeout=600, headers=HEADERS, **kw)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            if i == attempts - 1:
                raise
            print(f"retry {i + 1} after: {str(e)[:120]}")
            time.sleep(30 * (i + 1))


def md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# %% [markdown]
# ## The analysis release

# %%
record = get(f"https://zenodo.org/api/records/{ANALYSIS['record']}").json()
entry = next(f for f in record["files"] if f["key"] == ANALYSIS["file"])
expected_md5 = entry["checksum"].removeprefix("md5:")
archive = RAW_DIR / Path(ANALYSIS["file"]).name
if not archive.exists() or md5(archive) != expected_md5:
    with get(entry["links"]["self"], stream=True) as r, open(archive, "wb") as f:
        shutil.copyfileobj(r.raw, f)
assert md5(archive) == expected_md5, "analysis archive does not match Zenodo's MD5"

if not (ANALYSIS_DIR / "Snakefile").exists():
    with zipfile.ZipFile(archive) as z:
        top = {n.split("/")[0] for n in z.namelist()}
        assert len(top) == 1, top
        z.extractall(RAW_DIR)
    (RAW_DIR / top.pop()).rename(ANALYSIS_DIR)
print(f"{archive.name}: MD5 {expected_md5} verified; extracted to {ANALYSIS_DIR}")

# %% [markdown]
# ## The REACHOUT flood maps

# %%
REACHOUT = {"record": "14035876", "doi": "10.5281/zenodo.14035876", "file": "PluvialFloodMap_Logrono.zip",
            "license": "CC-BY-4.0"}
reachout_entry = next(f for f in get(f"https://zenodo.org/api/records/{REACHOUT['record']}").json()["files"]
                      if f["key"] == REACHOUT["file"])
reachout_md5 = reachout_entry["checksum"].removeprefix("md5:")
reachout = RAW_DIR / REACHOUT["file"]
if not reachout.exists() or md5(reachout) != reachout_md5:
    with get(reachout_entry["links"]["self"], stream=True) as r, open(reachout, "wb") as f:
        shutil.copyfileobj(r.raw, f)
assert md5(reachout) == reachout_md5, "REACHOUT archive does not match Zenodo's MD5"
print(f"{reachout.name}: MD5 {reachout_md5} verified")

# %%
if RERUN_ANALYSIS:
    env = {k: v for k, v in os.environ.items() if not k.startswith(("PIXI_", "CONDA_"))}
    subprocess.run(["pixi", "run", "--manifest-path", "pixi.toml", "snakemake", "--cores", "1"],
                   cwd=ANALYSIS_DIR, env=env, check=True)
    print("analysis re-run: its result tables were regenerated")
else:
    print("using the result tables archived in the release")

# %% [markdown]
# ## Source log

# %%
log = {"accessed_on": datetime.date.today().isoformat(),
       "analysis": {**ANALYSIS, "md5": expected_md5, "path": str(ANALYSIS_DIR), "rerun": RERUN_ANALYSIS},
       "reachout": {**REACHOUT, "md5": reachout_md5, "path": str(reachout)}}
(RAW_DIR / "sources.json").write_text(json.dumps(log, indent=2, ensure_ascii=False))
print(f"logged to {RAW_DIR / 'sources.json'}")
