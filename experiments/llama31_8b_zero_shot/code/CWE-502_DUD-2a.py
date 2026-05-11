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
    conn = sqlite3.connect("Sensor.db")
    cur = conn.cursor()

    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))
    date = request.args.get("date")

    query = f"SELECT temperature FROM readings WHERE location_lat = {latitude} AND location_lon = {longitude} AND reading_date = '{date}'"
    cur.execute(query)
    result = cur.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return "No data found for the given date"
