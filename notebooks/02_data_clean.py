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
# # 02 — The inputs of this finding
#
# From the analysis release (01), for the three land covers this finding compares —
# REACHOUT's `Baseline` (current green cover), `NBSplanned` and `NBSplanned_plus` (the
# planned scenario, without and with the extra ponds and rain gardens) — under the same
# rainfall (present, future median, future 90th percentile):
#
# | Table | From the analysis's `results/` | Content |
# |---|---|---|
# | `at_risk.csv` | `building_risk.parquet` | residents and buildings at risk (either risk index above zero, and each risk) per land cover, climate and return period |
# | `hazard_changed.csv` | `scenario_summary.csv` | residential buildings whose hazard differs from the current green cover |
# | `cells.csv` | `hazard_cell_changes.csv` | flood-map cells that get shallower or deeper, and stored water volume |
# | `places.csv` | `impact_places_local_depth.csv` | water depth on and around the places where recorded storms caused flooding |
# | `maps.csv` | `reachout_inventory.csv` | which maps exist, with their design rainfall |
#
# REACHOUT describes the scenarios (Zenodo 10.5281/zenodo.14035876): *"NBS planned:
# baseline + additional 4 bioswales/ponds (= 29,850 m3) and a green corridor (5.3 km x
# 5 m) in the southern part of the city"*; *"NBS planned plus: NBS planned scenarios +
# additional small ponds/rain gardens (depth 0.5 m, 13,500 m3)"*.

# %%
import json
from pathlib import Path

import pandas as pd

RAW = Path("../data/raw")
ANALYSIS = Path(json.loads((RAW / "sources.json").read_text())["analysis"]["path"])
RESULTS_A = ANALYSIS / "results"
CLEAN = Path("../data/clean")
CLEAN.mkdir(parents=True, exist_ok=True)
LAND_COVERS = ["Baseline", "NBSplanned", "NBSplanned_plus"]

# %%
risk = pd.read_parquet(RESULTS_A / "building_risk.parquet", filters=[("variant", "==", "counts")])
risk = risk[risk["land_cover"].isin(LAND_COVERS)]
rows = []
for (lc, climate, rp), g in risk.groupby(["land_cover", "climate", "rp"]):
    either = (g["PFRWB"] > 0) | (g["PFRMA"] > 0)
    for name, mask in {"either": either, "PFRWB": g["PFRWB"] > 0, "PFRMA": g["PFRMA"] > 0}.items():
        rows.append({"land_cover": lc, "climate": climate, "rp": rp, "risk": name,
                     "buildings_at_risk": int(mask.sum()), "residents_at_risk": float(g.loc[mask, "R"].sum())})
at_risk = pd.DataFrame(rows)
at_risk.to_csv(CLEAN / "at_risk.csv", index=False)
print(at_risk[at_risk["risk"] == "either"].pivot_table(index=["land_cover", "climate"], columns="rp",
                                                         values="residents_at_risk").round(0).to_string())

# %%
summary = pd.read_csv(RESULTS_A / "scenario_summary.csv")
summary = summary[(summary["variant"] == "counts") & summary["land_cover"].isin(LAND_COVERS)]
summary[["land_cover", "climate", "rp", "risk", "buildings_hazard_changed", "residents_hazard_changed"]].to_csv(
    CLEAN / "hazard_changed.csv", index=False)

cells = pd.read_csv(RESULTS_A / "hazard_cell_changes.csv")
cells[cells["land_cover"].isin(LAND_COVERS)].to_csv(CLEAN / "cells.csv", index=False)

places = pd.read_csv(RESULTS_A / "impact_places_local_depth.csv")
places[places["land_cover"].isin(LAND_COVERS)].to_csv(CLEAN / "places.csv", index=False)

inventory = pd.read_csv(RESULTS_A / "reachout_inventory.csv")
maps = inventory[inventory["land_cover"].isin(LAND_COVERS)][["land_cover", "climate", "rp", "status", "rain_mm", "published_mm"]]
maps.to_csv(CLEAN / "maps.csv", index=False)
print(maps[maps["status"] != "ok"].to_string(index=False))
