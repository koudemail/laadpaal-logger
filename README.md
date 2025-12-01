# Laadpaal Logger (Chargefinder Nijmegen Imbrexstraat)

Dit project logt ieder uur de beschikbaarheid van de twee laadpunten op:
https://chargefinder.com/nl/laadpaal-nijmegen-imbrexstraat/5j6my7

De data wordt weggeschreven naar een CSV-bestand in de repository.

## Bestanden

- `log_laadpaal_imbrexstraat.py` — Python script dat de Chargefinder API aanroept en de CSV bijwerkt.
- `requirements.txt` — Python dependencies (alleen `requests`).
- `.github/workflows/laadpaal_logger.yml` — GitHub Actions workflow die het script ieder uur draait.
- `laadpaal_imbrexstraat_log.csv` — Logbestand (wordt automatisch aangemaakt als het nog niet bestaat).

## Gebruik

1. Maak een nieuwe GitHub repository (mag privé zijn).
2. Upload de inhoud van deze map (of importeer de ZIP) in de repository.
3. Zorg dat GitHub Actions ingeschakeld is voor je account/repo.
4. Push naar `main` of `master`.
5. GitHub Actions zal nu ieder uur het script draaien en de CSV bijwerken.

Je vindt de run-logs onder het tabblad **Actions** in GitHub.
