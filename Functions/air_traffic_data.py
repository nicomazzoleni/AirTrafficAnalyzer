import os
import pandas as pd
from .distance_calculator import haversine


class AirTrafficData:
    """Initializes the class by loading datasets into pandas DataFrames."""

    def __init__(self):
        self.airlines_df = self.load_csv('downloads/airlines.csv')
        self.airplanes_df = self.load_csv('downloads/airplanes.csv')
        self.airports_df = self.load_csv('downloads/airports.csv')
        self.routes_df = self.load_csv('downloads/routes.csv')

    def load_csv(self, file_path):
        """
        Loads a CSV file into a pandas DataFrame.

        Parameters:
        - file_path: The path to the CSV file to load.

        Returns:
        A pandas DataFrame containing the data from the CSV file.
        """
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            raise FileNotFoundError(f"The file {file_path} does not exist.")

    def calculate_distance(self, airport_code1, airport_code2):
        """
        Calculates the distance between two airports.

        Parameters:
        - airport_code1: The IATA code of the first airport.
        - airport_code2: The IATA code of the second airport.

        Returns:
        The distance in kilometers between the two airports.
        """
        coords1 = self.airports_df[self.airports_df['IATA'] == airport_code1]\
            [['Latitude', 'Longitude']].iloc[0]
        coords2 = self.airports_df[self.airports_df['IATA'] == airport_code2]\
            [['Latitude', 'Longitude']].iloc[0]

        return haversine(
            coords1['Longitude'], coords1['Latitude'], 
            coords2['Longitude'], coords2['Latitude']
        )

