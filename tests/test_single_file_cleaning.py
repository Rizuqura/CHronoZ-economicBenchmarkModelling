import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dataCleansing import REGISTRY, run


class CleaningTests(unittest.TestCase):
    def process(self, text):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "data/raw").mkdir(parents=True)
        raw = root / "data/raw/INDPRO.csv"
        raw.write_text(text, encoding="utf-8")
        before = raw.read_bytes()
        with contextlib.redirect_stdout(io.StringIO()):
            audit = run(root, REGISTRY[:1])
        self.assertEqual(raw.read_bytes(), before)
        return root, audit.iloc[0]

    def test_conflicts_invalids_gaps_and_missing(self):
        root, row = self.process("date,INDPRO\n2020-01-01,.\n2020-02-01,2\n2020-02-01,3\n2020-02-01,3\n2020-04-01,NA\n2020-05-01,4\nbad,7\n,\n")
        clean = pd.read_csv(root / row.clean_file)
        self.assertEqual(list(clean.columns), ["date", "value"])
        self.assertEqual(len(clean), 4)
        self.assertFalse(clean.value.isna().any())
        self.assertEqual(row.missing_value_rows_removed, 2)
        self.assertTrue(row.conflicting_duplicate_dates)
        self.assertEqual(row.exact_duplicate_rows_removed, 1)
        self.assertEqual(row.safe_empty_rows_removed, 1)
        self.assertEqual(row.retained_invalid_dates, 1)
        self.assertEqual(row.suspicious_gap_count, 1)
        self.assertEqual(row.leading_missing_count, 0)
        self.assertEqual(row.internal_missing_count, 0)

    def test_preamble_footer_and_extra_columns(self):
        root, row = self.process("FRED export\ndate,INDPRO,notes\n2020-01-01,1,a\n2020-02-01,2,b\n2020-03-01,3,c\nEnd,unknown,footer\n")
        self.assertEqual(row.metadata_rows, 1)
        self.assertEqual(row.possible_footer_rows, 1)
        self.assertEqual(row.clean_rows, 3)
        self.assertEqual(row.missing_value_rows_removed, 1)
        self.assertEqual(row.nonnumeric_value_count, 1)
        self.assertIn("Extra columns", row.warning)
        self.assertTrue((root / "data/audit/observations_for_review.csv").exists())

    def test_fallback_detection_and_ambiguity(self):
        _, row = self.process("when,measurement,index\n2020-01-01,1,0\n2020-02-01,2,1\n2020-03-01,3,2\n")
        self.assertEqual(row.detected_date_column, "when")
        self.assertEqual(row.detected_value_column, "measurement")
        _, row = self.process("date,a,b\n2020-01-01,1,2\n2020-02-01,3,4\n")
        self.assertEqual(row.status, "FAILED")
        self.assertIn("Ambiguous", row.error)

    def test_empty_malformed_and_no_usable_observations(self):
        for text in ["date,INDPRO\n", "date,INDPRO\n2020-01-01,1,extra\n", "date,INDPRO\n2020-01-01,NA\n"]:
            with self.subTest(text=text):
                _, row = self.process(text)
                self.assertEqual(row.status, "FAILED")
                self.assertTrue(row.error)

    def test_nonfinite_extreme_and_trailing_missing(self):
        _, row = self.process("date,INDPRO\n2020-01-01,1\n2020-02-01,inf\n2020-03-01,1e101\n2020-04-01,oops\n2020-05-01,.\n")
        self.assertEqual(row.infinite_value_count, 1)
        self.assertEqual(row.extreme_numeric_count, 1)
        self.assertEqual(row.nonnumeric_value_count, 1)
        self.assertEqual(row.trailing_missing_count, 0)
        self.assertEqual(row.missing_value_rows_removed, 2)

    def test_missing_rows_removed_without_changing_remaining_observations(self):
        root, row = self.process("date,INDPRO\n2020-01-01,.\n2020-02-01,2\n2020-03-01,NA\n2020-04-01,4\n2020-05-01,\n")
        clean = pd.read_csv(root / row.clean_file)
        self.assertEqual(clean.to_dict('list'), {'date': ['2020-02-01', '2020-04-01'], 'value': [2, 4]})
        self.assertEqual(row.raw_missing_count, 3)
        self.assertEqual(row.missing_value_rows_removed, 3)
        self.assertEqual(row.clean_missing_count, 0)
        self.assertEqual(row.missing_pct, 0)
        self.assertEqual(row.valid_observations, 2)
        self.assertEqual(row.raw_rows, row.clean_rows + row.safe_empty_rows_removed + row.exact_duplicate_rows_removed + row.missing_value_rows_removed)
        review = pd.read_csv(root / 'data/audit/observations_for_review.csv')
        self.assertEqual(review.reason.str.contains('removed missing value').sum(), 3)

    def test_reproducibility_discovery_and_stale_output(self):
        root, _ = self.process("date,INDPRO\n2020-01-01,1\n2020-02-01,2\n2020-03-01,3\n")
        outputs = list((root / "data/audit").glob("*.csv")) + list((root / "data/cleaned").glob("*.csv"))
        before = [p.read_bytes() for p in outputs]
        with contextlib.redirect_stdout(io.StringIO()):
            run(root, REGISTRY[:1])
        self.assertEqual(before, [p.read_bytes() for p in outputs])
        (root / "data/INDPRO.csv").write_text("date,value\n2020-01-01,9\n")
        (root / "data/raw/extra.csv").write_text("anything\n")
        with contextlib.redirect_stdout(io.StringIO()):
            audit = run(root, REGISTRY[:2])
        self.assertEqual(audit.status.tolist(), ["FAILED", "FAILED"])
        self.assertIn("Raw copies differ", audit.iloc[0].error)
        self.assertIn("stale", audit.iloc[0].warning)
        self.assertIn("Missing expected", audit.iloc[1].error)
        self.assertTrue(pd.read_csv(root / "data/cleaned/series_metadata.csv").empty)
        inventory = pd.read_csv(root / "data/audit/raw_file_inventory.csv")
        self.assertEqual(inventory.kind.eq("unexpected").sum(), 1)


if __name__ == "__main__":
    unittest.main()
