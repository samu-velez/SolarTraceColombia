from __future__ import annotations
from io import BytesIO
import pandas as pd
from ..core.cache import cache

# Aliases de métricas (se aplican después de normalizar encabezados)
ALIASES = {
    "wind_generation": "wind-generation",
    "wind_generation_twh": "wind-generation",
    "wind_energy_consumption": "wind-energy-consumption",
    "solar_energy_consumption": "solar-energy-consumption",
    "hydropower_consumption": "hydropower-consumption",
    "biofuel_production": "biofuel-production",
    "installed_geothermal_capacity": "installed-geothermal-capacity",
    "cumulative_installed_wind_energy_capacity_gw": "cumulative-installed-wind-energy-capacity-gigawatts",
    "installed_solar_pv_capacity": "installed-solar-PV-capacity",
    "share_electricity_renewables": "share-electricity-renewables",
    "share_electricity_wind": "share-electricity-wind",
    "share_electricity_solar": "share-electricity-solar",
    "share_electricity_hydro": "share-electricity-hydro",
    "electricity_generation": "electricity-generation",
    "electricity_consumption": "electricity-consumption",
    "modern_renewable_energy_consumption": "modern-renewable-energy-consumption",
    "renewable_share_energy": "share-electricity-renewables",  # por si viene así
}

STANDARD_COLS = set(ALIASES.values()) | {
    "country", "year", "modern-renewable-energy-consumption",
}

# Posibles nombres de columnas para country/year
HEADER_ALIASES = {
    "country": {"country", "entity", "location", "country_name", "area", "name"},
    "year":    {"year", "time", "period", "date"},
}

def _std(s: str) -> str:
    s = s.encode("utf-8").decode("utf-8-sig")
    s = s.strip().replace("-", "_").replace(" ", "_").lower()
    return s

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # 1) normaliza a snake
    norm_map = {c: _std(str(c)) for c in df.columns}
    df = df.rename(columns=norm_map)

    # 2) country/year por alias
    def _ensure_col(target_key: str):
        if target_key in df.columns:
            return
        for c in list(df.columns):
            if c in HEADER_ALIASES[target_key]:
                df.rename(columns={c: target_key}, inplace=True)
                return

    _ensure_col("country")
    _ensure_col("year")

    # 3) métricas a nombres estándar
    met_map = {}
    for c in df.columns:
        met_map[c] = ALIASES.get(c, c)
    df = df.rename(columns=met_map)

    return df

def _read_csv_robust(file_bytes: bytes) -> pd.DataFrame:
    for args in (
        dict(),
        dict(sep=None, engine="python"),
        dict(sep=";", engine="python"),
        dict(sep=",", engine="python", on_bad_lines="skip"),
        dict(sep=",", engine="python", on_bad_lines="skip", encoding="latin-1"),
    ):
        try:
            return pd.read_csv(BytesIO(file_bytes), **args)
        except Exception:
            continue
    return pd.read_csv(BytesIO(file_bytes))

def load_dataframe(file_bytes: bytes, filename: str) -> dict:
    df = _read_csv_robust(file_bytes)
    df = _normalize_columns(df)

    if "country" not in df.columns or "year" not in df.columns:
        raise ValueError(f"El CSV debe contener columnas 'country' y 'year'. Encabezados: {list(df.columns)[:20]}")

    # Qué columnas de este archivo conservamos
    keep = [c for c in df.columns if c in (STANDARD_COLS | {"country", "year"})]
    if not keep:
        keep = [c for c in ["country", "year"] if c in df.columns]
    df_keep = df[keep].copy()

    # 🔑 FUSIÓN INCREMENTAL: si ya hay dataset cargado, hacemos outer-merge por country+year
    if cache.df is None:
        merged = df_keep
    else:
        merged = pd.merge(cache.df, df_keep, on=["country", "year"], how="outer")

    cache.df = merged
    cache.columns = list(merged.columns)
    cache.last_filename = filename
    return {"columns": cache.columns, "count": len(cache.df), "last_filename": filename}

def get_rows(offset=0, limit=100):
    if cache.df is None:
        return 0, []
    total = len(cache.df)
    page = cache.df.iloc[offset: offset + limit].fillna(0).to_dict(orient="records")
    return total, page