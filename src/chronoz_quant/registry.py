"""Canonical series metadata. Paths are relative to the project root."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Series:
    series_id: str
    name: str
    category: str
    expected_frequency: str
    source: str
    raw_path: str
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
