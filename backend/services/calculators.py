from __future__ import annotations
from typing import Optional
from ..core.cache import cache

def _choose_country_year(country: Optional[str], year: Optional[int]):
    df = cache.df
    if df is None:
        raise ValueError("No hay dataset cargado")
    if country:
        d = df[df["country"] == country]
        if d.empty:
            d = df
            country = "Global"
    else:
        d = df
        country = "Global"
    if year is None:
        year = int(d["year"].max())
    return country, int(year)

def _mean(d, col):
    return float(d[col].mean()) if col in d and not d[col].isna().all() else None

def user_renewable_percentage(kwh_total: float, country: Optional[str], year: Optional[int]):
    df = cache.df
    country2, year2 = _choose_country_year(country, year)
    d = df[df["year"] == year2]
    if country2 != "Global":
        d = d[d["country"] == country2]

    share = _mean(d, "share-electricity-renewables")
    method = "share-electricity-renewables"
    breakdown = {
        "share_renewables": share,
        "share_wind": _mean(d, "share-electricity-wind"),
        "share_solar": _mean(d, "share-electricity-solar"),
        "share_hydro": _mean(d, "share-electricity-hydro"),
    }

    if share is None:
        parts = [p for p in [breakdown["share_wind"], breakdown["share_solar"], breakdown["share_hydro"]] if p is not None]
        if parts:
            share = sum(parts)
            method = "sum(shares por fuente)"
        else:
            wind  = _mean(d, "wind-generation") or 0
            solar = _mean(d, "solar-energy-consumption") or 0
            hydro = _mean(d, "hydropower-consumption") or 0
            bio   = _mean(d, "biofuel-production") or 0
            geo   = _mean(d, "installed-geothermal-capacity") or 0
            total_el = _mean(d, "electricity-consumption") or _mean(d, "electricity-generation")
            if total_el and total_el > 0:
                ren = wind + solar + hydro + bio + geo
                share = ren / total_el
                method = "ren/total derivado"
                breakdown.update({"ren_calc": ren, "total_el": total_el})
            else:
                raise ValueError("No es posible derivar el share con las columnas disponibles")

    share = max(0.0, min(1.0, float(share)))
    return country2, year2, share, method, breakdown

def user_renewable_percentage(kwh_total: float, country: Optional[str], year: Optional[int]):
    country2, year2, share, method, breakdown = renewable_share(country, year)
    renewable_kwh = kwh_total * share
    return {
        "country": country2,
        "year": year2,
        "renewable_share": share,
        "renewable_kwh": renewable_kwh,
        "percent_of_user_consumption": share * 100.0,
        "method": method,
        "breakdown": breakdown,
    }
