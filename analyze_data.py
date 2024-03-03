from Functions.air_traffic_data import AirTrafficData

# Create an instance of data class
air_traffic_data = AirTrafficData()

# Access the dataframes as attributes
airlines_data = air_traffic_data.airlines_df
airplanes_data = air_traffic_data.airplanes_df
airports_data = air_traffic_data.airports_df
routes_data = air_traffic_data.routes_df

# test usage, printing the first few rows of the airlines dataframe
#print(airlines_data.info())
#print(airplanes_data.info())
print(airports_data.head())
#print(routes_data.info())

#print(airports_data[['IATA'] == 'LAX'])

print(airports_data[airports_data['IATA'] == 'LAX'])
