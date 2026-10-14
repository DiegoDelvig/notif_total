import requests
from datetime import datetime
from src import config

def fetch_station() -> dict | None:
    """Retourne la station, ou None si elle n'existe plus dans les données."""
    r = requests.get(config.API_URL, params={"where": f"id={config.STATION_ID}", "limit": 1}, timeout=20)
    r.raise_for_status()
    res = r.json().get("results", [])
    return res[0] if res else None

def get_available_fuels(station: dict) -> set[str]:
    val = station.get("carburants_disponibles") or []
    if isinstance(val, str):
        val = val.split(",")
    return {c.strip() for c in val if c.strip()}

def get_price(station: dict, fuel: str) -> str:
    p = station.get(f"{fuel.lower()}_prix")
    return f"{p:.3f} EUR" if isinstance(p, (int, float)) else "prix inconnu"

def get_last_update(station: dict, fuels: list[str]) -> datetime | None:
    dates = []
    for f in fuels:
        v = station.get(f"{f.lower()}_maj")
        if v:
            dates.append(datetime.fromisoformat(v))
    return max(dates) if dates else None
