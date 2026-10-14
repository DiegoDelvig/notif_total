import time
from datetime import datetime, timezone, timedelta
from src import config, api, state, notifier

def log(*args):
    print(time.strftime("%Y-%m-%d %H:%M:%S"), *args, flush=True)

def check():
    current_state = state.load()

    # 1. Récupération des données
    try:
        station = api.fetch_station()
    except Exception as e:
        current_state["fails"] = current_state.get("fails", 0) + 1
        log(f"Erreur API ({current_state['fails']}) :", e)
        if current_state["fails"] >= config.FAIL_ALERT and not current_state.get("fail_alerted"):
            notifier.notify("L'API des carburants est injoignable.", "Surveillance en panne", "high")
            current_state["fail_alerted"] = True
        state.save(current_state)
        return

    if current_state.get("fail_alerted"):
        notifier.notify("L'API répond de nouveau.", "Surveillance rétablie")
    current_state["fails"], current_state["fail_alerted"] = 0, False

    if station is None:
        if not current_state.get("missing_alerted"):
            notifier.notify(f"Station {config.STATION_ID} absente.", "Station introuvable", "high")
            current_state["missing_alerted"] = True
        state.save(current_state)
        return
    current_state["missing_alerted"] = False

    # 2. Changements de disponibilité
    dispo_actuelle = api.get_available_fuels(station)
    now = sorted(c for c in config.WATCH if c in dispo_actuelle)
    prev = current_state.get("available")
    where = station.get("adresse", "station")
    log("Disponibles surveillés :", now or "aucun")

    # Récupération et formatage de la date de mise à jour
    upd = api.get_last_update(station, now)
    maj_str = upd.strftime("%d/%m/%Y à %H:%M") if upd else "inconnue"

    if prev is None:
        notifier.notify(
            f"{where}\nDisponibles : {', '.join(sorted(dispo_actuelle)) or 'aucun'}\n"
            f"Surveillés : {', '.join(config.WATCH)}\n"
            f"Dernière MAJ station : {maj_str}", 
            "Surveillance démarrée"
        )
    else:
        # Nouveaux carburants disponibles
        for f in sorted(set(now) - set(prev)):
            notifier.notify(f"{f} disponible à {where} ({api.get_price(station, f)})", f"{f} disponible", "high")
        # Carburants tombés en rupture
        for f in sorted(set(prev) - set(now)):
            notifier.notify(f"{f} en rupture à {where}", f"{f} en rupture")
            
    current_state["available"] = now

    # 3. Données périmées
    upd = api.get_last_update(station, now)
    stale = bool(upd and datetime.now(timezone.utc) - upd > timedelta(days=config.STALE_DAYS))
    if stale and not current_state.get("stale_alerted"):
        notifier.notify(f"Aucune mise à jour depuis le {upd:%d/%m %H:%M}.", "Données périmées")
    current_state["stale_alerted"] = stale

    state.save(current_state)
