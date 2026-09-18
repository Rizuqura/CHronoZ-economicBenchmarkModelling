# CHronoZ Data Resources

Documentation generated: **2026-09-17** (local time, Asia/Jakarta, UTC+07:00).

This catalog describes the cleaned native-frequency series in `data/cleaned/`. 
Names, category order, and sources follow the active registry in `dataCleansing.py` 
and `data/cleaned/series_metadata.csv`. Validation and missing counts were checked 
against `data/audit/data_cleaning_audit.csv`.

Start and end dates are the earliest and latest dates with finite numeric observations. 
Observations count dated, finite numeric values; missing counts come from each 
individual cleaned series, before any cross-series alignment. Rows with missing values
are excluded from the cleaned training inputs; original missing counts and removal
records remain in the cleaning audit. Zero missing values does not imply an
uninterrupted calendar. Data age is the 
number of calendar days from the latest valid observation date to the generation 
date above. It is descriptive, not a release-lag or staleness assessment.

The series heading supplies **Nama data**. Source is **FRED**, the source recorded 
in project metadata; no underlying publisher is inferred. No training logs, 
model artifacts, or benchmark training/update metadata were found in the project. 
Every training field therefore reads **Not yet trained**.

**Available datasets:** 36. **Skipped registered datasets:** 0.

| Category | Datasets |
| --- | ---: |
| Growth / Activity | 8 |
| Labor | 8 |
| Inflation | 6 |
| Credit | 5 |
| Policy / Liquidity | 5 |
| External / Structural | 4 |

---

## Growth / Activity

## INDPRO — Industrial Production Index

**Representasi real world**  
Measures real output produced by U.S. manufacturing, mining, and utilities.

**Source**  
FRED

**Start date**  
1919-01-01

**End date**  
2026-07-01

**Observations**  
1291

**Missing count**  
0

**Data age**  
78 days

**Training model update date**  
Not yet trained

---

## IPMAN — Industrial Production: Manufacturing

**Representasi real world**  
Measures real output produced by U.S. manufacturing industries.

**Source**  
FRED

**Start date**  
1972-01-01

**End date**  
2026-07-01

**Observations**  
655

**Missing count**  
0

**Data age**  
78 days

**Training model update date**  
Not yet trained

---

## PCEC96 — Real Personal Consumption Expenditures

**Representasi real world**  
Measures inflation-adjusted spending by U.S. consumers on goods and services.

**Source**  
FRED

**Start date**  
2007-01-01

**End date**  
2026-07-01

**Observations**  
235

**Missing count**  
0

**Data age**  
78 days

**Training model update date**  
Not yet trained

---

## W875RX1 — Real Personal Income Excluding Current Transfer Receipts

**Representasi real world**  
Measures inflation-adjusted personal income excluding current transfer receipts, separating income earned through economic activity from transfers.

**Source**  
FRED

**Start date**  
1959-01-01

**End date**  
2026-07-01

**Observations**  
811

**Missing count**  
0

**Data age**  
78 days

**Training model update date**  
Not yet trained

---

## RPI — Real Personal Income

**Representasi real world**  
Measures the inflation-adjusted income received by individuals, including earnings, property income, and transfer receipts.

**Source**  
FRED

**Start date**  
1959-01-01

**End date**  
2026-07-01

**Observations**  
811

**Missing count**  
0

**Data age**  
78 days

**Training model update date**  
Not yet trained

---

## RRSFS — Advance Real Retail and Food Services Sales

**Representasi real world**  
Measures inflation-adjusted sales at U.S. retail stores and food-service establishments.

**Source**  
FRED

**Start date**  
1992-01-01

**End date**  
2026-08-01

**Observations**  
415

**Missing count**  
0

**Data age**  
47 days

**Training model update date**  
Not yet trained

**Data note**  
One missing-value row dated 2025-10-01 was removed from the cleaned training input. The original is preserved in raw data and the removal is recorded in the audit. The resulting gap from 2025-09-01 to 2025-11-01 is flagged; no observations were filled or shifted.

---

## HOUST — Housing Starts

**Representasi real world**  
Measures the number of new privately owned housing units on which construction has started in the United States.

**Source**  
FRED

**Start date**  
1959-01-01

**End date**  
2026-08-01

**Observations**  
812

**Missing count**  
0

**Data age**  
47 days

**Training model update date**  
Not yet trained

---

## PERMIT — Building Permits

**Representasi real world**  
Measures the number of new privately owned housing units authorized by building permits in the United States.

**Source**  
FRED

**Start date**  
1960-01-01

**End date**  
2026-08-01

**Observations**  
800

