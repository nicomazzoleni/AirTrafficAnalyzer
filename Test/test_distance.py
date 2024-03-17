"""
This module contains functionality for testing the calculation of distances
between airports using the AirTrafficData class from the Functions package.
"""

import os
import sys
# This will get the directory of the current file (__file__), go one directory up
# (the root of your project), and append it to sys.path
# pylint: disable=wrong-import-position
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Functions.air_traffic_data import AirTrafficData
# pylint: enable=wrong-import-position

# Create an instance of the AirTrafficData class
air_traffic = AirTrafficData()

def test_calculate_distance(airport_code1, airport_code2, expected_distance):
    """
    Test the calculate_distance method for a pair of airports.

    Parameters:
    airport_code1 (str): IATA code of the first airport.
    airport_code2 (str): IATA code of the second airport.
    expected_distance (int): The expected distance in kilometers.

    Prints a success message if the calculated distance is within the
    acceptable range of the expected distance, otherwise prints an error.
    """
    calculated_distance = air_traffic.calculate_distance(airport_code1, airport_code2)
    print(f"Distance between {airport_code1} and {airport_code2}: "
          f"{calculated_distance} km")

    # Check if the calculated distance is within an acceptable range
    if abs(calculated_distance - expected_distance) < 100:  # 100 km tolerance
        print("Success: The calculated distance is within the expected range.")
    else:
        print("Error: The calculated distance is not within the expected range.")

# Known distances for testing
test_calculate_distance('LAX', 'JFK', 3983)
test_calculate_distance('CDG', 'NRT', 9711)
test_calculate_distance('SYD', 'LHR', 17020)
