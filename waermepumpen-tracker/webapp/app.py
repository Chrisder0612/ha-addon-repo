import os
import json
import csv
import io
from datetime import datetime
from flask import Flask, request, jsonify, render_template, Response

app = Flask(__name__)
DATA_FILE = '/data/readings.json'


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def calc_jaz(reading):
    v = reading.get('verbrauch', 0)
    e = reading.get('ertrag', 0)
    if v and v > 0:
        return round(e / v, 3)
    return None


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/readings', methods=['GET'])
def get_readings():
    return jsonify(load_data())


@app.route('/api/readings', methods=['POST'])
def add_reading():
    body = request.get_json(force=True)
    if not body:
        return jsonify({'error': 'Kein JSON'}), 400

    required = ['date', 'verbrauch', 'ertrag']
    for field in required:
        if field not in body or body[field] is None:
            return jsonify({'error': f'Pflichtfeld fehlt: {field}'}), 400

    reading = {
        'id': datetime.utcnow().isoformat() + 'Z',
        'date': body['date'],
        'verbrauch': float(body['verbrauch']),
        'ertrag': float(body['ertrag']),
        'aussenTemp': float(body.get('aussenTemp', 0)),
        'vorlauf': float(body.get('vorlauf', 0)),
        'ruecklauf': float(body.get('ruecklauf', 0)),
    }

    readings = load_data()
    readings.append(reading)
    readings.sort(key=lambda r: r['date'])
    save_data(readings)

    return jsonify({'ok': True, 'reading': reading}), 201


@app.route('/api/readings/<reading_id>', methods=['DELETE'])
def delete_reading(reading_id):
    readings = load_data()
    before = len(readings)
    readings = [r for r in readings if r.get('id') != reading_id]
    if len(readings) == before:
        return jsonify({'error': 'Nicht gefunden'}), 404
    save_data(readings)
    return jsonify({'ok': True})


@app.route('/api/export/csv')
def export_csv():
    readings = load_data()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    writer.writerow([
        'Datum',
        'Stromverbrauch (kWh)',
        'Wärmeertrag (kWh)',
        'JAZ',
        'Außentemp. (°C)',
        'Vorlauf (°C)',
        'Rücklauf (°C)',
    ])

    for r in readings:
        jaz = calc_jaz(r)
        writer.writerow([
            r.get('date', ''),
            str(r.get('verbrauch', '')).replace('.', ','),
            str(r.get('ertrag', '')).replace('.', ','),
            str(jaz).replace('.', ',') if jaz is not None else '',
            str(r.get('aussenTemp', '')).replace('.', ','),
            str(r.get('vorlauf', '')).replace('.', ','),
            str(r.get('ruecklauf', '')).replace('.', ','),
        ])

    output.seek(0)
    filename = f'waermepumpe_{datetime.now().strftime("%Y%m%d")}.csv'
    return Response(
        '\ufeff' + output.getvalue(),   # BOM für Excel
        mimetype='text/csv; charset=utf-8',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )


@app.route('/api/stats')
def stats():
    readings = load_data()
    if not readings:
        return jsonify({})

    jaz_values = [calc_jaz(r) for r in readings if calc_jaz(r)]
    total_v = sum(r.get('verbrauch', 0) for r in readings)
    total_e = sum(r.get('ertrag', 0) for r in readings)

    return jsonify({
        'count': len(readings),
        'avg_jaz': round(sum(jaz_values) / len(jaz_values), 2) if jaz_values else None,
        'total_verbrauch': round(total_v, 2),
        'total_ertrag': round(total_e, 2),
        'overall_jaz': round(total_e / total_v, 2) if total_v > 0 else None,
    })


if __name__ == '__main__':
    os.makedirs('/data', exist_ok=True)
    app.run(host='0.0.0.0', port=8765, debug=False)
