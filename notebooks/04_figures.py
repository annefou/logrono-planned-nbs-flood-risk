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
# # 04 — Figures
#
# `figures/main_result.png` is this chain's headline figure. Saved and displayed inline
# (`plt.show()` after `fig.savefig()`; no `matplotlib.use('Agg')`). Before saving, the
# figure passes `scripts/figcheck.py`: no overlapping text, no legend over data.
#
# Top: the reduction in residents in buildings at pluvial flood risk, for each version of
# REACHOUT's planned scenario, against the current green cover. Bottom: where each version
# changes the 2-year flood map (depth change above 1 cm, cells modelled in both maps),
# read from the REACHOUT rasters — this shows where the *model's water* changes, not the
# layout of the measures, which REACHOUT does not publish. Basemap: Esri World Light Gray
# Canvas and its labels layer (context only; without network the map is drawn without it).
# REACHOUT has no 25-year map for the planned scenario under the median future rainfall:
# that line is broken there.

# %%
import json
import sys
from pathlib import Path

import contextily as cx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
import rasterio.windows
import xyzservices
from pyproj import Transformer

sys.path.insert(0, str(Path("../scripts").resolve()))
from figcheck import assert_layout  # noqa: E402

RAW = Path("../data/raw")
RESULTS = Path("../results")
FIGURES = Path("../figures")
FIGURES.mkdir(parents=True, exist_ok=True)
plt.style.use("seaborn-v0_8-whitegrid")
DPI = 150
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
CLIMATE = {"present": (BLUE, "present rainfall"), "CC_Q50": (ORANGE, "future, median (Q50)"),
           "CC_Q90": (AQUA, "future, 90th pct. (Q90)")}
SCENARIO = {"NBSplanned": "Planned NBS", "NBSplanned_plus": "Planned NBS + ponds"}
TEXT, MUTED = "#0b0b0b", "#52514e"
RPS = [2, 5, 10, 25, 50, 100, 200]
ARCHIVE = Path(json.loads((RAW / "sources.json").read_text())["reachout"]["path"])
BASE = cx.providers.Esri.WorldGrayCanvas
LABELS = xyzservices.TileProvider(
    name="Esri.WorldGrayReference", attribution=BASE.attribution, max_zoom=16,
    url="https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Reference/MapServer/tile/{z}/{y}/{x}")


def style_axis(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", visible=False)
    ax.tick_params(colors=MUTED, labelsize=9)


def depth_change(land_cover: str, rp_file: str = "A_RP2.tif") -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Cells (EPSG:3857 x, y) whose depth changes by more than 1 cm against Baseline, and the change."""
    with rasterio.open(f"/vsizip/{ARCHIVE}/Logrono/{land_cover}/{rp_file}") as s:
        scen, tf, nodata_s, crs = s.read(1), s.transform, s.nodata, s.crs
        bounds = s.bounds
    with rasterio.open(f"/vsizip/{ARCHIVE}/Logrono/Baseline/{rp_file}") as b:
        w = rasterio.windows.from_bounds(*bounds, transform=b.transform)
        w = rasterio.windows.Window(round(w.col_off), round(w.row_off), scen.shape[1], scen.shape[0])
        base, nodata_b = b.read(1, window=w), b.nodata
    modelled = (scen != nodata_s) & (base != nodata_b)
    diff = np.where(modelled, np.nan_to_num(scen, nan=0.0) - np.nan_to_num(base, nan=0.0), 0.0)
    rows, cols = np.nonzero(np.abs(diff) > 0.01)
    x, y = rasterio.transform.xy(tf, rows, cols)
    x3857, y3857 = Transformer.from_crs(crs, "EPSG:3857", always_xy=True).transform(np.asarray(x), np.asarray(y))
    return x3857, y3857, diff[rows, cols]


# %%
reduction = pd.read_csv(RESULTS / "residents_at_risk_reduction.csv")
either = reduction[reduction["risk"] == "either"]
changes = {lc: depth_change(lc) for lc in SCENARIO}
xs = np.concatenate([c[0] for c in changes.values()])
ys = np.concatenate([c[1] for c in changes.values()])
pad = 1500
extent = (xs.min() - pad, xs.max() + pad, ys.min() - pad, ys.max() + pad)

fig, axes = plt.subplots(2, 2, figsize=(14, 10.5), gridspec_kw={"height_ratios": [1, 1.15]})
ymax = either["reduction_pct"].max() * 1.25
for ax, (lc, name) in zip(axes[0], SCENARIO.items()):
    for c, (colour, label) in CLIMATE.items():
        # reindex on every return period: a map REACHOUT does not provide breaks the line
        d = either[(either["land_cover"] == lc) & (either["climate"] == c)].set_index("rp").reindex(RPS).reset_index()
        ax.plot(d["rp"], d["reduction_pct"], color=colour, lw=2, marker="o", ms=5, markeredgecolor="white",
                markeredgewidth=1.5)
    ax.axhline(0, color="#a3a29b", lw=1)
    ax.set_xscale("log")
    ax.set_xticks(RPS, labels=[str(r) for r in RPS])
    ax.set_xlim(1.7, 260)
    ax.set_ylim(-0.3, ymax)
    ax.set_xlabel("Return period of the design storm (years)", color=MUTED, fontsize=9)
    ax.set_ylabel("Fewer residents at risk than with current cover (%)", color=MUTED, fontsize=9)
    ax.set_title(f"{name}: reduction in residents at risk", loc="left", fontsize=11, color=TEXT)
    ax.legend([plt.Line2D([], [], color=CLIMATE[c][0], lw=2) for c in CLIMATE], [CLIMATE[c][1] for c in CLIMATE],
              loc="upper right", fontsize=8.5, frameon=False)
    style_axis(ax)

for ax, (lc, name) in zip(axes[1], SCENARIO.items()):
    x, y, d = changes[lc]
    for mask, colour, label in ((d < 0, BLUE, "shallower"), (d > 0, ORANGE, "deeper")):
        ax.scatter(x[mask], y[mask], s=1.5, color=colour, linewidths=0, label=f"{label} ({mask.sum() * 4 / 1e4:.1f} ha)")
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    try:
        cx.add_basemap(ax, crs="EPSG:3857", source=BASE, attribution=False, zorder=0)
        cx.add_basemap(ax, crs="EPSG:3857", source=LABELS, attribution=False, zorder=10)
    except Exception as exc:  # noqa: BLE001 - context layer only
        print(f"basemap not drawn ({type(exc).__name__})")
    ax.set_axis_off()
    ax.set_title(f"{name}: where the 2-year flood map changes", loc="left", fontsize=11, color=TEXT)
    ax.legend(loc="lower left", fontsize=8.5, markerscale=6, frameon=True, framealpha=0.9)

fig.suptitle("Logroño (Spain): REACHOUT's planned nature-based solutions reduce residents at pluvial flood risk "
             "only for frequent storms", x=0.01, ha="left", fontsize=12.5, color=TEXT)
fig.text(0.99, 0.005, f"Basemap: {BASE.attribution}", ha="right", fontsize=7, color=MUTED)
fig.tight_layout()
assert_layout(fig)
fig.savefig(FIGURES / "main_result.png", dpi=DPI, bbox_inches="tight")
plt.show()
