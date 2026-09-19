"""Offline technical cleaning of local FRED CSVs. All active logic lives here."""

from dataclasses import asdict, dataclass
import csv
import hashlib
import json
from pathlib import Path
import sys
import warnings as python_warnings

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Series:
    series_id: str
    name: str
    category: str
    expected_frequency: str
    source: str
    raw_file: str
    notes: str = "Original FRED observations; no economic transformations."


_GROUPS = {
    "growth_activity": [
        ("INDPRO", "Industrial Production Index", "monthly"),
        ("IPMAN", "Industrial Production: Manufacturing", "monthly"),
        ("PCEC96", "Real Personal Consumption Expenditures", "monthly"),
        ("W875RX1", "Real Personal Income Excluding Current Transfer Receipts", "monthly"),
        ("RPI", "Real Personal Income", "monthly"),
        ("RRSFS", "Advance Real Retail and Food Services Sales", "monthly"),
        ("HOUST", "Housing Starts", "monthly"),
        ("PERMIT", "Building Permits", "monthly"),
    ],
    "labor": [
        ("PAYEMS", "All Employees: Total Nonfarm Payrolls", "monthly"),
        ("UNRATE", "Unemployment Rate", "monthly"),
        ("ICSA", "Initial Claims", "weekly"),
        ("AWHAETP", "Average Weekly Hours: Total Private", "monthly"),
        ("AWHMAN", "Average Weekly Hours: Manufacturing", "monthly"),
        ("JTSJOL", "Job Openings: Total Nonfarm", "monthly"),
        ("CIVPART", "Labor Force Participation Rate", "monthly"),
        ("CES0500000003", "Average Hourly Earnings: Total Private", "monthly"),
    ],
    "inflation": [
        ("CPIAUCSL", "Consumer Price Index: All Urban Consumers", "monthly"),
        ("CPILFESL", "Core CPI", "monthly"),
        ("PCEPI", "PCE Price Index", "monthly"),
        ("PCEPILFE", "Core PCE Price Index", "monthly"),
        ("PPIFID", "Producer Price Index: Final Demand", "monthly"),
        ("PPIACO", "Producer Price Index: All Commodities", "monthly"),
    ],
    "credit": [
        ("BUSLOANS", "Commercial and Industrial Loans", "monthly"),
        ("TOTALSL", "Total Consumer Credit Owned and Securitized", "monthly"),
        ("DRTSCILM", "SLOOS: Banks Tightening C&I Lending Standards", "quarterly"),
        ("DRSDCILM", "SLOOS: Stronger Demand for C&I Loans", "quarterly"),
        ("DRBLACBS", "Delinquency Rate on Business Loans", "quarterly"),
    ],
    "policy_liquidity": [
        ("FEDFUNDS", "Federal Funds Effective Rate", "monthly"),
        ("TOTRESNS", "Reserves of Depository Institutions: Total", "monthly"),
        ("WRESBAL", "Reserve Balances with Federal Reserve Banks", "weekly"),
        ("WALCL", "Federal Reserve Total Assets", "weekly"),
        ("M2SL", "M2 Money Stock", "monthly"),
    ],
    "external_structural": [
        ("EXPGSC1", "Real Exports of Goods and Services", "quarterly"),
        ("IMPGSC1", "Real Imports of Goods and Services", "quarterly"),
        ("OPHNFB", "Nonfarm Business Sector Labor Productivity", "quarterly"),
        ("TCU", "Capacity Utilization: Total Industry", "monthly"),
    ],
}

REGISTRY = tuple(
    Series(sid, name, category, frequency, "FRED", f"data/raw/{category}/{sid}.csv")
    for category, entries in _GROUPS.items()
    for sid, name, frequency in entries
)

ROOT = Path(__file__).resolve().parent
MISSING = {"", ".", "na", "n/a", "nan", "null", "none"}
GAP_BANDS = {"daily": (1, 1), "weekly": (7, 7), "monthly": (28, 31),
             "quarterly": (89, 92), "annual": (365, 366)}


def encoded(value):
    return json.dumps(value, ensure_ascii=False, default=str)


def missing_mask(column):
    return column.str.strip().str.casefold().isin(MISSING)


