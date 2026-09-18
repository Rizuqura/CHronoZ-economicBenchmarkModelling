"""Conservative local discovery and CSV schema handling."""

import csv
import hashlib
import shutil
from pathlib import Path

import pandas as pd

from .registry import Series


def discover(root: Path, series: Series) -> tuple[Path, list[str]]:
    target = root / series.raw_path
    candidates = sorted(
        p for p in (root / "data").rglob("*")
        if p.is_file() and p.name.casefold() == f"{series.series_id}.csv".casefold()
    )
    if not candidates:
        raise FileNotFoundError(f"Missing {series.raw_path}")
    hashes = {hashlib.sha256(p.read_bytes()).hexdigest() for p in candidates}
    if len(hashes) != 1:
        raise ValueError("Different raw copies found: " + ", ".join(str(p.relative_to(root)) for p in candidates))
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(candidates[0], target)
    return target, []


def read_csv(path: Path) -> pd.DataFrame:
    # Inspect records before pandas can mangle duplicate headers or infer an index.
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
        normalized = [c.strip().casefold() for c in header]
        if not header or len(set(normalized)) != len(header):
            raise ValueError("Empty or duplicate CSV headers")
        for line, row in enumerate(reader, 2):
            if len(row) != len(header):
                raise ValueError(f"CSV record {line}: expected {len(header)} fields, found {len(row)}")
    return pd.read_csv(path, dtype=str, keep_default_na=False, skip_blank_lines=False, encoding="utf-8-sig")


def detect_columns(raw: pd.DataFrame, series_id: str) -> tuple[str, str, list[str]]:
    lookup = {c.strip().casefold(): c for c in raw.columns}
    dates = [lookup[k] for k in ("date", "observation_date") if k in lookup]
    if len(dates) != 1:
        raise ValueError(f"Expected one DATE/date/observation_date column, found {dates}")
    date = dates[0]
    remaining = [c for c in raw.columns if c != date]
    value = lookup.get(series_id.casefold()) or lookup.get("value")
    if value is None and len(remaining) == 1:
        value = remaining[0]
    if value is None or value == date:
        raise ValueError(f"Ambiguous value columns: {remaining}")
    extra = [c for c in remaining if c != value]
    warnings = [f"Extra columns preserved in raw only: {extra}"] if extra else []
    return date, value, warnings
