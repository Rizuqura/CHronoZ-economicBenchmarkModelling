#!/usr/bin/env python3
"""Generate ChronoZ series- and category-level macro dataset iterations.

Run from the repository root:
    python scripts/generate_macro_datasets.py

This generator is deliberately separate from the baseline notebooks and cleaned data.
It uses the current research-use transformation registry documented in
notebook/deltaAnalysis/CURRENT_MODEL_NOTES.md. It does NOT claim to reproduce
the inaccessible full code of analysis.ipynb; see limitations in the audit output.

Feature definitions:
- Per-series transformed movement follows the approved registry below.
- Spread is the historical standardized score of the transformed movement:
      (transformed_t - historical_mean) / historical_sample_std
  Calibration is retrospective/full-history in this research iteration, not a
  leakage-free point-in-time backtest.
- Category spread is the cross-sectional mean of available member series spreads.
- Series ROC4 is computed from the transformed series at a lag of four native
  observations, except weekly series use the last observation at or before the
  snapshot date minus four calendar months. Quarterly series use four native
  quarterly observations. ROC is x_t / x_lag - 1 where valid and nonzero.
- Interactions are spread * ROC4. Category interaction is category spread times
  the mean ROC4 of available category members.

IMPORTANT:
The user's notebook also discusses a polynomial comparison. The category CSV schema
has no polynomial columns, and the exact polynomial implementation could not be
retrieved through the GitHub connector. This script therefore records category
means as the category-level spread and does not silently inject polynomial terms
into the 13-column output. Confirm/reconcile this with analysis.ipynb before treating
these outputs as a faithful benchmark reproduction.

Point-in-time limitation:
Cleaned FRED CSVs contain observation dates and values, not release dates/vintages.
Snapshots therefore use observations dated on/before snapshot date; they cannot
guarantee that each value had actually been published by that snapshot date.
"""

from __future__ import annotations

import argparse
import calendar
import json
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "cleaned"
OUTPUT_DIR = ROOT / "data" / "derived" / "iterations"
METADATA_PATH = DATA_DIR / "series_metadata.csv"
START_SNAPSHOT = "2010-03-25"

# Model family/transform choices grounded in CURRENT_MODEL_NOTES.md.
# Values not explicitly listed as special are assigned the documented preferred
# change from the notes. This is a first research iteration, not production code.
LOG_DELTA = {
    "HOUST", "PERMIT", "JTSJOL", "OPHNFB", "PPIFID", "IMPGSC1", "EXPGSC1",
    "PCEPILFE", "PCEPI", "CPIAUCSL", "CPILFESL", "PPIACO", "PCEC96",
    "W875RX1", "RRSFS", "CES0500000003", "INDPRO", "IPMAN", "TOTALSL",
    "BUSLOANS", "M2SL", "RPI", "PAYEMS", "ICSA", "WALCL", "WRESBAL",
    "TOTRESNS",
}
LEVEL_DELTA = {
    "DRSDCILM", "DRTSCILM", "DRBLACBS", "TCU", "CIVPART", "FEDFUNDS",
    "AWHMAN", "AWHAETP", "UNRATE",
}
# Preserve native levels as a supporting measure where the notes require them;
# the standardized movement feature itself is still based on the selected delta.
SIGNED_SURVEY_LEVELS = {"DRSDCILM", "DRTSCILM"}
ALTERNATIVE_MODELS = {
    "AWHAETP": "DISCRETE_DELTA",
    "ICSA": "ROBUST_DELTA",
    "WALCL": "REGIME_ROBUST_DELTA",
    "WRESBAL": "REGIME_ROBUST_DELTA",
    "TOTRESNS": "STRUCTURAL_EPOCH_ROBUST_DELTA",
    "UNRATE": "DISCRETE_PLUS_SHOCK",
}
ROBUST_CALIBRATION = {"PCEC96", "ICSA", "WALCL", "WRESBAL", "TOTRESNS"}
REGIME_SERIES = {"WALCL", "WRESBAL", "TOTRESNS"}
DISCRETE_SERIES = {"AWHAETP", "UNRATE"}
POLYNOMIAL_NOTE = (
    "Polynomial terms are not emitted: the final 13-column category schema has "
    "no polynomial columns, and exact analysis.ipynb implementation was unavailable."
)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start", default=START_SNAPSHOT, help="First snapshot date YYYY-MM-DD")
    p.add_argument("--end", default=None, help="Last snapshot date YYYY-MM-DD; defaults to latest available month-end snapshot <= max data date")
    p.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Output directory")
    return p.parse_args()