**Missing count**  
0

**Data age**  
47 days

**Training model update date**  
Not yet trained

---

## Labor

## PAYEMS — All Employees: Total Nonfarm Payrolls

**Representasi real world**  
Measures the number of payroll jobs at U.S. nonfarm establishments; it counts jobs rather than unique people.

**Source**  
FRED

**Start date**  
1939-01-01

**End date**  
2026-08-01

**Observations**  
1052

**Missing count**  
0

**Data age**  
47 days

**Training model update date**  
Not yet trained

---

## UNRATE — Unemployment Rate

**Representasi real world**  
Measures the percentage of the U.S. civilian labor force that is unemployed and actively seeking work.

**Source**  
FRED

**Start date**  
1948-01-01

**End date**  
2026-08-01

**Observations**  
943

**Missing count**  
0

**Data age**  
47 days

**Training model update date**  
Not yet trained

**Data note**  
One missing-value row dated 2025-10-01 was removed from the cleaned training input. The original is preserved in raw data and the removal is recorded in the audit. The resulting gap from 2025-09-01 to 2025-11-01 is flagged; no observations were filled or shifted.

---

## ICSA — Initial Claims

**Representasi real world**  
Counts initial applications for unemployment insurance benefits, providing a weekly measure of new claims.

**Source**  
FRED

**Start date**  
1967-01-07

**End date**  
2026-09-12

**Observations**  
3115

**Missing count**  
0

**Data age**  
5 days

**Training model update date**  
Not yet trained

---

## AWHAETP — Average Weekly Hours: Total Private

**Representasi real world**  
Measures average weekly hours worked by employees on U.S. private nonfarm payrolls.

**Source**  
FRED

**Start date**  
2006-03-01

**End date**  
2026-08-01

**Observations**  
246

**Missing count**  
0

**Data age**  
47 days

**Training model update date**  
Not yet trained

---

## AWHMAN — Average Weekly Hours: Manufacturing

**Representasi real world**  
Measures average weekly hours worked by production and nonsupervisory employees in U.S. manufacturing.

**Source**  
FRED

**Start date**  
1939-01-01

**End date**  
2026-08-01

**Observations**  
1052

**Missing count**  
0

**Data age**  
47 days

**Training model update date**  
Not yet trained

---

## JTSJOL — Job Openings: Total Nonfarm

**Representasi real world**  
Measures the number of unfilled job openings at U.S. nonfarm establishments.

**Source**  
FRED

**Start date**  
2000-12-01

**End date**  
2026-07-01

**Observations**  
308

**Missing count**  
0

**Data age**  
78 days

**Training model update date**  
Not yet trained

---

## CIVPART — Labor Force Participation Rate

**Representasi real world**  
Measures the share of the civilian noninstitutional population aged 16 and over that is working or actively seeking work.

**Source**  
FRED

**Start date**  
1948-01-01

**End date**  
2026-08-01

**Observations**  
943

**Missing count**  
0

**Data age**  
47 days

**Training model update date**  
Not yet trained

**Data note**  
One missing-value row dated 2025-10-01 was removed from the cleaned training input. The original is preserved in raw data and the removal is recorded in the audit. The resulting gap from 2025-09-01 to 2025-11-01 is flagged; no observations were filled or shifted.

---

## CES0500000003 — Average Hourly Earnings: Total Private

**Representasi real world**  
Measures average hourly earnings of employees on U.S. private nonfarm payrolls.

**Source**  
FRED

**Start date**  
2006-03-01

**End date**  
2026-08-01

**Observations**  
246

**Missing count**  
0

**Data age**  
47 days

**Training model update date**  
Not yet trained

---

## Inflation

## CPIAUCSL — Consumer Price Index: All Urban Consumers

**Representasi real world**  
Tracks prices paid by urban consumers for a broad basket of goods and services in the United States.

**Source**  
FRED

**Start date**  
1947-01-01

**End date**  
2026-08-01

**Observations**  
955

**Missing count**  
0

**Data age**  
47 days

**Training model update date**  
Not yet trained

**Data note**  
One missing-value row dated 2025-10-01 was removed from the cleaned training input. The original is preserved in raw data and the removal is recorded in the audit. The resulting gap from 2025-09-01 to 2025-11-01 is flagged; no observations were filled or shifted.

---

## CPILFESL — Core CPI

**Representasi real world**  
Tracks prices paid by urban consumers for goods and services excluding food and energy.

**Source**  
FRED

**Start date**  
1957-01-01

**End date**  
2026-08-01

**Observations**  
835

**Missing count**  
0

**Data age**  
47 days

