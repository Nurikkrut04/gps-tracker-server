from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

TRACK_FILE = "track.json"

# ======= Загрузка данных =======
def load_track():
    if not os.path.exists(TRACK_FILE):
        return []
    with open(TRACK_FILE, "r") as f:
        return json.load(f)

# ======= Сохранение данных =======
def save_track(track):
    with open(TRACK_FILE, "w") as f:
        json.dump(track, f)

# ======= Страница карты =======
@app.route("/map")
def map_view():
    return render_template("map.html")

# ======= API получения точек =======
@app.route("/api/track")
def api_track():
    return jsonify(load_track())

# ======= Приём координат от ESP32 =======
@app.route("/submit", methods=["POST"])
def submit():
    try:
        data = request.get_json()
        lat = float(data.get("lat"))
        lon = float(data.get("lon"))

        print(f"[+] Новая точка: {lat}, {lon}")
        track = load_track()
        track.append({"lat": lat, "lon": lon})
        save_track(track)

        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print("Ошибка:", e)
        return jsonify({"status": "error", "message": str(e)}), 400

# ======= Главная =======
@app.route("/")
def index():
    return "<h1>GPS Tracker Server работает!</h1>"

# ======= Flask запуск =======
if __name__ == "__main__":
    app.run(debug=True)
