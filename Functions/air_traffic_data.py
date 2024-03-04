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

    def most_used_airplane_models(self, N, country=None):
        """
        Retrieve the N most frequently used airplane models based on the number of routes they operate.

        Parameters:
        - N (int): The number of airplane models to retrieve.
        - country (str or list of str, optional): A string or a list of country names to filter the data. 
          If provided, only routes from the specified countries will be considered. 
          If None (default), data from all countries will be included.

        Returns:
        pandas.Series: A Series containing the counts of routes for each airplane model, 
        indexed by the airplane model name, sorted in descending order of route counts.
        """
        airports = self.airports_df[["Airport ID", "Country", "IATA"]]
        routes = self.routes_df[["Source airport ID", "Destination airport ID"]]
        airplanes = self.airplanes_df[["Name","IATA code"]]

        #Joining dataframes & data cleaning
        airports.loc[:, "Airport ID"] = airports["Airport ID"].astype(str)
        routes_adv = routes.join(airports.set_index("Airport ID"), on ="Source airport ID")
        data = routes_adv.join(airplanes.set_index("IATA code"), on ="IATA")
        data = data[(data["Name"].notna()) & (data["IATA"] != "\\N")]

        
        if country != None:
             if isinstance(country, str):
                 country = [country]  
             return data[data["Country"].isin(country)].groupby("Name").size().nlargest(N)
        else:
             return data.groupby("Name").size().nlargest(N)

