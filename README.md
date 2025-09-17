# AirTrafficAnalyzer

*A Python-based toolkit for analyzing and visualizing global air traffic data — flight routes, airport distributions, aircraft usage, and environmental impact.*

---

## About

**AirTrafficAnalyzer** is an open-source Python module that simplifies the exploration of air traffic data. It provides a user-friendly interface for loading aviation datasets (airlines, airplanes, airports, and routes) into pandas DataFrames and offers tools for analysis and visualization.

Whether you're an aviation enthusiast, data analyst, or researcher, this module helps you uncover insights into flight patterns, aircraft usage, and the environmental impact of air travel.

### Key Features

* **Data Analysis:** Compute flight distances, explore airport- and country-level statistics, and analyze aircraft model usage.
* **Visualization:** Generate geospatial plots of airports and flight routes with customizable filters (e.g., by country or distance).
* **Environmental Impact:** Estimate CO₂ emission reductions by transitioning short-haul flights to lower-emission alternatives (e.g., rail).
* **Flexibility:** Customize analyses with optional parameters for targeted insights.

Developed by a team of data science enthusiasts, AirTrafficAnalyzer is intuitive, modular, and extensible for integration into larger projects.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/nicomazzoleni/AirTrafficAnalyzer.git
cd AirTrafficAnalyzer

# Install dependencies
pip install -r requirements.txt
```

**Required libraries:** `pandas`, `matplotlib`, `folium`, `geopy` (see `requirements.txt` for details).

### Data

Download or provide aviation datasets (e.g., from OpenFlights) and place them in the `data/` folder:

```
data/
├── airlines.csv
├── airplanes.csv
├── airports.csv
└── routes.csv
```

---

## Usage

### Instantiate the data loader

```python
from air_traffic_data import AirTrafficData

# Load datasets automatically
atd = AirTrafficData()
```

### Analyze flight routes

```python
# Get routes between 1000 and 5000 km
distance_stats = atd.analyze_distances(min_distance=1000, max_distance=5000)
print(distance_stats)
```

### Visualize airports

```python
# Plot airports in a specific country
atd.plot_airports_by_country(country="USA", output_file="usa_airports.html")
```

### Explore aircraft models

```python
# Get top 10 most-used aircraft models
top_models = atd.get_aircraft_models(top_n=10)
print(top_models)
```

### Estimate environmental impact

```python
# Calculate CO₂ savings by replacing short-haul flights (<500 km) with rail
emissions_savings = atd.estimate_emission_reductions(distance_threshold=500)
print(emissions_savings)
```

See the `examples/` folder for detailed Jupyter notebooks demonstrating each feature.

---

## Features

* **Data Loading:** Automatically loads aviation datasets into pandas DataFrames.
* **Route Analysis:** Compute and filter flight distances (e.g., short-haul vs. long-haul).
* **Geospatial Visualization:** Plot airports and routes on interactive maps using Folium.
* **Flight Statistics:** Analyze departure frequencies by airport or country.
* **Environmental Insights:** Estimate CO₂ reductions for short-haul flights compared to rail transport.
* **Customizable Queries:** Filter data by country, distance, or other parameters.

---

## Project Structure

```
AirTrafficAnalyzer/
├── data/                     # Aviation datasets (airlines, airports, etc.)
├── examples/                 # Jupyter notebooks with usage demos
├── src/                      # Source code
│   └── air_traffic_data.py   # Main AirTrafficData class
├── tests/                    # Unit tests for the module
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---


## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## Contact

For questions or feedback, reach out via GitHub Issues or email the maintainers:

* Nicolò Mazzoleni — 59935@novasbe.pt  
* Fabrizio Rigodanzo — 60526@novasbe.pt
* Robert Münchau — 61682@novasbe.pt
* Julia Antonioli — 60178@novasbe.pt

---

## Acknowledgments

* Inspired by public aviation datasets like **OpenFlights**.  
* Built with open-source libraries: **pandas**, **Matplotlib**, **Folium**, and more.  
* Thanks to the data science community for feedback and inspiration.