def parse_dates(column):
    # Reject numeric-only strings: pandas otherwise treats some as years/timestamps.
    text = column.str.strip()
    plausible = text.str.contains(r"[-/]|[A-Za-z]", regex=True) | text.str.fullmatch(r"\d{8}")
    with python_warnings.catch_warnings():
        python_warnings.simplefilter("ignore", UserWarning)
        result = pd.to_datetime(text.where(plausible), errors="coerce", format="mixed")
    if not pd.api.types.is_datetime64_any_dtype(result.dtype) or getattr(result.dt, "tz", None) is not None:
        raise ValueError("Mixed or timezone-bearing dates require manual review")
    if (result.dropna() != result.dropna().dt.normalize()).any():
        raise ValueError("Intraday timestamps require manual review; refusing to truncate time")
    return result


def inventory(root, registry):
    files = sorted(set((root / "data/raw").rglob("*.csv")) | set((root / "data").glob("*.csv")))
    expected = {s.series_id.casefold() for s in registry}
    rows = []
    for path in files:
        row = {"path": str(path.relative_to(root)), "series_id": path.stem,
               "kind": "expected" if path.stem.casefold() in expected else "unexpected", "error": ""}
        try:
            row["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            with path.open(encoding="utf-8-sig", newline="") as handle:
                records = list(csv.reader(handle, strict=True))
            row.update(first_record=encoded(records[0] if records else []), csv_records=len(records))
        except (OSError, UnicodeError, csv.Error) as exc:
            row["error"] = str(exc)
        rows.append(row)
    return files, pd.DataFrame(rows, columns=["path", "series_id", "kind", "sha256", "first_record", "csv_records", "error"])


def inspect_csv(path, series_id, info, warnings):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        records = list(csv.reader(handle, strict=True))
    if not records:
        raise ValueError("Empty CSV file")
    # Only skip a preamble if a recognizable header can be identified confidently.
    headers = [i for i, row in enumerate(records[:50])
               if any(c.strip().casefold() in {"date", "observation_date"} for c in row)
               and len(row) >= 2]
    start = headers[0] if headers else 0
    info["metadata_rows"] = start
    info["metadata_preview"] = encoded(records[:start])
    if start:
        warnings.append(f"Metadata preamble records={start}; preserved in raw and audit")
    header = records[start]
    normalized = [c.strip().casefold() for c in header]
    if len(header) < 2 or len(normalized) != len(set(normalized)):
        raise ValueError("Missing, insufficient, or duplicate CSV headers")
    body = records[start + 1:]
    info["raw_rows"] = len(body)
    # Blank records are retained for explicit safe-removal accounting.
    body = [[""] * len(header) if not row else row for row in body]
    malformed = [i + start + 2 for i, row in enumerate(body) if len(row) != len(header)]
    if malformed:
        info["malformed_record_numbers"] = encoded(malformed)
        raise ValueError(f"Inconsistent record widths (possible footer/metadata) at records {malformed[:10]}")
    raw = pd.DataFrame(body, columns=header, dtype=str)
    info.update(raw_columns=encoded(header), raw_dtypes=encoded({c: str(t) for c, t in raw.dtypes.items()}),
                first_five_rows=raw.head().to_json(orient="records"), last_five_rows=raw.tail().to_json(orient="records"),
                unnamed_columns=encoded([c for c in header if not c.strip() or c.lower().startswith("unnamed")]),
                empty_columns=encoded([c for c in header if missing_mask(raw[c]).all()]),
                entirely_null_rows=int(raw.apply(missing_mask).all(axis=1).sum()),
                duplicated_rows=int(raw.duplicated().sum()))
    if raw.empty:
        raise ValueError("Zero-row dataset")
    return raw, start


def detect_schema(raw, series_id, info, warnings):
    direct = [c for c in raw if c.strip().casefold() in {"date", "observation_date"}]
    if len(direct) > 1:
        raise ValueError(f"Ambiguous date columns: {direct}")
    if direct:
        date = direct[0]
    else:
        rates = {c: float(parse_dates(raw[c]).notna().mean()) for c in raw}
        best = max(rates.values())
        candidates = [c for c, rate in rates.items() if rate == best]
        info["date_candidate_rates"] = encoded(rates)
        if best < 0.8 or len(candidates) != 1:
            raise ValueError(f"Low-confidence or ambiguous date detection: {rates}")
        date = candidates[0]
        warnings.append(f"Date column inferred by parsing: {date}")
    dates = parse_dates(raw[date])
    info.update(detected_date_column=date, date_parse_success_rate=float(dates.notna().mean()))
    candidates = [c for c in raw if c != date and c.strip() and
                  not c.strip().casefold().startswith("unnamed") and c.strip().casefold() not in {"index", "level_0"}]
    rates = {}
    for c in candidates:
        useful = ~missing_mask(raw[c])
        rates[c] = float(pd.to_numeric(raw.loc[useful, c].str.strip(), errors="coerce").notna().mean()) if useful.any() else 0.0
    exact = [c for c in candidates if c.strip().casefold() == series_id.casefold()]
    named = [c for c in candidates if c.strip().casefold() == "value"]
    plausible = [c for c in candidates if rates[c] >= 0.8]
    if exact:
        value = exact[0]
    elif named:
        value = named[0]
    elif len(plausible) == 1:
        value = plausible[0]
        warnings.append(f"Value column inferred by numeric parsing: {value}")
    elif len(candidates) == 1:
        value = candidates[0]
        warnings.append(f"Only remaining value candidate selected: {value}")
    else:
        raise ValueError(f"Ambiguous or absent numeric observation column: {rates}")
    if len(plausible) > 1:
        warnings.append(f"Multiple plausible numeric columns={plausible}; selected {value} by header priority")
    extra = [c for c in raw if c not in {date, value}]
    if extra:
        warnings.append(f"Extra columns preserved in raw and review records only: {extra}")
    values = pd.to_numeric(raw[value].str.strip().mask(missing_mask(raw[value])), errors="coerce")
    info.update(detected_value_column=value, numeric_parse_success_rate=rates[value])
    if info["date_parse_success_rate"] < 0.8:
        warnings.append("Date parse success below 80%")
    if rates[value] < 0.8:
        warnings.append("Numeric parse success below 80% (excluding recognized missing markers)")
    return date, value, dates, values


def infer_frequency(dates):
    gaps = dates.dropna().drop_duplicates().sort_values().diff().dt.total_seconds().dropna() / 86400
    if len(gaps) < 2:
        return "unknown"
    for name, (low, high) in GAP_BANDS.items():
        if gaps.between(low, high).mean() >= 0.8:
            return name
    return "irregular"


def clean_series(raw, series, info, warnings, start):
    date, value, dates, values = detect_schema(raw, series.series_id, info, warnings)
    recognized_missing = missing_mask(raw[value])
    invalid = dates.isna()
    nonnumeric = values.isna() & ~recognized_missing
    infinite = values.notna() & ~np.isfinite(values)
    # Technical heuristic only; suspicious values are retained, never winsorized.
    huge = np.isfinite(values) & (values.abs() >= 1e100)
    duplicate = dates.notna() & dates.duplicated(keep=False)
    counts = pd.DataFrame({"date": dates, "value": values}).dropna(subset=["date"]).groupby("date").value.nunique(dropna=False)
    conflict_dates = counts[counts > 1].index
    info.update(invalid_date_count=int((invalid & ~missing_mask(raw[date])).sum()),
                missing_date_count=int((invalid & missing_mask(raw[date])).sum()),
                nonnumeric_value_count=int(nonnumeric.sum()), infinite_value_count=int(infinite.sum()),
                extreme_numeric_count=int(huge.sum()), raw_missing_count=int(recognized_missing.sum()),
                duplicate_dates=int(dates[duplicate].nunique()), conflicting_duplicate_dates=bool(len(conflict_dates)),
                conflicting_duplicate_date_count=len(conflict_dates), originally_sorted=dates.dropna().is_monotonic_increasing)

    # Unknown text is useful evidence: remove invalid-date rows only when ALL other
    # fields are recognized missing. Preserve footer text for human review.
    other = raw.drop(columns=[date])
    safe_empty = invalid & other.apply(missing_mask).all(axis=1)
    exact = raw.duplicated() & ~safe_empty
    # The training-input policy excludes NaN values, including failed numeric
    # parses. Count removals separately from blank rows and exact duplicates.
    missing_removed = values.isna() & ~(safe_empty | exact)
    keep = ~(safe_empty | exact | missing_removed)
    clean = pd.DataFrame({"date": dates, "value": values}).loc[keep].sort_values("date", kind="stable").reset_index(drop=True)
    info.update(safe_empty_rows_removed=int(safe_empty.sum()), exact_duplicate_rows_removed=int(exact.sum()),
                missing_value_rows_removed=int(missing_removed.sum()),
                retained_invalid_dates=int(clean.date.isna().sum()), clean_rows=len(clean))
    reasons = pd.Series("", index=raw.index, dtype=str)
    for mask, label in [(invalid, "invalid/missing date"), (nonnumeric, "non-numeric value"),
                        (infinite, "infinite value"), (huge, "extreme numeric magnitude >=1e100"),
                        (duplicate, "duplicate date"), (safe_empty, "removed empty observation"),
                        (exact, "removed exact duplicate"), (recognized_missing, "missing value"),
                        (missing_removed, "removed missing value from training input")]:
        reasons.loc[mask] += label + "; "
    if len(raw.columns) > 2:
        reasons += "extra columns preserved; "
    review = [{"series_id": series.series_id, "raw_record": int(i + start + 2), "reason": reasons[i],
               "raw_record_json": encoded(raw.loc[i].to_dict())} for i in raw.index if reasons[i]]
    tail_invalid = 0
    for is_invalid in invalid.iloc[::-1]:
        if not is_invalid:
            break
        tail_invalid += 1
    info["possible_footer_rows"] = tail_invalid
    for key in ("invalid_date_count", "missing_date_count", "nonnumeric_value_count", "infinite_value_count",
                "extreme_numeric_count", "duplicate_dates", "safe_empty_rows_removed", "exact_duplicate_rows_removed",
                "missing_value_rows_removed"):
        if info[key]:
            warnings.append(f"{key}={info[key]}")
    if len(conflict_dates):
        warnings.append("Conflicting duplicate dates retained for manual review")
    if not info["originally_sorted"]:
        warnings.append("Observations sorted chronologically")
    missing = clean.value.isna().to_numpy()
    positions = np.flatnonzero(~missing)
    # All-missing series use leading=N, trailing=internal=0, avoiding double counting.
    leading = int(positions[0]) if len(positions) else len(clean)
    trailing = int(len(clean) - 1 - positions[-1]) if len(positions) else 0
    info.update(clean_missing_count=int(missing.sum()), missing_values=int(missing.sum()),
                total_rows=len(clean), valid_values=int((clean.value.notna() & np.isfinite(clean.value)).sum()),
                valid_observations=int((clean.date.notna() & clean.value.notna() & np.isfinite(clean.value)).sum()),
                missing_pct=100 * float(missing.mean()) if len(clean) else None,
                leading_missing_count=leading, trailing_missing_count=trailing,
                internal_missing_count=int(missing.sum()) - leading - trailing,
                first_date=clean.date.min(), last_date=clean.date.max(), inferred_frequency=infer_frequency(clean.date))
    sorted_dates = clean.date.dropna().drop_duplicates().sort_values()
    gaps = sorted_dates.diff().dt.total_seconds() / 86400
    low, high = GAP_BANDS[series.expected_frequency]
    suspicious = gaps.notna() & ~gaps.between(low, high)
    info.update(largest_gap_days=gaps.max(), median_gap_days=gaps.median() if gaps.notna().any() else None,
                suspicious_gap_count=int(suspicious.sum()), number_of_suspicious_gaps=int(suspicious.sum()),
                suspicious_gaps=encoded([{"from": sorted_dates.shift()[i], "to": sorted_dates[i], "days": gaps[i]}
                                        for i in gaps.index[suspicious]]))
    if info["clean_missing_count"]:
        warnings.append(f"Missing values={info['clean_missing_count']} (internal={info['internal_missing_count']})")
    if info["inferred_frequency"] != series.expected_frequency:
        warnings.append(f"Frequency expected={series.expected_frequency}, inferred={info['inferred_frequency']}")
    if info["suspicious_gap_count"]:
        warnings.append(f"Suspicious gaps={info['suspicious_gap_count']}")
    return clean, review


AUDIT_FIELDS = "series_id name category raw_file clean_file file_exists raw_rows clean_rows detected_date_column detected_value_column date_parse_success_rate numeric_parse_success_rate expected_frequency inferred_frequency first_date last_date valid_observations raw_missing_count clean_missing_count missing_pct leading_missing_count trailing_missing_count internal_missing_count duplicate_dates conflicting_duplicate_dates largest_gap_days median_gap_days suspicious_gap_count infinite_value_count status warning error".split()


def save_csv(frame, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".csv.tmp")
    frame.to_csv(temporary, index=False, date_format="%Y-%m-%d", lineterminator="\n")
    temporary.replace(path)


def run(root=ROOT, registry=REGISTRY):
    root = Path(root).resolve()
    files, discovered = inventory(root, registry)
    save_csv(discovered, root / "data/audit/raw_file_inventory.csv")
    extras = discovered.loc[discovered.kind.eq("unexpected"), "path"].tolist()
    for path in extras:
        print(f"Unexpected CSV (preserved, not treated as a series): {path}")
    records, review_rows = [], []
    for index, series in enumerate(registry, 1):
        info = {key: None for key in AUDIT_FIELDS}
        info.update(asdict(series), status="FAILED", warning="", error="", file_exists=False, clean_file="")
        warnings = []
        matches = [p for p in files if p.stem.casefold() == series.series_id.casefold()]
        info["file_exists"] = bool(matches)
        info["raw_candidates"] = encoded([str(p.relative_to(root)) for p in matches])
        try:
            if not matches:
                raise FileNotFoundError(f"Missing expected file: {series.raw_file}")
            if len({hashlib.sha256(p.read_bytes()).hexdigest() for p in matches}) != 1:
                raise ValueError("Raw copies differ; choose the authoritative source manually: " + info["raw_candidates"])
            canonical = root / series.raw_file
            path = canonical if canonical in matches else matches[0]
            info["raw_file"] = str(path.relative_to(root))
            info["identical_raw_copies"] = len(matches)
            raw, start = inspect_csv(path, series.series_id, info, warnings)
            clean, review = clean_series(raw, series, info, warnings, start)
            review_rows.extend(review)
            if not info["valid_observations"]:
                raise ValueError("No usable observations with a valid date and finite numeric value")
            target = root / f"data/cleaned/{series.series_id}.csv"
            save_csv(clean, target)
            info["clean_file"] = str(target.relative_to(root))
            info["status"] = "WARNING" if warnings else "OK"
        except (OSError, ValueError, TypeError, UnicodeError, csv.Error) as exc:
            info["error"] = f"{type(exc).__name__}: {exc}"
            # Preserve earlier outputs but never advertise them as current successes.
            if (root / f"data/cleaned/{series.series_id}.csv").exists():
                warnings.append("An older clean CSV exists; stale, do not use it for this run")
        info["warning"] = "; ".join(warnings)
        records.append(info)
        print(f"[{index:02}/{len(registry)}] {series.series_id:<12} {info['status']:<7} rows={info['clean_rows']} frequency={info['inferred_frequency']} missing={info['clean_missing_count']} | {info['raw_file']}")
        if warnings or info["error"]:
            print("    " + (info["error"] or info["warning"]))
    audit = pd.DataFrame(records)
    save_csv(audit, root / "data/audit/data_cleaning_audit.csv")
    save_csv(pd.DataFrame(review_rows, columns=["series_id", "raw_record", "reason", "raw_record_json"]),
             root / "data/audit/observations_for_review.csv")
    summaries = []
    for category in ["ALL", *dict.fromkeys(s.category for s in registry)]:
        subset = audit if category == "ALL" else audit.loc[audit.category.eq(category)]
        summaries.append({"category": category, "total_expected_series": len(subset),
                          "files_found": int(subset.file_exists.sum()), "files_missing": int((~subset.file_exists).sum()),
                          "loaded_successfully": int(subset.status.ne("FAILED").sum()),
                          "warning_count": int(subset.status.eq("WARNING").sum()),
                          "failed_count": int(subset.status.eq("FAILED").sum()),
                          "missing_value_rows_removed": int(subset.get("missing_value_rows_removed", pd.Series(dtype=float)).sum()),
                          "unexpected_csv_count": len(extras) if category == "ALL" else None})
    save_csv(pd.DataFrame(summaries), root / "data/audit/data_quality_summary.csv")
    metadata_fields = "series_id name category expected_frequency inferred_frequency source first_date last_date valid_observations missing_pct clean_file".split()
    save_csv(audit.loc[audit.status.ne("FAILED"), metadata_fields], root / "data/cleaned/series_metadata.csv")
    summary = summaries[0]
    print("\nCHronoZ DATA CLEANING COMPLETE")
    print(f"Expected: {len(registry)} | Found: {summary['files_found']} | Cleaned: {summary['loaded_successfully']} | Warnings: {summary['warning_count']} | Failed: {summary['failed_count']} | Missing rows removed: {summary['missing_value_rows_removed']}")
    for relative in ["data/cleaned", "data/cleaned/series_metadata.csv", "data/audit/data_cleaning_audit.csv",
                     "data/audit/data_quality_summary.csv", "data/audit/raw_file_inventory.csv", "data/audit/observations_for_review.csv"]:
        print(root / relative)
    return audit


if __name__ == "__main__":
    result = run()
    sys.exit(1 if result.status.eq("FAILED").any() else 0)
