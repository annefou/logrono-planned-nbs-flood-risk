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
# # 03 — How much do the planned nature-based solutions reduce flood risk?
#
# The finding under test (AIDA): *the nature-based solutions of REACHOUT's planned scenario
# for Logroño reduce the number of residents in buildings at pluvial flood risk by less
# than 4 %, with no reduction during the 100- and 200-year storms.*
#
# Both versions of the planned scenario (without and with the extra ponds) are compared
# with the current green cover under the same rainfall, for every climate, return period
# and risk measure:
#
# 1. **Residents at risk**: the reduction, in residents and per cent.
# 2. **Which buildings change**: residential buildings whose hazard differs at all.
# 3. **The flood maps themselves**: cells getting shallower or deeper, stored water.
# 4. **Recorded impact places**: water on and around them.
#
# This notebook only measures.

# %%
import json
from pathlib import Path

import pandas as pd

CLEAN = Path("../data/clean")
RESULTS = Path("../results")
RESULTS.mkdir(parents=True, exist_ok=True)
NBS = ["NBSplanned", "NBSplanned_plus"]

at_risk = pd.read_csv(CLEAN / "at_risk.csv")
base = at_risk[at_risk["land_cover"] == "Baseline"].set_index(["climate", "rp", "risk"])

# %% [markdown]
# ## 1. Residents at risk, planned scenario against current green cover

# %%
rows = []
for lc in NBS:
    x = at_risk[at_risk["land_cover"] == lc].set_index(["climate", "rp", "risk"])
    b = base.reindex(x.index)
    rows.append(pd.DataFrame({"land_cover": lc, "residents_baseline": b["residents_at_risk"],
                              "residents_scenario": x["residents_at_risk"],
                              "reduction": b["residents_at_risk"] - x["residents_at_risk"],
                              "reduction_pct": 100 * (1 - x["residents_at_risk"] / b["residents_at_risk"]),
                              "buildings_reduction": b["buildings_at_risk"] - x["buildings_at_risk"]}).reset_index())
reduction = pd.concat(rows, ignore_index=True)
# Maps REACHOUT does not provide (missing or empty files) cannot be compared: recorded, then left out.
maps = pd.read_csv(CLEAN / "maps.csv")
not_available = maps[maps["land_cover"].isin(NBS) & (maps["status"] != "ok")][["land_cover", "climate", "rp", "status"]]
print("not available:", not_available.to_dict("records"))
reduction = reduction.dropna(subset=["residents_scenario"])
reduction.to_csv(RESULTS / "residents_at_risk_reduction.csv", index=False)
print(reduction[reduction["risk"] == "either"].pivot_table(index=["land_cover", "climate"], columns="rp",
                                                           values="reduction_pct").round(2).to_string())

# %% [markdown]
# ## 2. Residential buildings whose hazard changes at all
#
# The analysis compares every map with the **present-day** current-cover map of the same
# return period, so for future rainfall this count mixes the measures with the heavier
# rain; only present rainfall isolates the measures.

# %%
changed = pd.read_csv(CLEAN / "hazard_changed.csv")
changed = changed[changed["land_cover"].isin(NBS) & (changed["climate"] == "present")].pivot_table(
    index=["land_cover", "climate", "risk"], columns="rp", values="buildings_hazard_changed")
changed.to_csv(RESULTS / "buildings_hazard_changed.csv")
print(changed.to_string())

# %% [markdown]
# ## 3. The flood maps: cells and stored water against the current green cover
#
# Inside the area modelled by every scenario, water bodies included; 2 m cells. As in §2,
# only present rainfall isolates the measures.

# %%
cells = pd.read_csv(CLEAN / "cells.csv")
cells = cells[cells["land_cover"].isin(NBS) & (cells["climate"] == "present")][["land_cover", "climate", "rp", "cells_ge30", "cells_ge30_baseline",
                                              "cells_shallower", "cells_deeper", "volume_change_m3"]]
cells["area_shallower_ha"] = cells["cells_shallower"] * 4 / 1e4
cells["area_deeper_ha"] = cells["cells_deeper"] * 4 / 1e4
cells.to_csv(RESULTS / "flood_map_changes.csv", index=False)
print(cells.round(1).to_string(index=False))

# %% [markdown]
# ## 4. Recorded impact places
#
# Mean water depth within 5 m of each place where recorded storms (2018-2024) caused
# flooding, present climate, 100-year storm (from the analysis).

# %%
places = pd.read_csv(CLEAN / "places.csv").pivot_table(index="place", columns="land_cover", values="mean_depth_5m")
places.to_csv(RESULTS / "impact_places_depth.csv")
print(places.round(2).to_string())

# %% [markdown]
# ## Does the finding hold in every case?

# %%
either = reduction[reduction["risk"] == "either"]
rare = reduction[reduction["rp"].isin([100, 200])]
claim = {
    "aida": "The nature-based solutions of REACHOUT's planned scenario for Logroño reduce the number of residents "
            "in buildings at pluvial flood risk by less than 4 %, with no reduction during the 100- and 200-year storms.",
    "max_reduction_pct": float(reduction["reduction_pct"].max()),
    "max_reduction_residents": float(reduction["reduction"].max()),
    "reduction_below_4pct_everywhere": bool((reduction["reduction_pct"] < 4).all()),
    "no_reduction_for_100_and_200_year_storms": bool((rare["reduction"].abs() < 1e-6).all()),
    "never_an_increase": bool((reduction["reduction"] > -1e-6).all()),
    "return_periods_with_any_reduction": {lc: sorted(either.loc[(either["land_cover"] == lc) & (either["reduction"] > 1e-6), "rp"]
                                                     .unique().tolist()) for lc in NBS},
    "cases_checked": int(len(reduction)),
    "maps_not_available": not_available.to_dict("records"),
}
claim["holds"] = claim["reduction_below_4pct_everywhere"] and claim["no_reduction_for_100_and_200_year_storms"]
(RESULTS / "claim_test.json").write_text(json.dumps(claim, indent=2, ensure_ascii=False))
claim
