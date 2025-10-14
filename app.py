from flask import Flask, request, jsonify
from flask_cors import CORS

import json
import numpy as np
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Povolenie CORS – fajn na vývoj, v produkcii radšej obmedziť domény.

# cesta k súboru so študentmi.
DATA_PATH = Path(__file__).parent / "students.json"


@app.get("/Students")
def students():
    """
    Vracia obsah súboru students.json.
    """
    # city = request.args.get("Town")

    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        # Vráť konzistentnú JSON chybu (prehľadnejšie pre front-end).
        return jsonify({"error": "students.json not found"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "students.json has invalid JSON"}), 500

    # Príklad filtrovania – nechávam zakomentované, keďže si ho mal tiež tak.
    # if city:
    #     data = [x for x in data if x.get("City") == city]

    # Vráť ako JSON; vracanie „čistej“ Python štruktúry list by v staršom Flasku zlyhalo.
    return jsonify(data), 200


@app.get("/Predict")
def predict():
    """
    Lineárna extrapolácia skóre pre 6. test zo zadaných 5 skóre.
    Očakávaný formát: ?Scores=10 20 30 40 50
    Výstup je orezaný na <0, 100>.
    """
    scores_raw = request.args.get("Scores", "").strip()
    if not scores_raw:
        return jsonify({"error": "Missing Scores. Example: ?Scores=10 20 30 40 50"}), 400

    # Rozparsuj a over čísla
    try:
        y = [float(i) for i in scores_raw.split()]
    except ValueError:
        return jsonify({"error": "Scores must be numbers separated by spaces"}), 400

    if len(y) != 5:
        return jsonify({"error": "Provide exactly 5 scores"}), 400

    # x sú indexy testov 1..5, y sú skóre
    x = np.array([1, 2, 3, 4, 5], dtype=float)
    y = np.array(y, dtype=float)

    # np.polyfit vráti koeficienty lineárnej regresie (m*slope, b*intercept)
    m, b = np.polyfit(x, y, 1)

    # Predikcia pre „6. test“ (extrapolácia)
    pred = m * 6 + b

    # Orezanie na rozsah 0..100
    pred = max(0.0, min(100.0, float(pred)))

    # Konzistentný JSON výstup + zaokrúhlenie
    return jsonify({"prediction": round(pred, 2)}), 200


if __name__ == "__main__":
    # debug=True je užitočné pri vývoji (autoreload, tracebacky)
    app.run(debug=True)
