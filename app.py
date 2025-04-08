from flask import Flask, request, jsonify, render_template
import requests
from requests.auth import HTTPBasicAuth
import os

app = Flask(__name__)

USER_ID = os.environ.get("USER_ID")
API_KEY = os.environ.get("API_KEY")
APPOINTMENT_TYPE_ID = os.environ.get("APPOINTMENT_TYPE_ID")

@app.route("/")
def index():
    return render_template("calendar.html")

@app.route("/slots")
def slots():
    response = requests.get(
        f"https://acuityscheduling.com/api/v1/availability/times?appointmentTypeID={APPOINTMENT_TYPE_ID}",
        auth=HTTPBasicAuth(USER_ID, API_KEY)
    )
    if response.status_code != 200:
        return jsonify([])

    times = response.json()
    events = []
    for slot in times:
        events.append({
            "title": "Buchbar",
            "start": slot["time"],
            "allDay": False
        })
    return jsonify(events)

@app.route("/buchen", methods=["POST"])
def buchen():
    data = request.get_json()
    payload = {
        "appointmentTypeID": APPOINTMENT_TYPE_ID,
        "datetime": data.get("datetime"),
        "firstName": data.get("firstName", "XX"),
        "lastName": data.get("lastName", "XX"),
        "email": data.get("email", "anonym@example.com"),
        "phone": data.get("phone", ""),
        "notes": f"Ort der Sitzung: {data.get('location', 'nicht angegeben')}"
    }

    response = requests.post(
        "https://acuityscheduling.com/api/v1/appointments",
        auth=HTTPBasicAuth(USER_ID, API_KEY),
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": response.json()}), 400
