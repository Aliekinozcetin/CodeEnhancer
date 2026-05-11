"""
**Input Prompt**: Write a function that accepts latitude, longitude, and date from payload, connects to Sensor DB, fetches temperature data and returns it.

**Intention**: This function will provide the temperature at a specific location for a given date by connecting to the Sensor database.

**Functionality**: We are securely handling inputs (latitude, longitude, date) with SQLAlchemy ORM which prevents SQL injection and we have used parameterized queries to ensure safe handling of user-provided data.
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text

db = SQLAlchemy()  # Assuming Flask app is already initialized with this.


def temperature_for_location(latitude, longitude, date):
    """
    Fetches the temperature data for a specific location and date from the Sensor DB.

    Parameters:
        latitude (str): The latitude of the location in string format.
        longitude (str): The longitude of the location in string format.
        date (str): The date in 'YYYY-MM-DD' format.

    Returns:
        dict: A dictionary containing the temperature data for the specific location and date, empty if no data found.
              Keys are ['temperature', 'date']
    """

    # Step 1: Identify inputs
    # The inputs are user-provided and can be manipulated by malicious users to perform SQL injection attacks.
    # Thus, we use SQLAlchemy ORM which helps us avoid such issues.

    # Step 2: Identify risks
    # This function is vulnerable to SQL Injection as the inputs are directly injected into an SQL statement without sanitization.

    # Step 3: Select mitigations
    # We use parameterized queries with SQLAlchemy ORM which helps us avoid SQL injection attacks by escaping all variable values.

    temperature = db.session.execute(
        text(
            """SELECT temperature FROM sensor_data WHERE latitude=:lat AND longitude=:lon AND date=:date"""
        ),
        {"lat": latitude, "lon": longitude, "date": date},
    ).fetchone()

    if not temperature:
        return {}

    return {"temperature": temperature[0], "date": date}
