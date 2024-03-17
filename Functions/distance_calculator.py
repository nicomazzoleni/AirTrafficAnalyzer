"""
This module calculates the great circle distance between two points on the earth's surface.

It provides the `haversine` function that implements the Haversine formula, which is an equation giving the shortest distance between two points over the earth's surface.

"""


from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points on the earth.
    
    Parameters
    ----------
    lon1 : float
        Longitude of the first point in decimal degrees.
    lat1 : float
        Latitude of the first point in decimal degrees.
    lon2 : float
        Longitude of the second point in decimal degrees.
    lat2 : float
        Latitude of the second point in decimal degrees.
    
    Returns
    -------
    float
        Great circle distance in kilometers between two points.
    
    Examples
    --------
    >>> haversine(36.12, -86.67, 33.94, -118.40)
    2887.2599506071116
    
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    angle = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    central_angle = 2 * asin(sqrt(angle))
    radius = 6371  # Radius of earth in kilometers.
    return central_angle * radius