def add_months(ts: pd.Timestamp, months: int) -> pd.Timestamp:
    month_index = ts.year * 12 + (ts.month - 1) + months
    year, month0 = divmod(month_index, 12)
    month = month0 + 1
    day = min(ts.day, calendar.monthrange(year, month)[1])
    return pd.Timestamp(year=year, month=month, day=day)


def make_snapshots(start: str, end: str) -> list[pd.Timestamp]:
    start_ts, end_ts = pd.Timestamp(start), pd.Timestamp(end)
    dates = []
    cur = start_ts
    while cur <= end_ts:
        dates.append(cur)
        cur = add_months(cur, 1)
    return dates


def load_metadata() -> pd.DataFrame:
    meta = pd.read_csv(METADATA_PATH)
    required = {"series_id", "category", "expected_frequency", "clean_file"}
    missing = required - set(meta.columns)
    if missing:
        raise ValueError(f"Metadata missing required columns: {sorted(missing)}")
    return meta


def resolve_csv(series_id: str, clean_file: str) -> Path:
    # Metadata currently uses Windows separators; normalize for Linux/macOS too.
    candidate = DATA_DIR / Path(str(clean_file).replace("\\", "/")).name
    if not candidate.exists():
        candidate = DATA_DIR / f"{series_id}.csv"
    if not candidate.exists():
        raise FileNotFoundError(f"Cannot find cleaned series CSV for {series_id}: {candidate}")
    return candidate


def load_series(meta: pd.DataFrame) -> dict[str, pd.Series]:
    out = {}
    for row in meta.itertuples(index=False):
        path = resolve_csv(row.series_id, row.clean_file)
        frame = pd.read_csv(path)
        date_col = next((c for c in frame.columns if c.lower() in {"date", "observation_date"}), None)
        value_col = next((c for c in frame.columns if c.lower() == "value"), None)
        if date_col is None or value_col is None:
            raise ValueError(f"{path} must contain date,value columns; got {list(frame.columns)}")
        frame[date_col] = pd.to_datetime(frame[date_col], errors="coerce")
        frame[value_col] = pd.to_numeric(frame[value_col], errors="coerce")
        frame = frame.dropna(subset=[date_col, value_col]).sort_values(date_col)
        frame = frame.drop_duplicates(subset=[date_col], keep="last")
        out[row.series_id] = pd.Series(frame[value_col].to_numpy(), index=frame[date_col], name=row.series_id)
    return out


def transform_series(series_id: str, raw: pd.Series) -> pd.Series:
    raw = raw.astype(float).sort_index()
    # Do not bridge missing native periods: data are differenced only between
    # consecutive rows as supplied by the cleaned series.
    if series_id in LOG_DELTA:
        valid = raw.where(raw > 0)
        return (100.0 * (np.log(valid) - np.log(valid.shift(1)))).rename(series_id)
    if series_id in LEVEL_DELTA:
        delta = raw.diff()
        if series_id == "FEDFUNDS":
            # Keep percentage-point units consistent with the notebook notes.
            return delta.rename(series_id)
        return delta.rename(series_id)
    # Fallback is explicit rather than silently using an arbitrary transform.
    raise ValueError(f"No transformation registered for series {series_id}")


