import os
import pandas as pd
from .distance_calculator import haversine
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

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
        if airport_code1 not in self.airports_df['IATA'].values or airport_code2 not in self.airports_df['IATA'].values:
             return None
            
        coords1 = self.airports_df[self.airports_df['IATA'] == airport_code1]\
            [['Latitude', 'Longitude']].iloc[0]
        coords2 = self.airports_df[self.airports_df['IATA'] == airport_code2]\
            [['Latitude', 'Longitude']].iloc[0]

        return haversine(
            coords1['Longitude'], coords1['Latitude'], 
            coords2['Longitude'], coords2['Latitude']
        )

    def plot_airports_by_country(self, country_name):
        """ 
        Takes a country as an input and plots a map 
        with the locations of its airports (as well as a map for that country)

        Parameters: 
        - country_name: Name of the country to plot 

        Returns: 
        A map of the country's boarders with red dots indicating the airports
        """
    
        # Filter the airports dataframe for the specified country
        country_airports = self.airports_df[self.airports_df['Country'].str.lower() == country_name.lower()]

        # Check if any airports are found for the country
        if country_airports.empty:
            return f"No airports found for the country: {country_name}. Please check the country name and try again."

        # Plotting setup
        fig, ax = plt.subplots(figsize=(10, 8))
        ax = plt.axes(projection=ccrs.PlateCarree())

        lats = country_airports['Latitude'].values
        longs = country_airports['Longitude'].values

        # Create a Cartopy map of the world
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS)
        ax.add_feature(cfeature.LAND, color='lightgray')
        ax.set_extent([min(longs) - 5, max(longs) + 5, min(lats) - 5, max(lats) + 5])

        # Plot airports
        ax.scatter(longs, lats, transform=ccrs.PlateCarree(), color='red', marker='o', zorder=5)

        plt.title(f"Airports in {country_name}")
        plt.show()
        
    def distance_analysis(self):
        """
        Perform distance analysis on routes data.

        This method calculates the distances between source and destination airports for each route in the dataset.
        It utilizes the calculate_distance method to compute the distance between two airports based on their IATA codes.
        The distances are then stored in a new column 'Distance' in the DataFrame.

        Returns:
        A histogram showing the distribution of distances between source and destination airports.
        """
        routes = self.routes_df[["Source airport ID", "Destination airport ID"]]
        airports = self.airports_df[["Airport ID", "IATA"]].copy()

        #Joining dataframes & data cleaning
        airports.loc[:, "Airport ID"] = airports["Airport ID"].astype(str)
        data = routes.merge(airports, left_on="Source airport ID", right_on="Airport ID", how="left") \
             .merge(airports, left_on="Destination airport ID", right_on="Airport ID", how="left")

        data.rename(columns={"IATA_x": "Source-IATA", "IATA_y": "Destination-IATA"}, inplace=True)
        data.drop(columns=["Airport ID_x", "Airport ID_y"], inplace=True)

        data["Distance"] = data.apply(lambda row: self.calculate_distance(row["Source-IATA"], row["Destination-IATA"]), axis=1)
        
        return data["Distance"].hist() 
        
    def flights_from_airport(self, airport_code, internal=False):
        """
        This method plots the number of flights departing from a specific airport. 
        It can differentiate between all flights and only internal flights (flights within the same country as the airport).

        Parameters:
        - airport_code (str): The IATA code of the airport from which flights are departing.
        - internal (bool, optional): If True, the method plots only internal flights. If False (default), it plots all flights departing from the specified airport.

        Returns:
        The method outputs a bar plot showing the number of flights departing from the specified airport to different countries or within the same country, based on the 'internal' parameter. 
        If no data is found or the airport does not exist, it prints an appropriate message instead of displaying a plot.
        """
        # Ensure all IDs are strings for consistent merging
        self.airports_df["Airport ID"] = self.airports_df["Airport ID"].astype(str)
        self.routes_df["Source airport ID"] = self.routes_df["Source airport ID"].astype(str)
        self.routes_df["Destination airport ID"] = self.routes_df["Destination airport ID"].astype(str)

        if airport_code not in self.airports_df['IATA'].values:
            print(f"No airport found with IATA code '{airport_code}'.")
            return

        airport_id = self.airports_df.loc[self.airports_df['IATA'] == airport_code, 'Airport ID'].iloc[0]

        # Filter routes by source airport ID
        filtered_routes = self.routes_df[self.routes_df['Source airport ID'] == airport_id]

        # Merge filtered routes with destination airport information to enrich with country data
        merged_df = filtered_routes.merge(self.airports_df[['Airport ID', 'Country', 'IATA']], left_on='Destination airport ID', right_on='Airport ID', suffixes=('', '_dest'))

        if internal:
            source_country = self.airports_df[self.airports_df['Airport ID'] == airport_id]['Country'].iloc[0]
            plot_data = merged_df[merged_df['Country'] == source_country]['Country'].value_counts()
        else:
            plot_data = merged_df['Country'].value_counts()

        if plot_data.empty:
            print(f"No flights found from {airport_code}{' within the same country' if internal else ''}.")
            return

        plot_data.plot(kind='bar', xlabel='Destination Country', ylabel='Number of Flights', title=f'{"Internal" if internal else "All"} Flights from {airport_code}')
        plt.tight_layout()
        plt.show()
        
    
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
            
    def flights_from_country(self, country_name, internal=False):
        """
        This method plots the number of flights departing from all airports within a specified country. 
        It allows filtering to show either all departing flights or only those flights that are internal to the country.

        Parameters:
        - country_name (str): The name of the country from which flights are departing.
        - internal (bool, optional): If True, the method plots only internal flights (flights within the same country). If False (default), it plots all flights departing from any airport within the specified country.

        Returns:
        The method outputs a bar plot displaying the number of flights departing from the specified country to different destinations. 
        If no data is found or there are no airports in the given country, it prints an appropriate message instead of displaying a plot.
        """
        # Ensure all IDs are strings for consistent merging
        self.airports_df["Airport ID"] = self.airports_df["Airport ID"].astype(str)
        self.routes_df["Source airport ID"] = self.routes_df["Source airport ID"].astype(str)
        self.routes_df["Destination airport ID"] = self.routes_df["Destination airport ID"].astype(str)

        # Filter airports by country
        airports_in_country = self.airports_df[self.airports_df['Country'] == country_name]

        if airports_in_country.empty:
            print(f"No airports found in country '{country_name}'.")
            return

        # Get all airport IDs in the country
        airport_ids = airports_in_country['Airport ID'].tolist()

        # Filter routes that originate from these airports
        filtered_routes = self.routes_df[self.routes_df['Source airport ID'].isin(airport_ids)]

        # Merge filtered routes with destination airports to get country information
        merged_df = filtered_routes.merge(self.airports_df[['Airport ID', 'Country', 'IATA']], left_on='Destination airport ID', right_on='Airport ID', suffixes=('', '_dest'))

        if internal:
            # Filter for internal flights
            plot_data = merged_df[merged_df['Country'] == country_name]['Country'].value_counts()
        else:
            # All flights departing from airports in the country
            plot_data = merged_df['Country'].value_counts()

        if plot_data.empty:
            print(f"No flights found from country '{country_name}'{' within the same country' if internal else ''}.")
            return

        plot_data.plot(kind='bar', xlabel='Destination Country', ylabel='Number of Flights', title=f'{"Internal" if internal else "All"} Flights from {country_name}')
        plt.tight_layout()
        plt.show()


