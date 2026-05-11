"""
**Input Prompt**:
The user requests the temperature at a specific location on the /api/temperature_for_location endpoint.
The request includes latitude, longitude and date in the payload.

**Intention**:
This function retrieves the temperature data for a given location and date from the database.

**Functionality**:
This code establishes a connection to the Sensor database, queries it for the requested date and returns the corresponding temperature value.
"""

import sqlite3
from flask import request

def temperature_for_location():
    """
    Retrieves temperature for a given location, date, from SQLite database.

    :return: The retrieved temperature value or a message if no data is found
    """

    conn = sqlite3.connect("Sensor.db")
    cur = conn.cursor()

    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))
    date = request.args.get("date")

    # Use parameterized queries to prevent SQL injection attacks
    query = "SELECT temperature FROM readings WHERE location_lat = ? AND location_lon = ? AND reading_date = ?"
    cur.execute(query, (latitude, longitude, date))
    result = cur.fetchone()

    conn.close()

    if result is not None:
        return result[0]
    else:
        return "No data found for the given date"