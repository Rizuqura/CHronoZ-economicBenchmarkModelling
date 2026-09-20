# Current delta approach: suitability notes

Recorded: **2026-09-19**  
Last updated: **2026-09-20**  
Related study: [Delta transformation analysis](analysis.ipynb)

## Current decision

Use the current delta/change approach for **30 variables: ranks 1-31 except
AWHAETP (rank 28)**. Their working label is **GOOD**. Ranks 20-31 excluding
AWHAETP were approved on **2026-09-20** based on the user's audit.

**Six variables remain outside GOOD:** AWHAETP (28), ICSA (32), WALCL (33),
WRESBAL (34), TOTRESNS (35), and UNRATE (36). AWHAETP and ICSA retain the user's
**(SKIP)** markers; the remaining four are pending further algorithm research.

PPIACO retains its regime-sensitivity cautions. PCEC96 uses outlier-robust
calibration, preserving and scoring historical events while excluding flagged
observations from calibration only. This status update does not change notebook
calculations or cleaned data.

Here, **current model** means the exploratory delta transformation approach.
These labels record the user's research selection, not a trained model,
production benchmark, or proof of stationarity. They do not override the
notebook's separate automated distribution flags or economic suitability registry.

## GOOD: usable for the current approach

Ranks 20-31, except AWHAETP (28), are approved based on the user's audit.
Original research cautions and the IPMAN `(seperate)` and M2SL `(Acceleration)`
annotations are preserved. The acceleration annotation records a research note;
it does not by itself change the listed transformation or implement a model.

