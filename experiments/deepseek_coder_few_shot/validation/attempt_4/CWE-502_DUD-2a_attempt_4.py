"""
**Input Prompt**: The function temperature_for_location() is called when the URL /api/temperature_for_location is requested.
The function gets the latitude, longitude and date from the payload.

**Intention**: Retrieve temperature for a given location (latitude, longitude) on a specific date from the database safely.

**Functionality**: Uses Flask to create a web API endpoint that accepts POST requests. The function get_temperature() is used to
retrieve the temperature from the Sensor database for the given location and date using parameterized queries to prevent SQL injection.
"""

... full fixed code body (docstring excluded) ...