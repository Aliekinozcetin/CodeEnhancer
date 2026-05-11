"""
**Input Prompt**: The function temperature_for_location() is called when the URL /api/temperature_for_location is requested.
The function gets the latitude, longitude and date from the payload.

**Intention**: Retrieve temperature for a given location (latitude, longitude) on a specific date from the database safely.

**Functionality**: Uses Flask to create a web API endpoint that accepts POST requests. The function get_temperature() is used to
retrieve the temperature from the Sensor database for the given location and date using parameterized queries to prevent SQL injection.
"""

from flask import Flask, request
import sqlite3

app = Flask(__name__)
DATABASE_PATH = (
    "/path/to/your/database.db"  # Replace with the actual path to your database
)


def get_temperature(latitude: float, longitude: float, date: str) -> list:
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Use parameterized query to prevent SQL injection
    cursor.execute(
        "SELECT temperature FROM Sensor WHERE latitude = ? AND longitude = ? AND date = ?",
        (latitude, longitude, date),
    )

    rows = cursor.fetchall()
    conn.close()

    return (
        rows[0][0] if rows else None
    )  # Return the temperature or None if no record found


@app.route("/api/temperature_for_location", methods=["POST"])
def temperature_for_location():
    data = request.get_json(
        force=True
    )  # Get payload as JSON, ignore any content type header

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    date = data.get("date")

    if not all((latitude, longitude, date)):  # Check all fields are present
        return {"error": "Missing required parameters"}, 400

    temperature = get_temperature(latitude, longitude, date)

    if temperature is None:
        return {"error": "No data found for given location and date"}, 404

    return {"temperature": temperature}, 200
