# Data learning: individual distributions

One independent notebook per cleaned variable. Each loads its own CSV and shows a histogram, horizontal box plot, coverage, descriptive statistics, and existing audit warnings.

Includes monthly, weekly, and quarterly observations at native frequency. No economic transformations, imputation, trimming, or model fitting. Units are labeled as native file units because the project metadata does not specify units.

Open a notebook and use Restart Kernel and Run All with `requirements-notebook.txt`. PNG, summary CSV, histogram counts, and provenance exports go to `outputs/distributions/<SERIES_ID>/`.

Notebooks are organized by economic category. Open a category below to find its variables.

## Growth / Activity (8)

| Variable | Dataset | Frequency |
| --- | --- | --- |
| [INDPRO](growth_activity/INDPRO.ipynb) | Industrial Production | monthly |
| [IPMAN](growth_activity/IPMAN.ipynb) | Manufacturing Production | monthly |
| [PCEC96](growth_activity/PCEC96.ipynb) | Real Personal Consumption Expenditure | monthly |
| [W875RX1](growth_activity/W875RX1.ipynb) | Real Personal Income excluding transfers | monthly |
| [RPI](growth_activity/RPI.ipynb) | Real Personal Income | monthly |
| [RRSFS](growth_activity/RRSFS.ipynb) | Real Retail & Food Services Sales | monthly |
| [HOUST](growth_activity/HOUST.ipynb) | Housing Starts | monthly |
| [PERMIT](growth_activity/PERMIT.ipynb) | Building Permits | monthly |

## Labor (8)

| Variable | Dataset | Frequency |
| --- | --- | --- |
| [PAYEMS](labor/PAYEMS.ipynb) | Nonfarm Payroll Employment | monthly |
| [UNRATE](labor/UNRATE.ipynb) | Unemployment Rate | monthly |
| [ICSA](labor/ICSA.ipynb) | Initial Claims | weekly |
| [AWHAETP](labor/AWHAETP.ipynb) | Average Weekly Hours — Total Private | monthly |
| [AWHMAN](labor/AWHMAN.ipynb) | Average Weekly Hours — Manufacturing | monthly |
| [JTSJOL](labor/JTSJOL.ipynb) | Job Openings | monthly |
| [CIVPART](labor/CIVPART.ipynb) | Labor Force Participation Rate | monthly |
| [CES0500000003](labor/CES0500000003.ipynb) | Average Hourly Earnings — Total Private | monthly |

## Inflation (6)

| Variable | Dataset | Frequency |
| --- | --- | --- |
| [CPIAUCSL](inflation/CPIAUCSL.ipynb) | CPI All Items | monthly |
| [CPILFESL](inflation/CPILFESL.ipynb) | Core CPI | monthly |
| [PCEPI](inflation/PCEPI.ipynb) | PCE Price Index | monthly |
| [PCEPILFE](inflation/PCEPILFE.ipynb) | Core PCE Price Index | monthly |
| [PPIFID](inflation/PPIFID.ipynb) | Producer Prices — Final Demand | monthly |
| [PPIACO](inflation/PPIACO.ipynb) | Producer Prices — All Commodities | monthly |

## Credit (5)

| Variable | Dataset | Frequency |
| --- | --- | --- |
| [BUSLOANS](credit/BUSLOANS.ipynb) | Commercial & Industrial Loans | monthly |
| [TOTALSL](credit/TOTALSL.ipynb) | Consumer Credit | monthly |
| [DRTSCILM](credit/DRTSCILM.ipynb) | SLOOS: Banks Tightening C&I Lending Standards | quarterly |
| [DRSDCILM](credit/DRSDCILM.ipynb) | SLOOS: Stronger Demand for C&I Loans | quarterly |
| [DRBLACBS](credit/DRBLACBS.ipynb) | Delinquency Rate on Business Loans | quarterly |

## Policy / Liquidity (5)

| Variable | Dataset | Frequency |
| --- | --- | --- |
| [FEDFUNDS](policy_liquidity/FEDFUNDS.ipynb) | Federal Funds Rate | monthly |
| [TOTRESNS](policy_liquidity/TOTRESNS.ipynb) | Total Bank Reserves | monthly |
| [WRESBAL](policy_liquidity/WRESBAL.ipynb) | Reserve Balances with Federal Reserve Banks | weekly |
| [WALCL](policy_liquidity/WALCL.ipynb) | Federal Reserve Total Assets | weekly |
| [M2SL](policy_liquidity/M2SL.ipynb) | M2 Money Supply | monthly |

## External / Structural (4)

| Variable | Dataset | Frequency |
| --- | --- | --- |
| [EXPGSC1](external_structural/EXPGSC1.ipynb) | Real Exports of Goods and Services | quarterly |
| [IMPGSC1](external_structural/IMPGSC1.ipynb) | Real Imports of Goods and Services | quarterly |
| [OPHNFB](external_structural/OPHNFB.ipynb) | Nonfarm Business Sector Labor Productivity | quarterly |
| [TCU](external_structural/TCU.ipynb) | Total Capacity Utilization | monthly |
