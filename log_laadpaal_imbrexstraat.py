#!/usr/bin/env python3
import csv
import os
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

import requests

# Instellingen
STATION_ID = "5j6my7"
API_URL = f"https://api.chargefinder.com/status/{STATION_ID}"
CSV_BESTAND = "laadpaal_imbrexstraat_log.csv"
TIMEZONE = "Europe/Amsterdam"

# Headers om op een 'normale browser' te lijken
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; laadpaal-logger/1.0)",
    "Origin": "https://chargefinder.com",
    "Referer": "https://chargefinder.com/",
}


def haal_aantal_beschikbaar():
    """Haalt via de Chargefinder API op hoeveel connectors beschikbaar zijn.
    Geeft -1 terug als er iets misgaat, zodat we dat kunnen loggen.
    """
    try:
        resp = requests.get(API_URL, headers=HEADERS, timeout=10)
    except Exception as e:
        print(f"[ERROR] HTTP request naar Chargefinder faalde: {e}")
        return -1

    print(f"[DEBUG] HTTP status: {resp.status_code}")

    # Als de status geen 200 is, toch loggen dat er iets mis is
    if resp.status_code != 200:
        print(f"[ERROR] Onverwachte status code {resp.status_code}")
        return -1

    try:
        data = resp.json()
    except ValueError as e:
        print(f"[ERROR] Kon JSON niet parsen: {e}")
        return -1

    # Data kan of een lijst zijn, of een dict met 'connectors'
    if isinstance(data, dict) and "connectors" in data:
        connectors = data.get("connectors", [])
    else:
        connectors = data if isinstance(data, list) else []

    print(f"[DEBUG] Aantal connectors in response: {len(connectors)}")

    beschikbaar = 0
    for connector in connectors:
        status = connector.get("status")
        # Veel voorbeelden gebruiken status == 2 als 'vrij'
        if status == 2:
            beschikbaar += 1

    print(f"[DEBUG] Aantal beschikbare connectors (status==2): {beschikbaar}")
    return beschikbaar


def log_record(aantal_beschikbaar):
    """Schrijft een regel weg naar CSV met datum, tijd en aantal beschikbaar."""
    tz = ZoneInfo(TIMEZONE)
    nu = datetime.now(tz)
    datum = nu.date().isoformat()          # bv. 2025-12-01
    tijd = nu.strftime("%H:%M:%S")         # bv. 14:00:00

    bestand_bestaat = os.path.exists(CSV_BESTAND)

    with open(CSV_BESTAND, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        # Header alleen schrijven als het bestand nog niet bestond
        if not bestand_bestaat:
            writer.writerow(["datum", "tijd", "aantal_beschikbaar_van_2"])
        writer.writerow([datum, tijd, aantal_beschikbaar])


def main():
    # We zorgen dat er ALTIJD iets gelogd wordt, ook bij fouten.
    try:
        aantal = haal_aantal_beschikbaar()
    except Exception as e:
        print(f"[ERROR] Onverwachte fout in main(): {e}")
        aantal = -1

    log_record(aantal)
    print(f"Gelogd: {aantal} van de 2 laadpunten beschikbaar (of -1 = fout).")


if __name__ == "__main__":
    main()
