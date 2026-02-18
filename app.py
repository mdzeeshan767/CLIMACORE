from flask import Flask, render_template, request, redirect, session, jsonify
from config import get_db_connection

app = Flask(__name__)
app.secret_key = "climacore_secret"

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            session["user"] = user["username"]
            return redirect("/dashboard")
        else:
            return "Invalid Credentials"

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM temperature_readings ORDER BY recorded_at DESC")
    readings = cursor.fetchall()

    conn.close()

    return render_template("dashboard.html", readings=readings)

# ---------------- ADD TEMPERATURE ----------------
@app.route("/add", methods=["POST"])
def add_temperature():
    location = request.form["location"]
    temperature = request.form["temperature"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO temperature_readings (location, temperature) VALUES (%s, %s)",
        (location, temperature)
    )
    conn.commit()
    conn.close()

    return redirect("/dashboard")

# ---------------- REPORTS ----------------
@app.route("/reports")
def reports():
    return render_template("reports.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
