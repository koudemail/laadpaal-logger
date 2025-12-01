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
    """Haalt via de Chargefinder API op hoeveel connectors beschikbaar zijn."""
    resp = requests.get(API_URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    data = resp.json()
    # Aanname: elk element in 'data' is een connector met een 'status' veld.
    # In publieke voorbeelden betekent:
    #   status == 2  => beschikbaar
    beschikbaar = 0
    if isinstance(data, dict) and "connectors" in data:
        # fallback als API structuur een 'connectors'-veld heeft
        connectors = data.get("connectors", [])
    else:
        connectors = data

    for connector in connectors:
        status = connector.get("status")
        if status == 2:
            beschikbaar += 1

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
    try:
        aantal = haal_aantal_beschikbaar()
        log_record(aantal)
        print(f"Gelogd: {aantal} van de 2 laadpunten beschikbaar.")
    except Exception as e:
        # Foutmelding naar stdout/stderr zodat je via logs kunt zien wat er misgaat
        print(f"Fout tijdens ophalen of loggen: {e}")


if __name__ == "__main__":
    main()
