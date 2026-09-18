"""Audit and coverage tables; counts describe retained canonical rows."""

from dataclasses import asdict

import pandas as pd


def audit_record(series):
    return {
        **asdict(series), "file_exists": False, "rows_raw": None,
        "valid_observations": None, "missing_values": None, "missing_pct": None,
        "first_date": pd.NaT, "last_date": pd.NaT, "duplicate_dates": None,
        "conflicting_duplicate_dates": None, "detected_date_column": "",
        "detected_value_column": "", "load_status": "FAILED", "warning": "",
        "inferred_frequency": "unknown",
    }


def coverage_table(audit):
    coverage = audit[["series_id", "first_date", "last_date", "valid_observations", "missing_pct"]].copy()
    coverage["history_years"] = (
        pd.to_datetime(coverage.last_date) - pd.to_datetime(coverage.first_date)
    ).dt.total_seconds() / (86400 * 365.25)
    return coverage[["series_id", "first_date", "last_date", "valid_observations", "history_years", "missing_pct"]]