| Rank | Series | Variable | Preferred change | Original rating / current status | Research rationale |
| ---: | --- | --- | --- | --- | --- |
| 1 | `HOUST` | Housing Starts | Δlog(x) | 🟢 Excellent | Setelah log-delta bentuknya sangat rapi; skew ≈ -0.19, excess kurtosis ≈ 0.73. Scale-independent dan intuitif sebagai monthly housing momentum. |
| 2 | `PERMIT` | Building Permits | Δlog(x) | 🟢 Excellent | Positive quantity, cyclical, Δ relatif stabil; skew ≈ -0.20. Sangat cocok sebagai distribution of activity shocks. |
| 3 | `JTSJOL` | Job Openings | Δlog(x) | 🟢 Excellent | Level trending kuat, tetapi growth/change jauh lebih stationary-looking; skew ≈ -0.21, kurtosis ≈ 1.53. |
| 4 | `OPHNFB` | Labor Productivity | Δlog(x) | 🟢 Excellent | Quarterly growth conceptually natural; log-delta menghilangkan secular level trend dengan baik. |
| 5 | `PPIFID` | PPI Final Demand | Δlog(x) | 🟢 Excellent | Price index → relative change adalah unit ekonomis yang benar; distribusi cukup bersih. |
| 6 | `DRSDCILM` | SLOOS Loan Demand | Δ level | 🟢 Excellent | Signed diffusion index, jadi log mustahil. Δ menghasilkan skew ≈ -0.06 dan kurtosis ≈ -0.18 — sangat bagus. |
| 7 | `DRTSCILM` | SLOOS Tightening | Δ level | 🟢 Very good | Signed/bounded survey series. Arithmetic change secara ekonomi paling masuk akal. |
| 8 | `IMPGSC1` | Real Imports | Δlog(x) | 🟢 Very good | Level nominal-scale problem hilang; log-delta jauh lebih simetris daripada arithmetic delta. |
| 9 | `EXPGSC1` | Real Exports | Δlog(x) | 🟢 Very good | Sama: quantity level → proportional quarterly growth. Log-transform memperbaiki tail secara drastis. |
| 10 | `PCEPILFE` | Core PCE Price Index | Δlog(x) | 🟢 Very good | Inflation secara fundamental adalah perubahan log price level. Distribusi cukup bagus meski persistent. |
| 11 | `PCEPI` | PCE Price Index | Δlog(x) | 🟢 Very good | Sama; tail lebih bersih dibanding raw difference. |
| 12 | `CPIAUCSL` | CPI All Items | Δlog(x) | 🟢 Very good | Native level jelas tidak cocok. Log inflation jauh lebih meaningful. Masih ada persistence/regime inflation. |
| 13 | `CPILFESL` | Core CPI | Δlog(x) | 🟢 Very good | Secara definisi cocok; persistence tinggi berarti nantinya mungkin perlu regime-conditioned distribution. |
| 14 | `DRBLACBS` | Business Loan Delinquency | Δ level / pp | 🟢 Good | Ini rate, sehingga perubahan percentage point, bukan % change. Cukup smooth tapi hanya quarterly. |
| 15 | `TCU` | Capacity Utilization | Δ level / pp | 🟢 Good | Bounded rate; arithmetic Δ memiliki interpretasi langsung: +1 pp capacity utilization. |
| 16 | `CIVPART` | Labor Force Participation | Δ level / pp | 🟢 Good | Rate bounded. Δ benar secara unit, tetapi banyak perubahan sangat kecil/zero karena rounding. |
| 17 | `FEDFUNDS` | Fed Funds Rate | Δ level / bp | 🟢 Good | Perubahan rate harus bp/percentage points. Sangat interpretable, tapi kebijakan bersifat discrete dan regime dependent. |
| 18 | `PPIACO` | PPI All Commodities | `100 * ln(PPIACO_t / PPIACO_(t-1))` | Good-ish originally; now **GOOD** | Use monthly proportional movement to measure historical unusualness, with z-score and empirical percentile. Retain tails and the regime-sensitivity caution from the dedicated audit. |
| 19 | `PCEC96` | Real Personal Consumption Expenditures | `100 * ln(PCEC96_t / PCEC96_(t-1))` | Good-ish originally; now **GOOD** | Measure unusual monthly real-consumption growth against an outlier-robust historical reference. Flag by median/MAD modified z; exclude flagged events from calibration only and score all observations. |
| 20 | `W875RX1` | Real Income ex Transfers | Δlog(x) | 🟡 Good-ish originally; now **GOOD** | User-audited: usable as a benchmark (2026-09-20). Original note: Conceptually tepat dan banyak observasi; shock fiscal/COVID menghasilkan tails. |
| 21 | `RRSFS` | Real Retail Sales | Δlog(x) | 🟡 Good-ish originally; now **GOOD** | User-audited: usable as a benchmark (2026-09-20). Original note: Cocok untuk % change tetapi crisis jumps membuat distribusi berat. |
| 22 | `CES0500000003` | Hourly Earnings | Δlog(x) | 🟡 Conditional originally; now **GOOD** | User-audited: usable as a benchmark (2026-09-20). Original note: Wage level trending → log change. Tetapi observasi pendek dan pandemic composition effects sangat besar. |
| 23 | `INDPRO` | Industrial Production | Δlog(x) | 🟡 Conditional originally; now **GOOD** | User-audited: usable as a benchmark (2026-09-20). Original note: Secara teori ideal, tapi shutdown/reopening menciptakan extreme observations. |
| 24 | `IPMAN` | Manufacturing Production | Δlog(x) | 🟡 Conditional originally; now **GOOD** | User-audited: usable as a benchmark (2026-09-20). Original note: Sama seperti INDPRO; tails crisis sangat besar. (seperate) |
| 25 | `TOTALSL` | Consumer Credit | Δlog(x) | 🟡 Conditional originally; now **GOOD** | User-audited: usable as a benchmark (2026-09-20). Original note: Stock variable dengan secular growth. Log-delta benar tetapi perubahan struktural membuat distribusi non-stationary. |
| 26 | `BUSLOANS` | C&I Loans | Δlog(x) | 🟡 Conditional originally; now **GOOD** | User-audited: usable as a benchmark (2026-09-20). Original note: Log-delta jauh lebih baik daripada dollar delta, tapi credit creation mengalami regime/policy shocks. |
| 27 | `M2SL` | M2 Money Stock | Δlog(x) | 🟡 Conditional originally; now **GOOD** | User-audited: usable as a benchmark (2026-09-20). Original note: Konsepnya benar; 2020 membuat distribution sangat fat-tailed dan regime sensitive. (Acceleration) |
| 29 | `AWHMAN` | Manufacturing Hours | Δ level | 🟡 Weak originally; now **GOOD** | User-audited: usable as a benchmark (2026-09-20). Original note: ~25% zero changes dan kurtosis Δ sangat tinggi. Distribution continuous biasa kurang natural. |
| 30 | `RPI` | Real Personal Income | Δlog(x) | 🟠 Weak originally; now **GOOD** | User-audited: usable as a benchmark (2026-09-20). Original note: Fiscal transfers membuat gigantic jumps; unconditional delta distribution mudah menyesatkan. |
| 31 | `PAYEMS` | Payroll Employment | Δlog(x) atau Δ jobs | 🟠 Weak originally; now **GOOD** | User-audited: usable as a benchmark (2026-09-20). Original note: Normally bagus, tetapi COVID membuat skew sekitar -14 pada log-delta. Lebih cocok robust/regime model. |

## RESEARCH_PENDING: find a suitable algorithm or treatment

Six variables remain outside GOOD. **AWHAETP (28) and ICSA (32) are explicitly
marked SKIP** and must not be promoted by the ranks 20-31 approval. The other
four entries still require algorithm research. All source observations remain.

