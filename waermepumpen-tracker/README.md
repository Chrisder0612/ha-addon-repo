# Wärmepumpen Tracker – Home Assistant Add-on

Erfasse, visualisiere und exportiere tägliche Messwerte deiner Wärmepumpe direkt in Home Assistant.

## Features

- **Dashboard** – farbige Metrikkarten (Verbrauch, Ertrag, JAZ, Außentemperatur, Gesamt-JAZ)
- **Diagramm** – kombiniertes Balken-/Liniendiagramm der letzten 14 Einträge
- **Dateneingabe** – einfaches Formular für tägliche Messwerte
- **CSV-Export** – Excel-kompatibler Export (Semikolon-getrennt, mit BOM) per Knopfdruck
- **Persistent** – alle Daten werden in `/data/readings.json` gespeichert

## Datenfelder

| Feld               | Pflicht | Beschreibung                     |
|--------------------|---------|----------------------------------|
| Datum              | ✓       | Messdatum (YYYY-MM-DD)           |
| Stromverbrauch     | ✓       | Elektrische Energie in kWh       |
| Wärmeertrag        | ✓       | Thermische Energie in kWh        |
| Außentemperatur    |         | Tagesmittel in °C                |
| Vorlauftemperatur  |         | Heizwasservorlauf in °C          |
| Rücklauftemperatur |         | Heizwasserrücklauf in °C         |

Die **JAZ** (Jahresarbeitszahl) wird automatisch berechnet: `JAZ = Wärmeertrag / Stromverbrauch`

## Installation

1. Repo-URL in Home Assistant hinzufügen:  
   `https://github.com/Chrisder0612/ha-addon-repo`
2. Add-on **Wärmepumpen Tracker** installieren
3. Add-on starten
4. Im HA-Seitenmenü unter **Wärmepumpe** öffnen

## API

Das Add-on stellt eine REST-API auf Port 8765 bereit:

| Methode | Endpunkt                  | Beschreibung                  |
|---------|---------------------------|-------------------------------|
| GET     | `/api/readings`           | Alle Einträge (JSON)          |
| POST    | `/api/readings`           | Neuen Eintrag speichern       |
| DELETE  | `/api/readings/<id>`      | Eintrag löschen               |
| GET     | `/api/stats`              | Statistiken (Ø JAZ, Summen)   |
| GET     | `/api/export/csv`         | CSV-Export herunterladen      |
