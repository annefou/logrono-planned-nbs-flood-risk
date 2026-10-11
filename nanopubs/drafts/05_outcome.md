# 05 — FORRT Replication Outcome

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Verify the actual numerical results first** by reading `results/` and `notebooks/03_analysis.py`. Don't quote numbers from memory. See `docs/verify-before-drafting.md`.

## Field-by-field draft

<!-- field: outcome -->
### Short URI suffix for outcome ID (text input, required)

Slug. Use kebab-case.

```
logrono-planned-nbs-flood-risk-outcome
```

<!-- field: label -->
### Plain-text label for the outcome (text input, required)

Descriptive title.

```
REACHOUT's planned nature-based solutions reduce residents at pluvial flood risk in Logroño by less than 4 %, only for frequent storms
```

<!-- field: study -->
### Choose study (search/select, required)

URI of the Replication Study published in step 04. Pull from `nanopubs/PUBLISHED.md`.

```

```

<!-- field: repo -->
### Repository URL (text input, required)

Use the Zenodo **version DOI** URL for the release the results came from — not a
bare branch URL, and not the concept DOI.

> **Why not the bare repo URL.** `https://github.com/ORG/REPO` names a *moving
> branch*. This Outcome asserts "this code produced this number", in a signed,
> immutable record. A branch URL means that assertion points at whatever `main`
> happens to be years from now — code that may never have produced the number
> above. A concept DOI has the same flaw: it resolves to the latest version.
> The version DOI pins the exact release. `docs/chain-decision-tree.md` § Anchor
> ranks the options: SWHID > Zenodo DOI > repo URL > Wayback.
>
> Both DOIs and the SWHID are in `CITATION.cff` under `identifiers:`, recorded
> automatically at release by `.github/workflows/release-identifiers.yml`. Take
> the one described as *"Version DOI"*.

```
https://doi.org/{{ZENODO_VERSION_DOI}}
```

<!-- field: date -->
### Choose completion date (text input, required)

```
2026-10-10
```

<!-- field: validationStatus -->
### Choose validation status (dropdown, required)


This dropdown maps to the CiTO intention in step 06: Validated → `confirms`, PartiallySupported → `qualifies`, Contradicted → `disputes`.

- [ ] contradicted
- [ ] inconclusive
- [ ] not tested
- [ ] partially supported
- [x] validated

<!-- field: confidenceLevel -->
### Choose confidence level (dropdown, required)

_Vocabulary not yet captured._

```

```

- [ ] high - Strong evidence, mostly agrees with original
- [ ] low - Limited evidence, significant disagreement
- [x] moderate - Adequate evidence, partial agreement
- [ ] very high - Extensive evidence, high agreement with original
- [ ] very low - Minimal evidence, major disagreement

<!-- field: conclusion -->
### Describe the overall conclusion about the original claim (textarea, required)

Substantive interpretation. Headline comparison: replication's number vs the paper's number, sign + significance.

```
Validated. In Logroño (Spain), the nature-based solutions of REACHOUT's planned scenario reduce the number of residents in buildings at pluvial flood risk only a little and only for frequent storms: by at most 1.7 % without the extra ponds and 3.7 % with them, and not at all during the 100- and 200-year storms, under present or future rainfall. The planned scenario without ponds stops reducing risk after the 10-year storm, the version with ponds after the 50-year storm. Neither ever increases the number of residents at risk. The measures change the flood maps over a few hectares in the south of the city, while future rainfall adds tens to over a hundred hectares of deeper water (see the future-rainfall chain), so in this model the planned measures do not offset climate change. This describes the measures as REACHOUT modelled them, as infiltration and storage in a fill-and-spill model without sewers; it is not an assessment of the measures as they may be built.
```

<!-- field: evidence -->
### Describe the evidence that supports your conclusion (textarea, required)

Numerical results, test statistics, model coefficients. Read directly from `results/`.

```
Residents in buildings at risk (either risk index above zero), reduction against the current green cover under the same rainfall: planned scenario, 446 residents (1.7 %) for the 2-year storm with present rainfall, at most 0.8 % under future rainfall, none from the 25-year storm on (present) or the 10-year storm on (90th percentile); planned scenario with ponds, 640 (2.5 %), 405 (1.4 %) and 746 (2.3 %) residents for the 2-, 5- and 10-year storms with present rainfall, at most 1,001 residents (3.7 %) for the 2-year storm under the median future rainfall, 43 residents (0.1 %) for the 50-year storm, none for the 100- and 200-year storms. 123 cases checked (2 scenarios x 3 climates x 7 return periods x 3 risk measures, one map missing); no increase in any. Present rainfall: residential buildings whose hazard changes at all, 0-6 (planned) and 5-19 (with ponds) per return period and risk; flood-map cells changing by more than 1 cm, 0.06-9.1 ha (planned) and 7.6-12.5 ha (with ponds); stored water -66 to -8,380 m3 (planned) and -12,419 to +14,512 m3 (with ponds, which store more water from the 25-year storm on). Recorded impact places, 100-year storm, mean depth within 5 m: under the planned scenario it changes by at most 0.01 m at all 13 places; under the version with ponds it rises on the LO-20 ring road (0.19 to 0.26 m) and on the sunken LO-20 below the calle Chile roundabout (0.04 to 1.76 m), where a nearby terrain hollow drains, and changes by at most 0.01 m elsewhere. Figure: figures/main_result.png; checks: results/claim_test.json.
```

<!-- field: limitations -->
### Describe what limits the conclusions of the study (textarea, optional)

Honest caveats. If the result is partial or contradicted, say so plainly. Don't overclaim.

```
The measures are those of REACHOUT's planned scenario, modelled by REACHOUT: SaferRAIN represents them as infiltration and, for the ponds, as terrain changes, on 15-minute design storms, without sewers and without the dynamics of storage, overflow or clogging. A model of this kind is likely to understate what storage can do and cannot show what drainage design adds, so a small effect here is partly a property of the model. REACHOUT does not publish the layout of the measures; where they act is inferred from the changed flood maps, and the change at the LO-20 underpass under the version with ponds may be intended or an artefact of the terrain edit. One map (25-year storm, median future rainfall, planned scenario) is missing. The city's own plans, which may differ from REACHOUT's scenario, are not assessed. Risk counts residents only (fixed at 2021) and uses unvalidated census-section vulnerability; benefits for roads, businesses or public spaces are not counted.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 05.
