"""
Module: haversine_distance

This module provides a function to calculate the great circle distance
in kilometers between two points on the Earth, using the Haversine formula.

Functions:
- haversine(lon1, lat1, lon2, lat2): 
    Calculates the great circle distance in kilometers between two points 
    on the Earth, specified in decimal degrees of longitude and latitude.
"""

from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees).
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    angle = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    central_angle = 2 * asin(sqrt(angle))
    radius = 6371  # Radius of earth in kilometers.
    return central_angle * radius
