# 04 — FORRT Replication Study

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Verify code first:** read the actual reproduction script in `notebooks/03_analysis.py` before writing the methodology field. See `docs/verify-before-drafting.md`.

## Field-by-field draft

<!-- field: study -->
### Short URI suffix for study ID (text input, required)

Slug. Use kebab-case.

```
logrono-planned-nbs-flood-risk-study
```

<!-- field: label -->
### Label/name of replication study (text input, required)

Human-readable title.

```
Building-level pluvial flood risk in Logroño with REACHOUT's planned nature-based solutions
```

<!-- field: type -->
### Choose the study type (dropdown, required)

- [x] Replication Study - replication with different methodology or conditions
- [ ] Reproduction/Replication Study - study that is both, reproduction and replication
- [ ] Reproduction Study - direct reproduction: same methodology, same tools

<!-- field: claim -->
### Choose FORRT claim (search/select, required)

URI of the Claim published in step 03. Pull from `nanopubs/PUBLISHED.md`.

```

```

<!-- field: scope -->
### Describe what part of the claim is reproduced/replicated. (textarea, required)

The **scope** of the claim being tested. Which aspect, what's in/out of scope. NOT methodology. NOT results. See `docs/pico-study-outcome-levels.md`.

```
Whether the nature-based solutions of REACHOUT's planned scenario for Logroño (Spain) reduce the number of residents living in buildings at pluvial flood risk, compared with the current green cover under the same rainfall. In scope: both versions of the planned scenario as published by REACHOUT (bioswales and ponds, about 29,850 m3, and a 5.3 km green corridor in the southern part of the city; and the same with additional small ponds and rain gardens, about 13,500 m3); every residential building inside the area modelled by all scenarios; the seven design storms (return periods of 2 to 200 years) under present and future (EURO-CORDEX median and 90th percentile) rainfall; both risk indices and either; which residential buildings' hazard changes at all; where the flood maps change; water on and around the places where recorded storms (2018-2024) caused flooding. Out of scope: the city's own plans as eventually built (only REACHOUT's scenario is modelled, and its layout is not published); measures modelled other than as REACHOUT modelled them; sewers; costs and co-benefits of the measures; population change; the validity of social vulnerability.
```

<!-- field: methodology -->
### Describe how the claim is reproduced/replicated. (textarea, required)

The **method** in plain prose. Read `notebooks/03_analysis.py` and any config files first. NOT exact numerical results.

```
Data and pipeline: the shared analysis Logroño flood-adaptation scenarios, release v0.1.0 (10.5281/zenodo.23298913), whose result tables this chain reads (its pipeline can be re-run from the same repository), and the REACHOUT archive itself for the map. Flood hazard: REACHOUT pluvial flood maps for Logroño (Staccione and Pal, 10.5281/zenodo.14035876), SaferRAIN, 2 m, 15-minute design storms, for the current green cover (Baseline), the planned scenario (NBSplanned) and the planned scenario with extra ponds (NBSplanned_plus); in SaferRAIN the measures change the infiltration layer and, for the ponds, the terrain. The comparison is restricted to cells modelled in every scenario. Flooded extents at depths of 30 to 100 cm are polygonised on the native grid, without resampling, and water bodies are removed. City inputs from the Logroño replication v0.1.1 (10.5281/zenodo.23285198). Risk: building-climate-risk v0.2.1 (10.5281/zenodo.23285504) with the paper's settings (TOPSIS with entropy; flood-sensitivity transform; hazard to well-being from a 2 m ring over depths of 30-100 cm; hazard to mobility from 5 / 15 / 30 m rings at 30 cm; risk = social vulnerability x exposure x hazard), social vulnerability ranked over all residential buildings of the city; a building is at risk when a risk index is above zero. Measures: residents and buildings at risk in each planned scenario against the current green cover, same rainfall, every return period and climate; residential buildings whose hazard changes, and flood-map cells getting shallower or deeper by more than 1 cm, under present rainfall (the analysis compares every map with the present-day current cover, so only present rainfall isolates the measures); mean water depth within 5 m of each recorded impact place.
```

<!-- field: deviation -->
### Describe any deviations from original methodology. (textarea, optional)

What's different from the original method. Verify against the actual code, don't guess.

```
From the framework of Vogelbacher et al. (2026): (1) hazard model REACHOUT SaferRAIN (hydrostatic fill-and-spill with Green-Ampt infiltration, no sewer network, 15-minute storms) instead of VISDOM-SWMM; nature-based solutions enter only as REACHOUT modelled them (infiltration and, for the ponds, terrain), without the dynamics of storage, overflow or clogging; (2) census-section proxies for the vulnerability indicators; residents fixed at 2021; (3) comparison restricted to the area modelled by every scenario: 157 buildings (77 with residents, 1,851 residents) are left out. Data: (4) REACHOUT provides no 25-year map for the planned scenario under the median future rainfall; that case is left out; (5) the layout of the measures is not published, so where they act is inferred from where the flood maps change.
```

<!-- field: keyword -->
### Search keywords (Wikidata) (search/select, optional)

Provide labels (not QIDs) — the Wikidata search picks up labels.

- nature-based solutions (Q2421934)
- green infrastructure (Q3427027)
- Sustainable urban drainage system (Q2897115)
- urban flooding (Q15909735)
- flood risk (Q2288778)
- Logroño (Q14325)

<!-- field: discipline -->
### Search discipline (Wikidata) (search/select, optional)

Provide labels.

- hydrology (Q42250)

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 04.