**Training model update date**  
Not yet trained

**Data note**  
One missing-value row dated 2025-10-01 was removed from the cleaned training input. The original is preserved in raw data and the removal is recorded in the audit. The resulting gap from 2025-09-01 to 2025-11-01 is flagged; no observations were filled or shifted.

---

## PCEPI — PCE Price Index

**Representasi real world**  
Tracks prices of goods and services included in U.S. personal consumption expenditures.

**Source**  
FRED

**Start date**  
1959-01-01

**End date**  
2026-07-01

**Observations**  
811

**Missing count**  
0

**Data age**  
78 days

**Training model update date**  
Not yet trained

---

## PCEPILFE — Core PCE Price Index

**Representasi real world**  
Tracks prices in U.S. personal consumption expenditures excluding food and energy.

**Source**  
FRED

**Start date**  
1959-01-01

**End date**  
2026-07-01

**Observations**  
811

**Missing count**  
0

**Data age**  
78 days

**Training model update date**  
Not yet trained

---

## PPIFID — Producer Price Index: Final Demand

**Representasi real world**  
Tracks selling prices received by domestic producers for goods and services sold for final demand.

**Source**  
FRED

**Start date**  
2009-11-01

**End date**  
2026-08-01

**Observations**  
202

**Missing count**  
0

**Data age**  
47 days

**Training model update date**  
Not yet trained

---

## PPIACO — Producer Price Index: All Commodities

**Representasi real world**  
Tracks selling prices received by domestic producers for a broad range of commodities.

**Source**  
FRED

**Start date**  
1913-01-01

**End date**  
2026-08-01

**Observations**  
1364

**Missing count**  
0

**Data age**  
47 days

**Training model update date**  
Not yet trained

---

## Credit

## BUSLOANS — Commercial and Industrial Loans

**Representasi real world**  
Measures the outstanding value of commercial and industrial loans held by U.S. commercial banks.

**Source**  
FRED

**Start date**  
1947-01-01

**End date**  
2026-08-01

**Observations**  
956

**Missing count**  
0

**Data age**  
47 days

**Training model update date**  
Not yet trained

---

## TOTALSL — Total Consumer Credit Owned and Securitized

**Representasi real world**  
Measures outstanding consumer credit owned and securitized, covering revolving and nonrevolving credit rather than home mortgages.

**Source**  
FRED

**Start date**  
1943-01-01

**End date**  
2026-07-01

**Observations**  
1003

**Missing count**  
0

**Data age**  
78 days

**Training model update date**  
Not yet trained

---

## DRTSCILM — SLOOS: Banks Tightening C&I Lending Standards

**Representasi real world**  
Measures the net percentage of surveyed banks reporting tighter lending standards for commercial and industrial loans to large and middle-market firms.

**Source**  
FRED

**Start date**  
1990-04-01

**End date**  
2026-07-01

**Observations**  
146

**Missing count**  
0

**Data age**  
78 days

**Training model update date**  
Not yet trained

---

## DRSDCILM — SLOOS: Stronger Demand for C&I Loans

**Representasi real world**  
Measures the net percentage of surveyed banks reporting stronger demand for commercial and industrial loans from large and middle-market firms.

**Source**  
FRED

**Start date**  
1991-10-01

**End date**  
2026-07-01

**Observations**  
140

**Missing count**  
0

**Data age**  
78 days

**Training model update date**  
Not yet trained

---

## DRBLACBS — Delinquency Rate on Business Loans

**Representasi real world**  
Measures the percentage of business loans at commercial banks that are delinquent.

**Source**  
FRED

**Start date**  
1987-01-01

**End date**  
2026-04-01

**Observations**  
158

**Missing count**  
0

**Data age**  
169 days

**Training model update date**  
Not yet trained

---

## Policy / Liquidity

## FEDFUNDS — Federal Funds Effective Rate

**Representasi real world**  
Measures the effective overnight interest rate at which depository institutions lend reserve balances to one another.

**Source**  
FRED

**Start date**  
1954-07-01

**End date**  
2026-08-01

**Observations**  
866

**Missing count**  
0

**Data age**  
47 days

**Training model update date**  
Not yet trained

---

## TOTRESNS — Reserves of Depository Institutions: Total

**Representasi real world**  
Measures total reserves held by depository institutions, including reserve balances and qualifying vault cash.

**Source**  
FRED

**Start date**  
1959-01-01

**End date**  
2026-07-01

**Observations**  
811

**Missing count**  
0

**Data age**  
78 days

**Training model update date**  
Not yet trained

---

## WRESBAL — Reserve Balances with Federal Reserve Banks

