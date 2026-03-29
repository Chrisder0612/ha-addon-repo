# 🔥 Wärmepumpen Monitor – HAOS Add-on

## Schritt 1: GitHub Repository anlegen

1. Geh auf **github.com** und melde dich an (oder erstelle einen Account)
2. Klick auf **"New repository"**
3. Name: `ha-addon-repo`
4. Auf **"Add file" → "Upload files"** klicken
5. Den kompletten Inhalt dieses Ordners hochladen (alle Dateien und Unterordner)
6. In `repository.yaml` deinen GitHub-Nutzernamen eintragen (statt `DEIN_GITHUB_NAME`)

Deine Repo-URL sieht dann so aus:
```
https://github.com/DEIN_GITHUB_NAME/ha-addon-repo
```

---

## Schritt 2: Add-on Repository in HA hinzufügen

1. Home Assistant öffnen
2. **Einstellungen → Add-ons → Add-on Store**
3. Oben rechts die **drei Punkte** → **"Repositories"**
4. Deine GitHub-URL einfügen:
   ```
   https://github.com/DEIN_GITHUB_NAME/ha-addon-repo
   ```
5. **"Hinzufügen"** klicken
6. Seite neu laden

---

## Schritt 3: Add-on installieren

1. Im Add-on Store scrollst du runter → **"Wärmepumpen Monitor"** erscheint
2. **Installieren** klicken (dauert 1–2 Minuten beim ersten Mal)
3. **Starten**
4. Optional: **"Im Seitenmenü anzeigen"** aktivieren

---

## Zugriff

```
http://<PI-IP>:5000
```

Die Daten werden unter `/data/daten.json` gespeichert —
das ist der persistente HAOS-Speicher, überlebt Updates und Neustarts.

---

## Dateistruktur

```
ha-addon-repo/
├── repository.yaml              ← Pflicht für HA Add-on Repos
└── waermepumpe/
    ├── config.yaml              ← Add-on Metadaten & Port-Konfiguration
    ├── Dockerfile               ← Container-Build
    ├── run.sh                   ← Startskript
    ├── app.py                   ← Flask Backend
    └── templates/
        └── index.html           ← Frontend
```
