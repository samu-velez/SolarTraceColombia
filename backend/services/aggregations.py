from __future__ import annotations
from typing import Optional
import pandas as pd
from ..core.cache import cache

def _df() -> pd.DataFrame:
    if cache.df is None:
        raise ValueError("No hay dataset cargado")
    return cache.df

def latest_year(df: pd.DataFrame, country: str | None) -> int:
    d = df if not country else df[df["country"] == country]
    return int(d["year"].max())

def production_by_source(country: Optional[str]= None, year: Optional[int] = None):
    df = _df()
    if year is None:
        year = latest_year(df, country)
    d = df[df["year"] == year]
    if country:
        d = d[d["country"] == country]

    def val(col):
        return float(d[col].sum()) if col in d else 0.0

    items = [
        {"label": "wind",       "value": val("wind-generation")},
        {"label": "solar",      "value": val("solar-energy-consumption")},
        {"label": "hydro",      "value": val("hydropower-consumption")},
        {"label": "biofuel",    "value": val("biofuel-production")},
        {"label": "geothermal", "value": val("installed-geothermal-capacity")},
    ]
    return year, items

def renewables_share_breakdown(country: Optional[str]= None, year: Optional[int] = None):
    df = _df()
    if year is None:
        year = latest_year(df, country)
    d = df[df["year"] == year]
    if country:
        d = d[d["country"] == country]

    def mean(col):
        return float(d[col].mean()) if col in d else 0.0

    return year, {
        "renewables": mean("share-electricity-renewables"),
        "wind":       mean("share-electricity-wind"),
        "solar":      mean("share-electricity-solar"),
        "hydro":      mean("share-electricity-hydro"),
    }

def installed_capacity_trends(country: Optional[str]= None):
    df = _df()
    d = df if not country else df[df["country"] == country]
    g = d.groupby("year").mean(numeric_only=True).reset_index()
    out = []
    for _, row in g.iterrows():
        out.append({
            "year": int(row["year"]),
            "wind_gw":   float(row.get("cumulative-installed-wind-energy-capacity-gigawatts", 0)),
            "solar_pv":  float(row.get("installed-solar-PV-capacity", 0)),
            "geothermal":float(row.get("installed-geothermal-capacity", 0)),
        })
    return out

def renewable_vs_conventional(country: Optional[str]= None):
    df = _df()
    d = df if not country else df[df["country"] == country]
    out = []
    for y, g in d.groupby("year"):
        ren = float(g.get("modern-renewable-energy-consumption", 0).mean()) if "modern-renewable-energy-consumption" in g else None
        total_el = float(g.get("electricity-consumption", 0).mean()) if "electricity-consumption" in g else None
        if ren is not None and total_el is not None and total_el > 0:
            conv = max(total_el - ren, 0.0)
            out.append({"year": int(y), "renewable": ren, "conventional": conv})
    return out