**Representasi real world**  
Measures reserve balances held by depository institutions at Federal Reserve Banks.

**Source**  
FRED

**Start date**  
2002-12-18

**End date**  
2026-09-09

**Observations**  
1239

**Missing count**  
0

**Data age**  
8 days

**Training model update date**  
Not yet trained

---

## WALCL — Federal Reserve Total Assets

**Representasi real world**  
Measures the total assets on the Federal Reserve balance sheet.

**Source**  
FRED

**Start date**  
2002-12-18

**End date**  
2026-09-09

**Observations**  
1239

**Missing count**  
0

**Data age**  
8 days

**Training model update date**  
Not yet trained

---

## M2SL — M2 Money Stock

**Representasi real world**  
Measures a broad stock of money that includes currency, transaction deposits, and selected liquid savings instruments.

**Source**  
FRED

**Start date**  
1959-01-01

**End date**  
2026-07-01

**Observations**  
811

**Missing count**  
0

**Data age**  
78 days

**Training model update date**  
Not yet trained

---

## External / Structural

## EXPGSC1 — Real Exports of Goods and Services

**Representasi real world**  
Measures the inflation-adjusted value of U.S. exports of goods and services.

**Source**  
FRED

**Start date**  
1947-01-01

**End date**  
2026-04-01

**Observations**  
318

**Missing count**  
0

**Data age**  
169 days

**Training model update date**  
Not yet trained

---

## IMPGSC1 — Real Imports of Goods and Services

**Representasi real world**  
Measures the inflation-adjusted value of U.S. imports of goods and services.

**Source**  
FRED

**Start date**  
1947-01-01

**End date**  
2026-04-01

**Observations**  
318

**Missing count**  
0

**Data age**  
169 days

**Training model update date**  
Not yet trained

---

## OPHNFB — Nonfarm Business Sector Labor Productivity

**Representasi real world**  
Measures real output per hour worked in the U.S. nonfarm business sector.

**Source**  
FRED

**Start date**  
1947-01-01

**End date**  
2026-04-01

**Observations**  
318

**Missing count**  
0

**Data age**  
169 days

**Training model update date**  
Not yet trained

---

## TCU — Capacity Utilization: Total Industry

**Representasi real world**  
Measures industrial output as a percentage of estimated production capacity across manufacturing, mining, and utilities.

**Source**  
FRED

**Start date**  
1967-01-01

**End date**  
2026-07-01

**Observations**  
715

**Missing count**  
0

**Data age**  
78 days

**Training model update date**  
Not yet trained

---

## Appendix — Original planning notes

The original variable-universe notes are preserved below as historical planning 
context. Candidate measures (such as ISM PMI or a derived real policy rate) are 
not additional available cleaned datasets. The catalog above is authoritative 
for current availability.

<details>
<summary>Original Resources.md content</summary>

```text
Initial US Variable Universe

series_id
name
source
frequency
units
seasonal_adjustment
start_date
end_date
observations
missing_count
missing_pct
latest_observation
data_age

Growth / Activity
Variable	Candidate FRED	Reason
Industrial Production	INDPRO	real production
Real PCE	PCEC96	consumption
Real Personal Income	candidate FRED/BEA series	household income
Real Retail / Trade activity	candidate series	consumption/business
Housing Starts	HOUST	cyclical activity
Building Permits	PERMIT	leading housing
ISM Manufacturing PMI	FRED/ISM where available	survey activity
Labor
Variable	Candidate
Nonfarm Payrolls	PAYEMS
Unemployment Rate	UNRATE
Initial Claims	ICSA
Average Weekly Hours	AWHAETP / suitable series
Job Openings	JTSJOL
Labor Force Participation	CIVPART
Average Hourly Earnings	CES0500000003 or appropriate aggregate
Inflation
Variable	Candidate
CPI	CPIAUCSL
Core CPI	CPILFESL
PCE Price Index	PCEPI
Core PCE	PCEPILFE
Producer Prices	appropriate PPI
Wage growth	from earnings data
Credit
Variable	Candidate
C&I Loans	BUSLOANS
Consumer Credit	TOTALSL
SLOOS standards	Fed series
SLOOS demand	Fed series
Delinquencies	Fed series
Policy / Liquidity
Variable	Candidate
Effective Fed Funds	FEDFUNDS
Bank Reserves	reserve series
Fed Balance Sheet	WALCL
M2	M2SL
Real policy rate	derived, not raw
External / Structural
Variable	Candidate
Real Exports	BEA/FRED
Real Imports	BEA/FRED
Labor Productivity	OPHNFB
Capacity Utilization	TCU
```

</details>
