# Data model

## Observation

One row represents one variable observed by one source at one instant. Required fields are timestamp with offset, source identifier, variable, value and unit. Harmonised output retains the original value and unit, adds UTC time, and records explicit QA flags.

## Instrument

Recommended metadata: manufacturer, model, serial number, analyser identifier, gases, units, detection/reporting limits, calibration records, inlet and sampling-line identifiers, raw frequency, response time, flush time, averaging time, time zone, owner and source-file hash.

## Site and housing

Recommended metadata: farm/building/zone identifiers, coordinates with access controls, time zone, species and animal category, animal count, production stage, housing, ventilation, floor and manure systems, occupancy intervals and campaign identifiers.

## Weather and barn climate

Wind speed/direction, temperature, relative humidity, precipitation, ventilation flow and equipment states remain timestamped observations. The calculation adapter decides whether each variable is a direct input, explanatory covariate, quality criterion or evidence-only field.

## Laboratory sample

Sample identifier, collection time and location, matrix, wet mass, total solids, volatile solids, analyte, method, laboratory, detection limit, uncertainty and chain-of-custody/provenance fields.
