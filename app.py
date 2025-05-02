# gps_tracker/app.py
from flask import Flask, request, render_template, jsonify
import time

app = Flask(__name__)

# Временное хранилище координат
coordinates = []

@app.route('/')
def home():
    return "Сервер GPS трекера работает. Перейдите на /map"

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    lat = data.get("lat")
    lon = data.get("lon")
    if lat is not None and lon is not None:
        coordinates.append({
            "lat": lat,
            "lon": lon,
            "timestamp": time.time()
        })
        return jsonify({"status": "ok"})
    return jsonify({"status": "error", "message": "invalid data"}), 400

@app.route('/api/track')
def api_track():
    return jsonify(coordinates)

@app.route('/map')
def map_view():
    return render_template("map.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # обязательно для Render
