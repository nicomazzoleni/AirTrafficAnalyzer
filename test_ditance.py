from Functions.air_traffic_data import AirTrafficData

# Create an instance of the AirTrafficData class
air_traffic = AirTrafficData()

# Define a function to manually test the calculate_distance method
def test_calculate_distance(airport_code1, airport_code2, expected_distance):
    calculated_distance = air_traffic.calculate_distance(airport_code1, airport_code2)
    print(f"Distance between {airport_code1} and {airport_code2}: {calculated_distance} km")

    # Check if the calculated distance is within an acceptable range of the expected distance
    if abs(calculated_distance - expected_distance) < 100:  # 100 km tolerance
        print("Success: The calculated distance is within the expected range.")
    else:
        print("Error: The calculated distance is not within the expected range.")

# Known distances for testing
test_calculate_distance('LAX', 'JFK', 3983)  
test_calculate_distance('CDG', 'NRT', 9711)  
test_calculate_distance('SYD', 'LHR', 17020)
