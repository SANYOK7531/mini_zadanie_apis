import pyodbc
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔗 Підключення до Azure SQL
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:petsafrance.database.windows.net,1433;"
    "Database=cvik2db;"
    "Uid=sanya;"
    "Pwd=peca009169@;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

@app.get("/Students")
def students():
    city = request.args.get("City")
    students = []

    try:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()

            if city:
                query = "SELECT Id, Name, Gender, City, EnrollmentDate FROM Students WHERE City = ?"
                cursor.execute(query, (city,))
            else:
                query = "SELECT Id, Name, Gender, City, EnrollmentDate FROM Students"
                cursor.execute(query)

            for row in cursor.fetchall():
                students.append({
                    "Id": row[0],
                    "Name": row[1],
                    "Gender": row[2],
                    "City": row[3],
                    "EnrollmentDate": row[4].strftime("%Y-%m-%d")
                })

        return jsonify(students), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
