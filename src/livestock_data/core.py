"""Small dependency-free processing core for auditable tabular harmonisation."""

from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_OBSERVATION_COLUMNS = {
    "timestamp",
    "source_id",
    "variable",
    "value",
    "unit",
}

UNIT_FACTORS = {
    ("ppm", "ppm"): 1.0,
    ("ppb", "ppm"): 0.001,
    ("mg/m3", "mg/m3"): 1.0,
    ("degC", "degC"): 1.0,
    ("%", "%"): 1.0,
    ("m/s", "m/s"): 1.0,
    ("m3/h", "m3/h"): 1.0,
}

REQUIRED_SITE_FIELDS = {
    "farm_id", "building_id", "timezone", "species", "animal_category", "housing_system"
}


def validate_site_metadata(data: dict) -> list[str]:
    """Return stable validation messages without discarding extra metadata."""
    errors = [f"missing:{name}" for name in sorted(REQUIRED_SITE_FIELDS - set(data))]
    if "animal_count" in data and (not isinstance(data["animal_count"], (int, float)) or data["animal_count"] < 0):
        errors.append("invalid:animal_count")
    if data.get("species") not in {"cattle", "pig", "chicken", "turkey", "other"}:
        errors.append("invalid:species")
    return errors


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_timestamp(value: str) -> str:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include a UTC offset or Z")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def qa_flags(variable: str, value: float) -> list[str]:
    flags = []
    if value < 0:
        flags.append("negative_value")
    if variable in {"ch4", "co2", "nh3"} and value == 0:
        flags.append("zero_concentration")
    if variable == "relative_humidity" and not 0 <= value <= 100:
        flags.append("outside_physical_range")
    return flags


def harmonise_csv(input_path: str | Path, output_path: str | Path) -> dict:
    input_path, output_path = Path(input_path), Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with input_path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        missing = REQUIRED_OBSERVATION_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing columns: {sorted(missing)}")
        rows = list(reader)

    fields = list(reader.fieldnames or []) + ["timestamp_utc", "value_original", "unit_original", "qa_flags"]
    with output_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            original = float(row["value"])
            row["timestamp_utc"] = parse_timestamp(row["timestamp"])
            row["value_original"] = row["value"]
            row["unit_original"] = row["unit"]
            row["qa_flags"] = "|".join(qa_flags(row["variable"], original)) or "ok"
            writer.writerow(row)

    record = {
        "input_sha256": sha256_file(input_path),
        "output_sha256": sha256_file(output_path),
        "row_count": len(rows),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "software": "livestock-sensor-data-pipeline/0.1.0",
    }
    provenance_path = output_path.with_suffix(output_path.suffix + ".provenance.json")
    provenance_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return record