def robust_keep_mask(x: pd.Series) -> pd.Series:
    vals = x.dropna()
    if len(vals) < 8:
        return pd.Series(True, index=x.index)
    med = vals.median()
    mad = (vals - med).abs().median()
    if not np.isfinite(mad) or mad == 0:
        return pd.Series(True, index=x.index)
    modified_z = 0.6745 * (x - med) / mad
    return modified_z.abs().le(3.5).fillna(True)


def historical_spread(series_id: str, transformed: pd.Series) -> pd.Series:
    x = transformed.copy()
    if series_id in ROBUST_CALIBRATION:
        keep = robust_keep_mask(x)
        calibration = x[keep & x.notna()]
    else:
        calibration = x.dropna()
    if len(calibration) < 2:
        return pd.Series(np.nan, index=x.index, name=series_id)
    mean = calibration.mean()
    std = calibration.std(ddof=1)
    if not np.isfinite(std) or std == 0:
        return pd.Series(np.nan, index=x.index, name=series_id)
    # Score every observation, including observations excluded from calibration.
    return ((x - mean) / std).rename(series_id)


def roc4_native(series_id: str, transformed: pd.Series, frequency: str) -> pd.Series:
    x = transformed.sort_index()
    if frequency == "weekly":
        vals = []
        dates = x.index
        for date, value in x.items():
            target = add_months(pd.Timestamp(date), -4)
            eligible = x.loc[x.index <= target].dropna()
            if len(eligible) == 0 or not np.isfinite(value):
                vals.append(np.nan)
                continue
            lag = eligible.iloc[-1]
            vals.append(value / lag - 1 if lag != 0 else np.nan)
        return pd.Series(vals, index=x.index, name=series_id)
    lag = x.shift(4)
    denom = lag.replace(0, np.nan)
    return (x / denom - 1).rename(series_id)


def asof_value(series: pd.Series, snapshot: pd.Timestamp) -> float:
    available = series.loc[series.index <= snapshot].dropna()
    return float(available.iloc[-1]) if not available.empty else np.nan