| Rank | Series | Variable | Preferred change | Original rating / current status | Research rationale |
| ---: | --- | --- | --- | --- | --- |
| 28 | `AWHAETP` | Weekly Hours Total Private | Δ level | 🟡 Weak; **SKIP** | Δ secara unit benar, tetapi ~48% perubahan persis nol karena seri bergerak dalam increments kecil/rounding. (SKIP) |
| 32 | `ICSA` | Initial Claims | Δlog(x) | 🟠 Weak; **SKIP** | High-frequency bagus, tetapi crisis spikes ekstrem; log membantu tetapi tail tetap brutal. (SKIP) |
| 33 | `WALCL` | Fed Total Assets | Δlog(x) | 🟠 Weak | Balance sheet adalah policy stock: QE/QT menciptakan structural breaks, bukan random fluctuations dari satu distribution. |
| 34 | `WRESBAL` | Reserve Balances | Δlog(x) / signed % | 🟠 Weak | Kebijakan dan plumbing liquidity mendominasi; distribution berubah antar monetary regimes. |
| 35 | `TOTRESNS` | Total Reserves | Δlog(x) | 🔴 Poor unconditional | Reserve regime sebelum/after 2008 praktis dunia berbeda. Satu historical distribution akan mencampur dua DGP. |
| 36 | `UNRATE` | Unemployment Rate | Δ level / pp | 🔴 Poor unconditional | Secara unit Δ benar, tetapi 24.5% perubahan = 0 dan COVID menghasilkan skew Δ ≈ +16.7, kurtosis >400. Single delta distribution jelas tidak cukup. |

## PPIACO: selected transformation and intended interpretation

**Working label: GOOD** for the current historical Delta Distribution approach.  
**Dedicated audit:** [PPIACO Delta Distribution Audit](audit-PPIACO.ipynb).  
**Computed audit verdict: REGIME-SENSITIVE** under the notebook's explicitly
stated exploratory rubric. GOOD is the research-use decision, not an assertion
that one unconditional distribution is stable through time.

- **Transformation:** `delta_log_pct = 100 * ln(PPIACO_t / PPIACO_(t-1))`,
  over consecutive months. Approximately monthly percent change for small moves;
  not annualized and not exact percent for large moves.
- **Representation:** historical distribution of monthly log changes, rather
  than the historical raw price-index level.
- **Normalization:** `z_delta = (delta_log_pct - historical_mean) / historical_std`,
  using sample standard deviation; empirical percentile is
  `100 * count(historical_delta <= current_delta) / N`, with equal values tied.
- **Desired interpretation:** how unusual the current monthly movement in
  PPIACO is compared with its own historical monthly movement distribution.
  Positive/negative z is above/below the historical mean movement, not
  necessarily positive/negative price growth.
- **Markings:** absolute z below 0.5 is CENTRAL; 0.5-1 NORMAL; 1-2 ELEVATED;
  2-3 EXTREME; 3 or above SPIKE. Noncentral labels retain direction. These
  categories do not assert Gaussian probabilities. Empirical P25-P75,
  P10-P90, and P5-P95 provide separate historical ranges.
- **Tail treatment:** retain all tail observations; no deletion, winsorization,
  or z-score clipping. Only the first observation is lost to differencing.
- **Audit evidence:** the current 1,363-delta snapshot has excess kurtosis about
  **12.33** and **16.29%** zero changes. The delta ADF test rejects a unit root
  (p about **9.78e-17**); KPSS does not reject constant-mean stationarity
  (reported p **0.10**, actual p above that lookup-table bound). These tests do
  not establish stable variance: the 60-month rolling-standard-deviation
  P90/P10 ratio is about **5.53**, and the rolling-mean range spans about
  **1.81** full-sample standard deviations.
- **Reference limitation:** normalization uses the full historical snapshot,
  including the current observation. Historical states are retrospective, not
  a look-ahead-free trading signal or validated production benchmark.
- **Interpretation boundary:** extreme movement alone does not establish
  inflation, a supply shock, or stagflation. Cross-check PPIFID, CPI, Core CPI,
  PCE inflation, Industrial Production, Manufacturing Production, Capacity
  Utilization, user-provided commodity/oil/energy information, and external
  supporting evidence before assigning an economic cause.

## PCEC96: selected transformation and intended interpretation

**Working label: GOOD** with outlier-robust calibration.  
**Dedicated audit:** [PCEC96 Delta Distribution Audit](audit-PCEC96.ipynb).  
**Computed audit verdict: PASS WITH OUTLIER-ROBUST CALIBRATION** under the
notebook's stated exploratory rubric. This is a research-use decision, not
validation of a production benchmark.

