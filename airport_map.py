import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from Functions.air_traffic_data import AirTrafficData

 
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


# Create an instance of the AirTrafficData class
air_traffic = AirTrafficData()

# Call the plot_airports_by_country method
air_traffic.plot_airports_by_country('USA')