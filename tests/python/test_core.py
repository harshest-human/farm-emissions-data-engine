import csv
import json
import tempfile
import unittest
from pathlib import Path

from livestock_data.core import harmonise_csv, parse_timestamp, validate_site_metadata


class PipelineTests(unittest.TestCase):
    def test_timestamp_normalises_to_utc(self):
        self.assertEqual(parse_timestamp("2026-01-15T10:00:00+01:00"), "2026-01-15T09:00:00Z")

    def test_naive_timestamp_rejected(self):
        with self.assertRaisesRegex(ValueError, "UTC offset"):
            parse_timestamp("2026-01-15T10:00:00")

    def test_metadata_validation(self):
        data = {"farm_id": "f", "building_id": "b", "timezone": "Europe/Berlin", "species": "cattle", "animal_category": "dairy_cow", "housing_system": "free_stall"}
        self.assertEqual(validate_site_metadata(data), [])

    def test_harmonise_preserves_original_and_flags(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "raw.csv"
            target = Path(tmp) / "clean.csv"
            source.write_text("timestamp,source_id,variable,value,unit\n2026-01-15T10:00:00+01:00,a,ch4,0,ppm\n", encoding="utf-8")
            record = harmonise_csv(source, target)
            with target.open(newline="", encoding="utf-8") as stream:
                row = next(csv.DictReader(stream))
            self.assertEqual(row["value_original"], "0")
            self.assertEqual(row["qa_flags"], "zero_concentration")
            self.assertEqual(record["row_count"], 1)
            self.assertTrue(target.with_suffix(".csv.provenance.json").exists())


if __name__ == "__main__":
    unittest.main()
