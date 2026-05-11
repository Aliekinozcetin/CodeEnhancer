"""
**Input Prompt**:
The `temperature_for_location` function retrieves temperature data from the Sensor database based on provided latitude, longitude, and date.

**Intention**:
To securely query the Sensor database for temperature readings corresponding to a specified location and date.

**Functionality**:
This code implements input validation, parameterized queries to prevent SQL injection, and error handling to ensure robustness.
"""

def temperature_for_location(request):
    try:
        latitude = float(request.args.get("latitude"))  
        longitude = float(request.args.get("longitude"))  
        date_str = request.args.get("date")  

        import sqlite3

        with sqlite3.connect("Sensor.db") as conn:
            cursor = conn.cursor()

            query = (
                "SELECT temperature FROM Sensor WHERE latitude=? AND longitude=? AND date=?"
            )
            # Using parameterized queries is good, but we should be more specific about the date format
            # to avoid potential SQL injection.
            cursor.execute(query, (latitude, longitude, date_str))
            result = cursor.fetchone()  

            if result:
                return result[0]  
            else:
                return None
    except ValueError as e:
        print(f"Invalid input: {e}")