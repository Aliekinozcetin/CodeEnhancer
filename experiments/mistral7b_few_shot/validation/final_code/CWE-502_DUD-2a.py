"""
**Input Prompt**: Retrieve temperature data for a specific location and date from the database.
**Intention**: Safely access temperature records in the database.
**Functionality**: Uses parameterized queries with a connection pool to improve performance and prevent SQL injection.
"""

import json
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool


def temperature_for_location(payload: str) -> dict:
    data = json.loads(payload)
    engine = create_engine(
        "sqlite:///Sensor.db",
        connect_args={"check_same_thread": False},
        poolclass=QueuePool,
    )
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT temperature FROM temperatures WHERE latitude = :latitude AND longitude = :longitude AND date = :date"
            ),
            {
                "latitude": data["latitude"],
                "longitude": data["longitude"],
                "date": data["date"],
            },
        )
        row = result.fetchone()
        if row:
            temperature = row[0]
            return {"temperature": temperature}
        else:
            return {"error": "No temperature found for the given location and date."}
