"""Validation without frequency conversion, filling, or economic transforms."""

import numpy as np
import pandas as pd


def infer_frequency(dates: pd.Series) -> str:
    gaps = dates.dropna().drop_duplicates().sort_values().diff().dt.total_seconds().dropna() / 86400
    if len(gaps) < 2:
        return "unknown"
    for name, low, high in (
        ("daily", 1, 1), ("weekly", 7, 7), ("monthly", 28, 31),
        ("quarterly", 89, 92), ("annual", 365, 366),
    ):
        if gaps.between(low, high).mean() >= 0.8:
            return name
    return "irregular"


def validate(raw, date_column, value_column, expected_frequency):
    warnings = []
    dates = pd.to_datetime(raw[date_column].str.strip(), errors="coerce", format="mixed")
    values = pd.to_numeric(raw[value_column].str.strip(), errors="coerce")
    frame = pd.DataFrame({"date": dates, "value": values})
    invalid_dates = int(dates.isna().sum())
    tokens = raw[value_column].str.strip().str.casefold()
    missing_tokens = tokens.isin(["", ".", "na", "n/a", "nan", "null", "none"])
    coerced = int((values.isna() & ~missing_tokens).sum())
    nonfinite = int((values.notna() & ~np.isfinite(values)).sum())
    if invalid_dates:
        warnings.append(f"Invalid/missing dates={invalid_dates}; retained as blank dates in long and wide")
    if coerced:
        warnings.append(f"Unrecognized numeric tokens coerced to NaN={coerced}; originals retained in raw")
    if nonfinite:
        warnings.append(f"Non-finite numeric values={nonfinite}; retained")
    duplicate_dates = int(dates[dates.notna() & dates.duplicated(keep=False)].nunique())
    conflicts = int(frame.dropna(subset=["date"]).groupby("date")["value"].nunique(dropna=False).gt(1).sum())
    # Only full raw-record duplicates with valid dates qualify for removal.
    exact = raw.duplicated() & dates.notna()
    removed = int(exact.sum())
    frame = frame.loc[~exact].sort_values("date", kind="stable").reset_index(drop=True)
    if duplicate_dates:
        warnings.append(f"Duplicate dates={duplicate_dates}; exact duplicate rows removed={removed}")
    if conflicts:
        warnings.append(f"Conflicting duplicate dates={conflicts}; all distinct records retained; wide has repeated dates")
    missing = int(frame.value.isna().sum())
    if missing:
        warnings.append(f"Missing values={missing}")
    frequency = infer_frequency(frame.date)
    if frequency != expected_frequency:
        warnings.append(f"Frequency expected={expected_frequency}, inferred={frequency}")
    metrics = {
        "rows_raw": len(raw), "rows_output": len(frame),
        "valid_observations": int((frame.date.notna() & frame.value.notna() & np.isfinite(frame.value)).sum()),
        "missing_values": missing, "missing_pct": 100 * missing / len(frame) if len(frame) else float("nan"),
        "first_date": frame.date.min(), "last_date": frame.date.max(),
        "duplicate_dates": duplicate_dates, "conflicting_duplicate_dates": conflicts,
        "inferred_frequency": frequency, "invalid_dates": invalid_dates,
        "coerced_values": coerced, "nonfinite_values": nonfinite, "exact_duplicate_rows_removed": removed,
    }
    if frame.empty:
        warnings.append("No observations")
    return frame, metrics, warnings
