"""Reproducible, offline ingestion orchestration."""

from pathlib import Path

import pandas as pd

from .audit import audit_record, coverage_table
from .io import detect_columns, discover, read_csv
from .registry import REGISTRY
from .validation import validate


LONG_COLUMNS = ["date", "series_id", "value", "category", "expected_frequency", "source"]


def build_wide(long, series_ids):
    if long.empty:
        return pd.DataFrame(columns=["date", *series_ids])
    work = long.copy()
    # An occurrence index preserves conflicts without aggregation or Cartesian joins.
    # It is internal only: repeated dates in the inspection CSV are documented.
    work["_occurrence"] = work.groupby(["date", "series_id"], dropna=False).cumcount()
    wide = work.pivot(index=["date", "_occurrence"], columns="series_id", values="value")
    wide = wide.reindex(columns=series_ids).sort_index().reset_index().drop(columns="_occurrence")
    wide.columns.name = None
    return wide


def run(root: Path, registry=REGISTRY):
    root = Path(root).resolve()
    records, frames = [], []
    for index, series in enumerate(registry, 1):
        record = audit_record(series)
        warnings = []
        record["file_exists"] = any(
            p.is_file() and p.name.casefold() == f"{series.series_id}.csv".casefold()
            for p in (root / "data").rglob("*")
        )
        try:
            path, discovered_warnings = discover(root, series)
            warnings.extend(discovered_warnings)
            raw = read_csv(path)
            record["rows_raw"] = len(raw)
            date_column, value_column, schema_warnings = detect_columns(raw, series.series_id)
            warnings.extend(schema_warnings)
            record.update(detected_date_column=date_column, detected_value_column=value_column)
            frame, metrics, validation_warnings = validate(raw, date_column, value_column, series.expected_frequency)
            record.update(metrics)
            warnings.extend(validation_warnings)
            record["load_status"] = "WARNING" if warnings else "OK"
            for field in ("series_id", "category", "expected_frequency", "source"):
                frame[field] = getattr(series, field)
            frames.append(frame[LONG_COLUMNS])
        except (OSError, ValueError, TypeError, pd.errors.ParserError) as exc:
            record["load_status"] = "FAILED"
            warnings.append(f"{type(exc).__name__}: {exc}")
        record["warning"] = "; ".join(warnings)
        records.append(record)
        start = str(record["first_date"])[:10] if pd.notna(record["first_date"]) else "n/a"
        end = str(record["last_date"])[:10] if pd.notna(record["last_date"]) else "n/a"
        detail = f"{start} -> {end} | {record['valid_observations']} obs"
        if warnings:
            detail += " | " + record["warning"]
        print(f"[{index:02}/{len(registry)}] {series.series_id:<12} {record['load_status']:<7} {detail}")

    long = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=LONG_COLUMNS)
    long = long.sort_values(["date", "series_id"], kind="stable").reset_index(drop=True)
    audit = pd.DataFrame(records)
    outputs = {
        "Long dataset": ("data/interim/us_macro_long.csv", long),
        "Wide dataset": ("data/interim/us_macro_wide.csv", build_wide(long, [s.series_id for s in registry])),
        "Audit": ("outputs/audits/us_macro_data_audit.csv", audit),
        "Coverage": ("outputs/audits/us_macro_coverage.csv", coverage_table(audit)),
    }
    for relative, table in outputs.values():
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(".csv.tmp")
        table.to_csv(temporary, index=False, date_format="%Y-%m-%d", lineterminator="\n")
        temporary.replace(target)
    failed = int(audit.load_status.eq("FAILED").sum())
    print("\n========================================\nCHronoZ DATA INGESTION COMPLETE\n========================================")
    print(f"Expected series: {len(registry)}\nLoaded: {len(registry) - failed}\nWarnings: {audit.load_status.eq('WARNING').sum()}\nFailed: {failed}")
    for label, (relative, _) in outputs.items():
        print(f"{label}: {root / relative}")
    return audit
