from flask import Flask, request, render_template
import requests
from requests.auth import HTTPBasicAuth
import os
from datetime import datetime

app = Flask(__name__)

USER_ID = os.environ.get("USER_ID")
API_KEY = os.environ.get("API_KEY")
APPOINTMENT_TYPE_ID = os.environ.get("APPOINTMENT_TYPE_ID")

@app.route("/", methods=["GET"])
def form():
    return render_template("form.html")

@app.route("/buchen", methods=["POST"])
def buchen():
    first = request.form["firstName"].strip().upper()
    last = request.form["lastName"].strip().upper()
    email = request.form.get("email", "").strip() or "anonym@example.com"
    phone = request.form.get("phone", "").strip()
    datetime_input = request.form["datetime"].strip()
    location = request.form.get("location", "nicht angegeben")

    data = {
        "appointmentTypeID": APPOINTMENT_TYPE_ID,
        "datetime": datetime_input,
        "firstName": first,
        "lastName": last,
        "email": email,
        "phone": phone,
        "notes": f"Ort der Sitzung: {location}"
    }

    response = requests.post(
        "https://acuityscheduling.com/api/v1/appointments",
        auth=HTTPBasicAuth(USER_ID, API_KEY),
        json=data
    )

    if response.status_code == 200:
        return "Termin erfolgreich gebucht!"
    else:
        return f"Fehler: {response.text}", 400
