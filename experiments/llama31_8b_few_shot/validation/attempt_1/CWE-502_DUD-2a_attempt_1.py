"""
**Input Prompt**: Return the temperature for a given location.
**Intention**: Retrieve temperature data from the database safely.
**Functionality**: Uses parameterized queries and secure database connection.
"""

import sqlite3
from flask import request, jsonify


def temperature_for_location():
    # Get payload from request
    payload = request.get_json()

    if not payload:
        return jsonify({"error": "Missing required data"}), 400

    latitude = payload["latitude"]
    longitude = payload["longitude"]
    date = payload["date"]

    # Connect to database securely
    conn = sqlite3.connect("Sensor.db")
    cursor = conn.cursor()

    # Use parameterized query to prevent SQL injection
    cursor.execute(
        "SELECT temperature FROM readings WHERE location = ? AND date = ?",
        (f"{latitude},{longitude}", date),
    )

    result = cursor.fetchone()

    if not result:
        return jsonify({"error": "No data found for the given location and date"}), 404

    conn.close()

    # Return temperature
    return jsonify(result[0])