def build_datasets(meta: pd.DataFrame, raw: dict[str, pd.Series], snapshots: list[pd.Timestamp]) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    spread_by_series = {}
    roc_by_series = {}
    for row in meta.itertuples(index=False):
        sid = row.series_id
        transformed = transform_series(sid, raw[sid])
        spread_by_series[sid] = historical_spread(sid, transformed)
        roc_by_series[sid] = roc4_native(sid, transformed, str(row.expected_frequency).lower())

    series_rows = []
    category_rows = []
    categories = list(dict.fromkeys(meta["category"].tolist()))
    for snap in snapshots:
        spread_row = {"snapshot_date": snap.strftime("%Y-%m-%d")}
        interaction_row = {}
        category_spreads = {}
        category_rocs = {}
        for row in meta.itertuples(index=False):
            sid = row.series_id
            s = asof_value(spread_by_series[sid], snap)
            roc = asof_value(roc_by_series[sid], snap)
            spread_row[f"{sid}_spread"] = s
            interaction_row[f"{sid}_spread_x_roc4"] = s * roc if np.isfinite(s) and np.isfinite(roc) else np.nan
            category_spreads.setdefault(row.category, []).append(s)
            category_rocs.setdefault(row.category, []).append(roc)
        for category in categories:
            vals = pd.Series(category_spreads[category], dtype=float)
            rocs = pd.Series(category_rocs[category], dtype=float)
            category_rows.append({
                "snapshot_date": snap.strftime("%Y-%m-%d"),
                "category": category,
                "category_spread": vals.mean(skipna=True),
                "category_roc4": rocs.mean(skipna=True),
            })
        series_rows.append({**spread_row, **interaction_row})

    series_df = pd.DataFrame(series_rows)
    series_cols = ["snapshot_date"]
    ids = meta["series_id"].tolist()
    series_cols += [f"{sid}_spread" for sid in ids]
    series_cols += [f"{sid}_spread_x_roc4" for sid in ids]
    series_df = series_df.reindex(columns=series_cols)

    cat_long = pd.DataFrame(category_rows)
    category_df = pd.DataFrame({"snapshot_date": [s.strftime("%Y-%m-%d") for s in snapshots]})
    for category in categories:
        pivot = cat_long.pivot(index="snapshot_date", columns="category", values="category_spread")
        category_df[f"{category}_spread"] = category_df["snapshot_date"].map(pivot[category].to_dict())
    for category in categories:
        pivot = cat_long.pivot(index="snapshot_date", columns="category", values="category_roc4")
        category_df[f"{category}_spread_x_roc4"] = category_df[f"{category}_spread"] * category_df["snapshot_date"].map(pivot[category].to_dict())
    category_cols = ["snapshot_date"] + [f"{c}_spread" for c in categories] + [f"{c}_spread_x_roc4" for c in categories]
    category_df = category_df.reindex(columns=category_cols)

    audit = {
        "generated_utc": pd.Timestamp.utcnow().isoformat(),
        "snapshots": len(snapshots),
        "series_count": len(ids),
        "categories": categories,
        "series_columns": len(series_df.columns),
        "category_columns": len(category_df.columns),
        "calibration": "Full-history mean/sample SD; PCEC96, ICSA, WALCL, WRESBAL, TOTRESNS use robust outlier exclusion from calibration only.",
        "release_date_vintages": "Unavailable in cleaned CSVs; observation-date cutoff is not release-aware.",
        "polynomial": POLYNOMIAL_NOTE,
        "alternative_models": ALTERNATIVE_MODELS,
        "warnings": [
            "Retrospective full-history normalization is not leakage-free for historical ML backtests.",
            "Current spread definition is transformed-change z-score against historical benchmark.",
            "Exact polynomial implementation from analysis.ipynb was not retrieved; no polynomial terms added.",
            "Regime-specific and discrete model families are approximated by documented robust/discrete handling; review before production.",
        ],
    }
    return series_df, category_df, audit


def main() -> None:
    args = parse_args()
    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    meta = load_metadata()
    raw = load_series(meta)
    latest = max(s.dropna().index.max() for s in raw.values())
    end = pd.Timestamp(args.end) if args.end else pd.Timestamp(year=latest.year, month=latest.month, day=25)
    snapshots = make_snapshots(args.start, end.strftime("%Y-%m-%d"))
    if not snapshots:
        raise ValueError("No snapshots generated; check --start and --end.")

    series_df, category_df, audit = build_datasets(meta, raw, snapshots)
    series_path = out_dir / "macro_series_dataset_v0.1.csv"
    category_path = out_dir / "macro_category_dataset_v0.1.csv"
    audit_path = out_dir / "macro_dataset_generation_audit.json"
    series_df.to_csv(series_path, index=False, float_format="%.10g")
    category_df.to_csv(category_path, index=False, float_format="%.10g")
    audit_path.write_text(json.dumps(audit, indent=2), encoding="utf-8")

    # Basic output validation
    assert series_df.shape[1] == 73, f"Expected 73 series columns, got {series_df.shape[1]}"
    assert category_df.shape[1] == 13, f"Expected 13 category columns, got {category_df.shape[1]}"
    assert series_df["snapshot_date"].is_unique and category_df["snapshot_date"].is_unique
    print(f"Series dataset: {series_path} shape={series_df.shape}")
    print(f"Category dataset: {category_path} shape={category_df.shape}")
    print(f"Audit: {audit_path}")
    print("\nSeries preview:")
    print(series_df.iloc[:3, :8].to_string(index=False))
    print("\nCategory preview:")
    print(category_df.head(3).to_string(index=False))


if __name__ == "__main__":
    main()
