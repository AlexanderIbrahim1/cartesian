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
) -> Sequence[CartesianND]:
    assert len(points) == len(coeffs) > 0

    sum_point = coeffs[0] * points[0]
    for (point, coeff) in zip(points[1:], coeffs[1:]):
        sum_point = sum_point + coeff * point

    return sum_point
