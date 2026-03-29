from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime

app = Flask(__name__)

# /data wird von HAOS persistent gespeichert (überlebt Updates/Neustarts)
DATA_FILE = "/data/daten.json"

def lade_daten():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def speichere_daten(daten):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(daten, f, indent=2, ensure_ascii=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/eintraege", methods=["GET"])
def get_eintraege():
    daten = lade_daten()
    return jsonify(sorted(daten, key=lambda x: x["datum"]))

@app.route("/api/eintraege", methods=["POST"])
def add_eintrag():
    body = request.json
    for feld in ["datum", "verbrauch", "energieleistung", "aussentemp", "jaz"]:
        if not body.get(feld) and body.get(feld) != 0:
            return jsonify({"fehler": f"Feld '{feld}' fehlt"}), 400
    eintrag = {
        "id": int(datetime.now().timestamp() * 1000),
        "datum": body["datum"],
        "verbrauch": float(body["verbrauch"]),
        "energieleistung": float(body["energieleistung"]),
        "aussentemp": float(body["aussentemp"]),
        "jaz": float(body["jaz"]),
        "notiz": body.get("notiz", "")
    }
    daten = lade_daten()
    daten.append(eintrag)
    speichere_daten(daten)
    return jsonify(eintrag), 201

@app.route("/api/eintraege/<int:eintrag_id>", methods=["DELETE"])
def delete_eintrag(eintrag_id):
    daten = lade_daten()
    neue_daten = [e for e in daten if e["id"] != eintrag_id]
    if len(neue_daten) == len(daten):
        return jsonify({"fehler": "Nicht gefunden"}), 404
    speichere_daten(neue_daten)
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
