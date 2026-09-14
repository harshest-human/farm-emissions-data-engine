# Farm Emissions Data Engine

**Reproducible R and Python workflows from multimodal farm observations to calculation-ready livestock datasets.**

[![CI](https://github.com/harshest-human/farm-emissions-data-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/harshest-human/farm-emissions-data-engine/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](https://www.python.org/)
[![R](https://img.shields.io/badge/R-QA%2FQC-276DC3.svg)](https://www.r-project.org/)

**Portfolio:** [From sensors to climate evidence](https://harshest-human.github.io/farm-emissions-data-engine/)

This repository preserves provenance while ingesting, cleaning, harmonising and validating raw analyser, weather, barn-climate, animal, housing, management and site data. It produces machine-readable exports that can be mapped to the publicly documented input requirements of KTBL's *Berechnungsmethode für einzelbetriebliche Klimabilanzen* (BEK) and to other institutional calculation services.

## Research context and affiliation

The project is developed by **Harsh Sahu**, Doctoral Researcher in Sensors and Modelling at the **Leibniz Institute for Agricultural Engineering and Bioeconomy (ATB), Potsdam**, in the scientific context of barn-climate and emission measurement/modelling from livestock buildings.

The design is informed by data-engineering needs encountered in **EmiMod - Development of methods for recording, modelling and assessing emissions in livestock buildings**. EmiMod investigates diffuse emission sources including naturally ventilated cattle and pig housing, outdoor areas and slurry stores. It covers ammonia, greenhouse gases, odour and bioaerosols and combines measurements with mechanistic modelling, numerical flow simulation and AI applications.

This is an independent open-source research prototype. It is not an official product of ATB, EmiMod, KTBL, Freie Universität Berlin or any project partner, and institutional affiliation does not imply endorsement or validation.

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

## What it can do now

- validate essential farm, building, time-zone, species, animal-category and housing metadata
- ingest tidy long-format observations from gas analysers, weather stations and barn sensors
- reject timestamps without an explicit offset and normalise valid timestamps to UTC
- preserve original values and units alongside processed fields
- flag negative values, zero gas concentrations and impossible humidity values without silently deleting rows
- hash raw inputs and processed outputs and write machine-readable provenance records
- attach analyser response and flush-window metadata in the R QA layer
- maintain explicit BEK-oriented crosswalks and source-status labels
- run on synthetic cattle, pig, poultry or other-species fixtures without exposing farm data

## Planned adapters

- FTIR, CRDS and PAS source-specific parsers
- ultrasonic anemometer and weather-station adapters
- fan, curtain, cooling and ventilation-control logs
- herd-management and production records
- manure/slurry laboratory results including total and volatile solids
- Parquet and JSON-LD exports
- FastAPI validation and export endpoints
- reviewed adapters for institutional calculation services

## Sources

- [KTBL BEK project and revision status](https://www.ktbl.de/projekte/emissionen-und-klimaschutz/klimabilanzen)
- [KTBL BEK topic page](https://www.ktbl.de/themen/bek)
- [KTBL Sachbilanz Tierhaltung 2026](https://www.ktbl.de/fileadmin/user_upload/Allgemeines/Download/BEK/BEK_Sachbilanz_Tierhaltung_2026-02-05.pdf)
- [KTBL WebKlim project](https://www.ktbl.de/projekte/emissionen-und-klimaschutz/webklim)
- [KTBL InKalkTier](https://www.ktbl.de/webanwendungen/inkalktier)
- [KTBL National Assessment Framework for pig housing](https://www.ktbl.de/themen/nationaler-bewertungsrahmen-tierhaltung/nbr-schwein)
- [ATB profile of Harsh Sahu](https://www.atb-potsdam.de/en/about-us/team/staff-members/person/harsh-sahu)
- [ATB EmiMod project](https://www.atb-potsdam.de/en/research/research-programs/en-integriertes-reststoffmanagement/projects/project/projekt/emimod)

## Licence

Apache-2.0 for code. Source classifications and parameters retain their original attribution and usage conditions.
