"""
**Input Prompt**: The function `temperature_for_location()` receives latitude, longitude and date as input from a request payload.

**Intention**: This code is used to fetch temperature data for a given location on a specific date from the database.

**Functionality**: The function connects to the 'Sensor' database, fetches the temperature data for the provided latitude, longitude and date, and returns it.
"""

import psycopg2
from flask import Flask, request
from psycopg2 import sql

app = Flask(__name__)

@app.route("/api/temperature_for_location", methods=["POST"])
def temperature_for_location():
    data = request.get_json()  # Fetch the JSON payload from the request

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    date = data.get("date")

    conn = psycopg2.connect(
        database="Sensor",
        user="postgres",
        password="password",
        host="localhost",
        port="5432",
    )  # Connect to the database

    cur = conn.cursor()  # Create a cursor object

    query_string = sql.SQL("SELECT temperature FROM weather_data WHERE latitude = %s AND longitude = %s AND date = %s")  # Prepare SQL query string

    cur.execute(query_string, (latitude, longitude, date))  # Execute the prepared query

    result = cur.fetchone()  # Fetch one record from the executed query

    conn.close()  # Close the database connection

    if result:
        return {"temperature": result[0]}  # If a temperature exists, return it in JSON format
    else:
        return {"error": "No data found for provided latitude, longitude and date."}  # Else, return an error message