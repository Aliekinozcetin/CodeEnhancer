"""
**Input Prompt**: The function `temperature_for_location()` is called when the URL `/api/temperature_for_location` is requested.
                  The function gets the latitude, longitude and date from the payload.
                  The function connects to the database `Sensor` and gets the temperature for the given date.
                  The function returns the temperature.

**Intention**: To retrieve temperature data for a specific location and date from the Sensor database.

**Functionality**: The code establishes a connection with the Sensor database, fetches temperature data based on the provided latitude, longitude, and date, and returns the temperature.
"""

import psycopg2


def temperature_for_location(payload):
    lat, lon, date = payload["latitude"], payload["longitude"], payload["date"]

    connection = psycopg2.connect(dbname="Sensor", user="username", password="password")
    cursor = connection.cursor()

    query = f"SELECT temperature FROM temperatures WHERE latitude={lat} AND longitude={lon} AND date='{date}'"
    cursor.execute(query)

    result = cursor.fetchone()[0]
    cursor.close()
    connection.close()

    return result
