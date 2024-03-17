"""
This module contains functionality for testing the calculation of distances
between airports using the AirTrafficData class from the Functions package.
"""

# test_distance.py
import pytest
from Functions.air_traffic_data import AirTrafficData

@pytest.mark.parametrize("airport_code1, airport_code2, expected_distance", [
    ('LAX', 'JFK', 3983),
    ('CDG', 'NRT', 9711),
    ('SYD', 'LHR', 17020),
])
def test_calculate_distance(airport_code1, airport_code2, expected_distance):
    """
    Test the AirTrafficData class's ability to calculate distances.

    This test takes two airport codes and an expected distance, calculates the
    actual distance using AirTrafficData, and asserts that the calculated
    distance is within 100 kilometers of the expected distance.

    Args:
        airport_code1 (str): IATA code for the first airport.
        airport_code2 (str): IATA code for the second airport.
        expected_distance (int): Expected distance in kilometers between the two airports.
    """
    air_traffic = AirTrafficData()
    calculated_distance = air_traffic.calculate_distance(airport_code1, airport_code2)
    assert abs(calculated_distance - expected_distance) < 100, (
        f"Distance between {airport_code1} and {airport_code2} "
        f"({calculated_distance} km) differs from expected ({expected_distance} km)"
    )
