"""
**Input Prompt**:
The `temperature_for_location` function retrieves temperature data from the Sensor database based on provided latitude, longitude, and date.

**Intention**:
To securely query the Sensor database for temperature readings corresponding to a specified location and date.

**Functionality**:
This code implements input validation, parameterized queries to prevent SQL injection, and error handling to ensure robustness.
"""

def temperature_for_location(request):
    # Step 1 — Identify inputs:
    # The function receives data from the request payload (latitude, longitude, date) and the database connection.
    try:
        # Step 2 — Identify risks:
        # Potential risks include SQL injection and insecure direct object reference (IDOR).
        latitude = float(request.args.get("latitude"))  # Validate as float
        longitude = float(request.args.get("longitude"))  # Validate as float
        date_str = request.args.get("date")  # Get date from request

        # Step 3 — Select mitigations:
        # Use parameterized queries to prevent SQL injection and validate inputs.
        import sqlite3

        conn = sqlite3.connect("Sensor.db")
        cursor = conn.cursor()

        query = (
            "SELECT temperature FROM Sensor WHERE latitude=? AND longitude=? AND date=?"
        )
        cursor.execute(query, (latitude, longitude, date_str))  # Parameterized query

        result = cursor.fetchone()  # Retrieve the first matching row
        if result:
            temperature = result[0]  # Extract and return the temperature value
            return temperature
        else:
            # Step 4 — Write the code:
            # Handle cases where no match is found in the database.
            return None
    except ValueError as e:
        # Input validation failed; handle the exception securely.
        print(f"Invalid input: {e}")
    finally:
        # Ensure the database connection is properly closed, regardless of execution flow.
        if "conn" in locals():
            conn.close()
