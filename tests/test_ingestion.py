import contextlib
import hashlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from chronoz_quant.io import detect_columns, discover, read_csv
from chronoz_quant.pipeline import build_wide, run
from chronoz_quant.registry import REGISTRY
from chronoz_quant.validation import infer_frequency, validate


class IngestionTests(unittest.TestCase):
    def test_duplicates_and_invalid_tokens_are_accounted_for(self):
        raw = pd.DataFrame({"DATE": ["2020-01-01"] * 3 + ["bad", "2020-02-01"],
                            "VALUE": ["1", "1", "2", "oops", "."]})
        frame, metrics, warnings = validate(raw, "DATE", "VALUE", "monthly")
        self.assertEqual(len(frame), 4)
        self.assertEqual(metrics["exact_duplicate_rows_removed"], 1)
        self.assertEqual(metrics["conflicting_duplicate_dates"], 1)
        self.assertEqual(metrics["invalid_dates"], 1)
        self.assertEqual(metrics["coerced_values"], 1)
        self.assertEqual(metrics["missing_values"], 2)
        self.assertTrue(warnings)
        frame["series_id"] = "TEST"
        wide = build_wide(frame, ["TEST", "ABSENT"])
        self.assertEqual(len(wide), 4)
        self.assertEqual(wide.TEST.dropna().tolist(), [1, 2])
        self.assertEqual(wide.date.isna().sum(), 1)
        self.assertTrue(wide.ABSENT.isna().all())

    def test_extra_columns_prevent_false_deduplication(self):
        raw = pd.DataFrame({"date": ["2020-01-01"] * 2, "INDPRO": ["1", "1"], "note": ["a", "b"]})
        date, value, warnings = detect_columns(raw, "INDPRO")
        self.assertIn("note", warnings[0])
        frame, metrics, _ = validate(raw, date, value, "monthly")
        self.assertEqual(len(frame), 2)
        self.assertEqual(metrics["exact_duplicate_rows_removed"], 0)
        with self.assertRaises(ValueError):
            detect_columns(pd.DataFrame(columns=["DATE", "observation_date", "VALUE"]), "X")
        with self.assertRaises(ValueError):
            detect_columns(pd.DataFrame(columns=["date", "a", "b"]), "X")

    def test_frequency_does_not_resample(self):
        for frequency, dates in [
            ("monthly", ["2020-01-01", "2020-02-01", "2020-03-01"]),
            ("quarterly", ["2020-01-01", "2020-04-01", "2020-07-01"]),
            ("weekly", ["2020-01-04", "2020-01-11", "2020-01-18"]),
            ("irregular", ["2020-01-01", "2020-01-04", "2020-05-01"]),
        ]:
            self.assertEqual(infer_frequency(pd.Series(pd.to_datetime(dates))), frequency)

    def test_run_is_reproducible_and_raw_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "data").mkdir()
            source = root / "data/INDPRO.csv"
            original = b"observation_date,INDPRO\n2020-01-01,1\n2020-02-01,.\n2020-03-01,3\n"
            source.write_bytes(original)
            with contextlib.redirect_stdout(io.StringIO()):
                audit = run(root, REGISTRY[:2])
                paths = list((root / "outputs").rglob("*.csv")) + list((root / "data/interim").glob("*.csv"))
                before = [hashlib.sha256(p.read_bytes()).hexdigest() for p in paths]
                run(root, REGISTRY[:2])
            self.assertEqual(before, [hashlib.sha256(p.read_bytes()).hexdigest() for p in paths])
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual((root / REGISTRY[0].raw_path).read_bytes(), original)
            self.assertEqual(audit.load_status.tolist(), ["WARNING", "FAILED"])
            self.assertTrue(pd.isna(audit.iloc[1].valid_observations))
            source.write_text("date,value\n2020-01-01,9\n")
            with self.assertRaises(ValueError):
                discover(root, REGISTRY[0])

    def test_malformed_records_and_headers_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.csv"
            for content in ["date,value\n2020-01-01,1,extra\n", "date,value,value\n2020-01-01,1,2\n", "date,value\n\n"]:
                path.write_text(content)
                with self.assertRaises(ValueError):
                    read_csv(path)


if __name__ == "__main__":
    unittest.main()
