#!/usr/bin/with-contenv bashio

bashio::log.info "Starte Wärmepumpen Tracker..."
mkdir -p /data

cd /app
python3 app.py
