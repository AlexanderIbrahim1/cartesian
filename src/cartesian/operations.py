"""
This module contains functions to perform common operations on CartesianND points,
such as:
    - taking linear combinations of several points
    - ...
"""
from array import array
from typing import Sequence

from cartesian import CartesianND


def linear_combination(
    points: Sequence[CartesianND], coeffs: Sequence[CartesianND]
) -> CartesianND:
    assert len(points) == len(coeffs) > 0

    sum_point = coeffs[0] * points[0]
    for (point, coeff) in zip(points[1:], coeffs[1:]):
        sum_point = sum_point + coeff * point

    return sum_point


def centroid(points: Sequence[CartesianND]) -> CartesianND:
    """
    Calculate the centroid position of a sequence of points.
    This is like the centre of mass, but we give each position the same weight.
    """
    n_points = len(points)
    assert n_points >= 1
    
    sum_point = points[0]
    for point in points[1:]:
        sum_point += point
    
    return sum_point / n_points