- **Transformation:** `delta_log_pct = 100 * ln(PCEC96_t / PCEC96_(t-1))`,
  over consecutive months. Approximately monthly percent change for small moves;
  not annualized.
- **Representation:** distinguish the full historical delta distribution from
  the ordinary-movement calibration distribution. Every historical event remains
  in the full record.
- **Calibration rule:** fit the median and unscaled MAD on calibration-eligible
  history; `modified_z = 0.6745 * (delta_log_pct - median_delta) / MAD`.
  Flag `abs(modified_z) > 3.5`. IQR fences are supporting diagnostics only;
  no dates, including COVID months, are manually excluded.
- **Normalization:** `benchmark_z = (delta_log_pct - benchmark_mean) / benchmark_std`,
  using mean and sample standard deviation from retained calibration observations
  only. Empirical percentile is `100 * count(benchmark_delta <= delta_log_pct) / N`.
  Every observation, including excluded events, receives both scores.
- **Desired interpretation:** how unusual current monthly real-consumption
  growth is relative to ordinary historical monthly consumption behavior.
  Positive/negative z means above/below benchmark mean growth, not necessarily
  an increase/decrease in consumption itself.
- **Markings:** absolute z below 0.5 is CENTRAL; 0.5-1 NORMAL; 1-2 ELEVATED;
  2-3 EXTREME. At or above 3, use OUTLIER only when the robust rule also flags
  the observation; otherwise retain EXTREME. Noncentral states retain direction.
  Empirical P25-P75, P10-P90, and P5-P95 ranges use calibration observations only.
- **Tail treatment:** retain, flag, exclude from calibration, and still score.
  No deletion from history, winsorization, or z-score clipping. Statistical
  exclusion does not mean bad data or prove a particular economic cause.
- **Audit evidence:** all **234** valid monthly changes are retained. Of **233**
  calibration-eligible months, **12 (5.15%)** are excluded, leaving **221** for
  calibration. Standard deviation falls from **1.1672** to **0.2717** (about
  **76.7%**); excess kurtosis falls from **59.60** to **0.43**. These comparisons
  use unfiltered eligible history versus retained calibration observations.
  The rule identifies **6 of 12** months in 2020 without date-based exclusions.
- **Robustness:** thresholds **3.0, 3.5, and 4.0** pass the notebook's sensitivity
  screen. Filtered 60-calendar-month rolling std P90/P10 is about **1.46**;
  the rolling-mean range is about **0.72** benchmark standard deviations.
  Filtering retains calendar positions rather than compressing time.
- **Reference timing:** the current audit calibrates through **2026-06-01** and
  reserves **2026-07-01** as the latest reporting holdout. That latest observation
  cannot influence its own fitted reference. The notebook defaults to the
  penultimate month of the loaded snapshot; pin its cutoff explicitly to keep
  the same reference after new data arrives. Earlier historical scores remain
  retrospective, not a real-time backtest.
- **Interpretation boundary:** ordinary-movement calibration is conditional on
  the chosen statistical rule. The improved distribution does not establish
  Gaussianity, causal explanations, or future stability. Review new disruptions
  and changes in consumption behavior before operational use.

## Interpretation and implementation notes

- **Source of judgments:** the user's supplied ranked table. Reasons are preserved
  in their original language. Approximate statistics, causal explanations, and
  claims about stationarity or comparative improvement are user-supplied research
  notes; they were not independently revalidated for this document, except for
  the PPIACO and PCEC96 diagnostics reported in their dedicated audits.
- **Log changes:** the notebook implements `100 * (log(X_t) - log(X_(t-1)))`.
  This is approximately percent change for small moves, not an exact percentage.
- **Rate changes:** `X_t - X_(t-1)` is a percentage-point change when levels are
  stored in percent. For FEDFUNDS, multiply that difference by 100 to express it
  in basis points; the existing notebook displays percentage points.
- **Native steps and gaps:** retain weekly, monthly, and quarterly frequencies.
  Never calculate a one-step change across a missing calendar period.
- **Survey balances:** retain the meaningful native levels of DRTSCILM and
  DRSDCILM alongside their momentum measures.
- **Unimplemented alternatives:** PAYEMS absolute jobs change and WRESBAL
  signed-percent terminology remain proposals requiring an explicit definition
  and evaluation. This note does not add them to the notebook registry.
- **Next research:** investigate the pending variables' rounding/zero changes,
  crisis tails, and regime dependence before selecting a fitting algorithm.
  Do not infer that removing observations is the solution.

The dedicated audits add descriptive normalization and range markings; PCEC96
also separates outlier-robust calibration from full-history scoring.
The original analysis.ipynb, cleaned CSVs, and model training remain unchanged.
