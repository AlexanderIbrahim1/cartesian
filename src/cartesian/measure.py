"""
This module contains functions to calculate the distance between two instances
of Cartesian1D, Cartesian2D, or Cartesian3D. The distances may be in free space,
or in a periodic box.

There are also functions to return the squared distance between two points.
"""

import math

from .point import CartesianND
from .periodic_box_sides import PeriodicBoxSidesND


def euclidean_distance_squared(point0: CartesianND, point1: CartesianND) -> float:
    """The square of the Euclidean distance between two points in N-dimensional free space."""
    if type(point0) is not type(point1):
        return NotImplemented

    distance_sq = sum(
        [
            (coord0 - coord1) ** 2
            for (coord0, coord1) in zip(point0.coordinates(), point1.coordinates())
        ]
    )

    return distance_sq


def euclidean_distance(point0: CartesianND, point1: CartesianND) -> float:
    """The Euclidean distance between two points in N-dimensional free space."""
    result_distance_sq = euclidean_distance_squared(point0, point1)
    if result_distance_sq is NotImplemented:
        return NotImplemented
    else:
        return math.sqrt(result_distance_sq)


def euclidean_norm_squared(point: CartesianND) -> float:
    """The square of the Euclidean norm of a point, from the origin, in free space."""
    return sum([coord**2 for coord in point.coordinates()])


def euclidean_norm(point: CartesianND) -> float:
    """The Euclidean norm of a point, from the origin, in free space."""
    return math.sqrt(euclidean_norm_squared(point))


def _periodic_modulus_pairdist(pair_separation: float, sidelength: float) -> float:
    """
    Calculate the true distance along a coordinate between two points in a periodic box.
        'pair_separation' is the signed, non-period-corrected separation length
        'sidelength' is the positive along which to judge the true distance

    The output will be between
        '-0.5 * sidelength' and '0.5 * sidelength'
    """
    abs_pair_separation = abs(pair_separation)

    if 2.0 * abs_pair_separation > sidelength:
        sign = math.copysign(1, pair_separation)
        n_shifts = math.ceil((abs_pair_separation / sidelength) - 0.5)

        total_position_shift = sign * n_shifts * sidelength
        true_pair_separation = pair_separation - total_position_shift
        return true_pair_separation
    else:
        return pair_separation


def periodic_euclidean_distance_squared(
    point0: CartesianND, point1: CartesianND, box: PeriodicBoxSidesND
) -> float:
    """
    The square of the Euclidean distance between two points subject to periodic
    boundary conditions imposed by `box`.
    """
    if type(point0) is not type(point1):
        return NotImplemented

    if len(point0._coords) != len(box._coords):
        err_msg = "The points and the box must have the same number of dimensions."
        raise RuntimeError(err_msg)

    distance_sq = 0.0
    for (coord0, coord1, sidelength) in zip(
        point0.coordinates(), point1.coordinates(), box.coordinates()
    ):
        true_pair_separation = _periodic_modulus_pairdist(coord1 - coord0, sidelength)

        distance_sq += true_pair_separation**2

    return distance_sq


def periodic_euclidean_distance(
    point0: CartesianND, point1: CartesianND, box: PeriodicBoxSidesND
) -> float:
    """
    The Euclidean distance between two points subject to periodic boundary conditions
    imposed by `box`.
    """
    result_distance_sq = periodic_euclidean_distance_squared(point0, point1, box)
    if result_distance_sq is NotImplemented:
        return NotImplemented
    else:
        return math.sqrt(result_distance_sq)


def periodic_euclidean_norm_squared(
    point: CartesianND, box: PeriodicBoxSidesND
) -> float:
    """
    The square of the Euclidean norm of a point, subject to periodic boundary conditions
    imposed by `box`.
    """
    if len(point._coords) != len(box._coords):
        err_msg = "The points and the box must have the same number of dimensions."
        raise RuntimeError(err_msg)

    distance_sq = 0.0
    for (coord, sidelength) in zip(point.coordinates(), box.coordinates()):
        true_pair_separation = _periodic_modulus_pairdist(coord, sidelength)

        distance_sq += true_pair_separation**2

    return distance_sq


def periodic_euclidean_norm(point: CartesianND, box: PeriodicBoxSidesND) -> float:
    """The Euclidean norm of a point subject to periodic boundary conditions imposed by `box`."""
    return math.sqrt(periodic_euclidean_norm_squared(point, box))
