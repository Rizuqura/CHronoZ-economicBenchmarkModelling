# CHronoZ local macroeconomic cleaning

Run `python dataCleansing.py` with `requirements.txt` installed. All active registry,
discovery, inspection, validation, cleaning, and reporting logic lives in
**dataCleansing.py**. Paths resolve relative to the script. No network access is used.

The script scans `data/raw/` recursively and the original CSVs directly under
`data/`. Identical copies are recorded; differing copies fail for manual source
selection. Raw files are never rewritten or moved. Unexpected CSVs are reported
in the console and inventory rather than treated as economic series.

Outputs regenerated on each run:

- `data/cleaned/{SERIES_ID}.csv`: exactly `date,value`, for each successful series.
- `data/cleaned/series_metadata.csv`: metadata and paths for current successes.
- `data/audit/data_cleaning_audit.csv`: detailed audit per expected series.
- `data/audit/data_quality_summary.csv`: overall and per-category counts.
- `data/audit/raw_file_inventory.csv`: paths, hashes, headers, and extra files.
- `data/audit/observations_for_review.csv`: suspicious/removed records and reasons.

Earlier `src/chronoz_quant/` modules and long/wide outputs are preserved as legacy
work. The current entry point does not import or regenerate them.

## Cleaning and manual review

Only full raw-record duplicates and invalid-date rows whose other fields are all
recognized missing markers are removed during structural cleanup. Rows whose
numeric value is NaN are then dropped from the cleaned training inputs, including
unparseable numeric tokens. All other observations retain their original dates
and values. Every removal is counted and recorded; raw files remain unchanged.
Conflicting duplicate dates remain with warnings. Invalid dates with useful
observations remain as blank dates; rows with unparseable values are removed. Original
records remain in the review CSV. Extra columns are reported and preserved in
raw files and review records.

Recognizable metadata preambles are recorded before being skipped. Inconsistent
record widths fail rather than guessing about footers. Same-width footer
candidates are recorded and handled by the conservative cleaning rules.
Ambiguous schema detection fails unless an explicit series/value header resolves
value selection; multiple plausible numeric columns still warn. Intraday or
timezone-bearing dates fail to avoid silent truncation or conversion.

No filling, interpolation, resampling, normalization, or economic transformations
are performed. Infinite values and finite magnitudes at or above `1e100` are
flagged and retained; this is only a technical review heuristic. Zero-row series
or series without any dated finite observations fail.

Failed series have explicit errors. Older cleaned CSVs are preserved but flagged
as stale and excluded from current metadata. Use the audit/metadata to identify
current usable outputs. Exit code is 1 if any series fails.

## Audit definitions

Raw row counts exclude the detected header and metadata preamble. Raw dtypes
reflect the deliberate string-preserving read; parsing success is separate.
Date parse success is a fraction of all table rows; numeric success excludes
recognized missing markers. `raw_missing_count` records original missing markers;
`missing_value_rows_removed` counts NaN rows removed after structural cleanup.
Clean missing counts and percentages describe the saved output (zero after this
filter). Date-gap diagnostics run after removal, so dropped internal observations
remain visible as gaps. No dates are shifted or filled. Removing NaNs alone does
not resolve other warnings, such as invalid dates or conflicting duplicates.
Leading/trailing/internal counts partition clean NaNs in sorted order; an
all-missing series counts every row as leading missing. Valid observations
require a date and a finite numeric value. Date coverage includes dated rows
with missing values.

Duplicate dates count distinct repeated valid dates before cleaning. Conflicts
compare parsed values, including missing versus numeric. Nonidentical raw rows
remain even when parsing makes values equal.

Frequency inference requires two unique-date gaps and 80% of gaps in the daily
(1), weekly (7), monthly (28-31), quarterly (89-92), or annual (365-366 days) band.
Otherwise the result is irregular or unknown. Suspicious gaps are individual
unique-date gaps outside the expected band, including short gaps. Endpoints are
stored in the audit. These diagnostics do not certify calendar completeness.

## Notebook use

From the project root:

```python
import pandas as pd
indpro = pd.read_csv("data/cleaned/INDPRO.csv", parse_dates=["date"])
indpro.plot(x="date", y="value")
```

If the working directory is `notebooks/`, use `../data/cleaned/INDPRO.csv`.
Cleaning stays in the script, outside the notebook.

Run checks with `python -m unittest discover -s tests -v`.

## Monthly correlation notebook

Open `notebook/matrix-corrAnalysis.ipynb` and run all cells using the dependencies
in `requirements-notebook.txt`. The executed notebook includes native monthly
availability, raw-level diagnostic correlations, explicitly registered one-month
changes, Pearson/Spearman heatmaps, pairwise counts, and top positive/negative
pairs. Weekly and quarterly exclusions are listed. Every correlation requires
at least 60 shared observations; histories are paired independently.

Changes require consecutive calendar months, so removed observations cannot
turn a two-month move into a one-month move. Inputs stay unchanged. CSV matrices,
PNG heatmaps, tables, and source fingerprints are written to `outputs/correlation/`.
The results describe co-movement, not causality or predictive performance.

To execute without opening an editor:

```text
python -m jupyter nbconvert --execute --to notebook --inplace notebook/matrix-corrAnalysis.ipynb
```

## Follow-up correlation notebooks

Each notebook imports the cleaned data independently, uses the same explicit
monthly-change transformations, displays full dataset titles, and preserves
missing calendar months. Parameters are editable in its setup cell.

| Notebook | Analysis | Default parameters | Exports |
| --- | --- | --- | --- |
| `notebook/redundancy-map.ipynb` | Candidate overlap graph, screened matrix, and connection counts | At least 60 pairs; absolute Pearson >= 0.80 and Spearman >= 0.60, matching signs | `outputs/redundancy/` |
| `notebook/lead-lag-correlation.ipynb` | Calendar-aligned Pearson/Spearman lag scan and profiles | -12 to +12 months; at least 60 observations per pair/lag | `outputs/lead_lag/` |
| `notebook/rolling-correlation.ipynb` | Trailing Pearson paths, pair stability tables, and latest-window matrix | 60 calendar months; at least 48 paired observations; full elapsed window required | `outputs/rolling_correlation/` |

In lead-lag analysis, lag `k` means correlation of `X_t` with `Y_(t+k)`:
positive lag means the first variable precedes the second. This is observation
timing, not publication timing or forecast performance. Peak lag selection
searches multiple comparisons and is descriptive. Redundancy candidates do not
automatically remove variables, and rolling paths do not define regimes.

Use Restart Kernel and Run All, or substitute the notebook filename in the
execution command above. Each output directory contains source fingerprints,
parameters, CSV results, PNG charts, and a computed summary.
