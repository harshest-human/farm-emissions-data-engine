# Livestock Sensor Data Pipeline

**Reproducible R and Python workflows from multimodal farm observations to calculation-ready livestock datasets.**

This repository preserves provenance while ingesting, cleaning, harmonising and validating raw analyser, weather, barn-climate, animal, housing, management and site data. It produces machine-readable exports that can be mapped to the publicly documented input requirements of KTBL's *Berechnungsmethode für einzelbetriebliche Klimabilanzen* (BEK) and to other institutional calculation services.

## Important terminology

The outputs are **KTBL-oriented** and **mappable to KTBL classifications**. They are not official “KTBL-standard datasets”. As of September 2026, KTBL publicly provides a revised BEK *Sachbilanz Tierhaltung* for cattle and pigs, while the wider handbook and parameter application are under revision. No public formal raw-sensor schema or general BEK API contract was identified.

Broader housing classifications for cattle, pigs and poultry may be cross-referenced from separate KTBL resources such as the National Assessment Framework and InKalkTier. Those classifications are versioned separately and must not be presented as BEK calculation inputs unless the BEK method explicitly requires them.

## Pipeline

```text
Immutable raw files + metadata
             |
             v
      Source-specific adapter  <---- R analyser QA and visual review
             |
             v
 timestamps, time zones, units, response/flush windows
             |
             v
 long observations + explicit QA flags + provenance hashes
             |
             v
 animal/site/housing/management metadata validation
             |
             v
 clean research export + BEK-oriented activity-data crosswalk
             |
             v
 calculation service, API adapter, or livestock-emissions-dmrv
```

## Data domains

- reference gas analysers: FTIR, CRDS, PAS and adapter-defined instruments
- weather: wind, temperature, relative humidity, precipitation and external station provenance
- barn climate: indoor temperature/RH, concentration, ventilation, fan/curtain/cooling states
- animals: species, category, counts, live weight, production stage and performance
- site and housing: farm/building/zone identifiers, coordinates, time zone, housing/ventilation/floor/manure systems
- management: occupancy, feeding, milking, cleaning and manure-removal events
- laboratory: sample ID, matrix, total solids, volatile solids, analyte, method and uncertainty

## BEK 2026 mapping

The current public livestock method identifies farm-specific needs for:

1. feed quantity, composition, origin and feed product carbon footprint
2. animal number and weight, housing/pasture system and duration
3. excretion/manure type and manure management
4. electricity and other energy quantity, source and origin

The pipeline records these as a crosswalk layer. Sensor streams are normally evidence or inputs to derived quantities; they are not automatically direct BEK inputs.

## Quick start

```bash
python -m pip install -e .
livestock-data validate examples/metadata/site.json
livestock-data harmonise examples/raw/synthetic_observations.csv artifacts/observations.csv
python -m unittest discover -s tests/python -v
Rscript tests/r/test_qaqc.R
```

## Repository boundary

This repository owns raw-file registration, source adapters, QA flags, time/unit harmonisation, metadata and calculation-ready exports. The companion `livestock-emissions-dmrv` repository owns emission equations, uncertainty propagation and evidence bundles. Neither repository contains private farm data or unpublished research data.

## Status and limitations

- Public synthetic fixtures only.
- Current controlled vocabulary is a small, explicit demonstrator, not a complete KTBL catalogue.
- Cattle and pig BEK mapping is supported at the method-crosswalk level.
- Poultry and other species require separately sourced, licensed and versioned mappings.
- A FastAPI interface is a planned transport layer after scientific schema review.

## Sources

- [KTBL BEK project and revision status](https://www.ktbl.de/projekte/emissionen-und-klimaschutz/klimabilanzen)
- [KTBL BEK topic page](https://www.ktbl.de/themen/bek)
- [KTBL Sachbilanz Tierhaltung 2026](https://www.ktbl.de/fileadmin/user_upload/Allgemeines/Download/BEK/BEK_Sachbilanz_Tierhaltung_2026-02-05.pdf)
- [KTBL WebKlim project](https://www.ktbl.de/projekte/emissionen-und-klimaschutz/webklim)
- [KTBL InKalkTier](https://www.ktbl.de/webanwendungen/inkalktier)
- [KTBL National Assessment Framework for pig housing](https://www.ktbl.de/themen/nationaler-bewertungsrahmen-tierhaltung/nbr-schwein)

## Licence

Apache-2.0 for code. Source classifications and parameters retain their original attribution and usage conditions.
