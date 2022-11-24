"""
This module contains functions to perform common operations on CartesianND points,
such as:
    - taking linear combinations of several points
    - ...
"""
from typing import Sequence

from cartesian import CartesianND


def dot_product(p0: CartesianND, p1: CartesianND) -> float:
    """The N-dimensional Cartesian inner product between these two points."""
    if p0.n_dims != p1.n_dims:
        raise ValueError(
            "Two points must have the same dimensionality to calculate their dot product.\n"
            f"p0.n_dims = {p0.n_dims}\n"
            f"p1.n_dims = {p1.n_dims}"
        )

    return sum(
        [elem0 * elem1 for (elem0, elem1) in zip(p0.coordinates, p1.coordinates)]
    )


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
