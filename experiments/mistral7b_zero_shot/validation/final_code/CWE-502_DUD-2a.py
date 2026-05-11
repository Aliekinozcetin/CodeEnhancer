"""
**Input Prompt**: The function `temperature_for_location()` is called when the URL `/api/temperature_for_location` is requested.
                  The function gets the latitude, longitude and date from the payload.
                  The function connects to the database `Sensor` and gets the temperature for the given date.
                  The function returns the temperature.

**Intention**: To retrieve temperature data for a specific location and date from the Sensor database.

**Functionality**: The code establishes a connection with the Sensor database, fetches temperature data based on the provided latitude, longitude, and date, and returns the temperature.
"""

import psycopg2
import paramiko
from sqlalchemy import create_engine, text

def load_secret(filename):
    client = paramiko.SSHClient()
    known_hosts = paramiko.util.load_host_keys('~/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Change policy to AutoAddPolicy
    client.connect('secrets-server', knownhosts=known_hosts)
    stdin, stdout, stderr = client.get_transport().open_session()
    stdin.send(f'cat {filename}\n')
    password = stdout.read().decode().strip()
    client.close()
    return password

def temperature_for_location(payload):
    lat, lon, date = payload["latitude"], payload["longitude"], payload["date"]
    password = load_secret('db_password.txt')

    engine = create_engine('postgresql://username:{0}@localhost/Sensor'.format(password)) # Escape the password with an escape character or use a config file
    connection = engine.connect()
    query = text("SELECT temperature FROM temperatures WHERE latitude=:lat AND longitude=:lon AND date=:date")
    result = connection.execute(query, lat=lat, lon=lon, date=date).fetchone()[0]
    connection.close()

    return result