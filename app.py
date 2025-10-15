from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import numpy as np
from pathlib import Path

app = Flask(__name__)
CORS(app)

# файл зі студентами
DATA_PATH = Path(__file__).parent / "students.json"

@app.get("/Students")
def students():
    """
    Vracia obsah súboru students.json (s voliteľným filtrovaním podľa mesta).
    """
    city = request.args.get("City")  # <-- отримуємо місто з URL

    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return jsonify({"error": "students.json not found"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "students.json has invalid JSON"}), 500

    # якщо користувач вказав місто → відфільтрувати
    if city:
        city_lower = city.strip().lower()
        data = [x for x in data if x.get("City", "").lower() == city_lower]

    return jsonify(data), 200


@app.get("/Predict")
def predict():
    scores_raw = request.args.get("Scores", "").strip()
    if not scores_raw:
        return jsonify({"error": "Missing Scores"}), 400
    try:
        y = [float(i) for i in scores_raw.split()]
    except ValueError:
        return jsonify({"error": "Scores must be numbers"}), 400
    if len(y) != 5:
        return jsonify({"error": "Provide exactly 5 scores"}), 400

    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array(y, dtype=float)
    m, b = np.polyfit(x, y, 1)
    pred = max(0.0, min(100.0, float(m * 6 + b)))
    return jsonify({"prediction": round(pred, 2)}), 200

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
