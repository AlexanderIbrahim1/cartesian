"""
This module contains functions to perform common operations on CartesianND points,
such as:
    - taking linear combinations of several points
    - ...
"""

import array
import math
from itertools import combinations
from typing import Sequence

from cartesian import Cartesian2D
from cartesian import Cartesian3D
from cartesian import CartesianND
from cartesian.measure import euclidean_distance
from cartesian.measure import periodic_euclidean_distance
from cartesian.periodic_box_sides import PeriodicBoxSidesND


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


def cross_product(pa: Cartesian3D, pb: Cartesian3D) -> Cartesian3D:
    if pa.n_dims != 3 or pb.n_dims != 3:
        raise ValueError(
            "The cross product is only defined between two 3-dimensional vectors.\n"
            f"pa.n_dims = {pa.n_dims}\n"
            f"pb.n_dims = {pb.n_dims}"
        )

    coords_a = pa.coordinates
    coords_b = pb.coordinates

    result0 = coords_a[1] * coords_b[2] - coords_a[2] * coords_b[1]
    result1 = coords_a[2] * coords_b[0] - coords_a[0] * coords_b[2]
    result2 = coords_a[0] * coords_b[1] - coords_a[1] * coords_b[0]

    return Cartesian3D(result0, result1, result2)


def cross_product_result(pa: Cartesian2D, pb: Cartesian2D) -> float:
    if pa.n_dims != 2 or pb.n_dims != 2:
        raise ValueError(
            "The cross product result is only defined between two 2-dimensional vectors.\n"
            f"pa.n_dims = {pa.n_dims}\n"
            f"pb.n_dims = {pb.n_dims}"
        )

    coords_a = pa.coordinates
    coords_b = pb.coordinates

    return coords_a[0] * coords_b[1] - coords_a[1] * coords_b[0]


def linear_combination(
    points: Sequence[CartesianND], coeffs: Sequence[float]
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


def relative_pair_distances(points: Sequence[CartesianND]) -> list[float]:
    """
    Calculate the distances between all pairs of points in free, non-periodic space.

    If fewer than two points are present, the returned list is empty.
    """
    return [euclidean_distance(p0, p1) for (p0, p1) in combinations(points, 2)]


def periodic_relative_pair_distances(
    points: Sequence[CartesianND], box: PeriodicBoxSidesND
) -> list[float]:
    """
    Calculate the distances between all pairs of points in periodic space.

    If fewer than two points are present, the returned list is empty.
    """
    return [
        periodic_euclidean_distance(p0, p1, box) for (p0, p1) in combinations(points, 2)
    ]


# TODO: come up with a better description
def shift_points_together(
    points: Sequence[CartesianND],
    box: PeriodicBoxSidesND,
    err_if_too_far: bool = False,
) -> Sequence[CartesianND]:
    """
    Shift the positions of the points such that they end up close to each other.
    """
    # trivial case; don't have to shift points together, if there are only 0 or 1
    if len(points) <= 1:
        return points

    # pick a point and translate the entire system so that point is at the origin
    point0 = points[0]

    # shift all points to be inside the box around 'p0'
    shifted_points = [CartesianND.origin(point0.n_dims)]
    shifted_points.extend(
        [
            _translate_point_near_origin(p - point0, box, err_if_too_far)
            for p in points[1:]
        ]
    )

    return shifted_points


def _number_of_box_shifts(pair_separation: float, sidelength: float) -> int:
    """
    Along a certain coordinate, calculate the numebr of times that a point would
    have to make jumps of length 'sidelength' to end up within a distance 'sidelength'
    of another point.
    """
    abs_pair_separation = abs(pair_separation)

    if 2.0 * abs_pair_separation > sidelength:
        sign = int(math.copysign(1, pair_separation))
        n_shifts = math.ceil((abs_pair_separation / sidelength) - 0.5)
        return sign * n_shifts
    else:
        return 0


def _translate_point_near_origin(
    point: CartesianND,
    box: PeriodicBoxSidesND,
    err_if_too_far: bool = False,
) -> CartesianND:
    """
    Translate 'point' in space such that it lies within the sides of 'box' around
    the origin.

    'err_if_too_far'
        - raise an exception if more than one shift has to be done to move the point
          near the origin
    """

    new_coords = array.array("d", [0] * point.n_dims)
    for i_coord, (coord, sidelen) in enumerate(zip(point.coordinates, box.coordinates)):
        n_shifts = _number_of_box_shifts(coord, sidelen)
        if err_if_too_far and abs(n_shifts) > 1:
            raise RuntimeError(
                "The point is too far from the origin relative to the size of the box.\n"
                "More than a single shift had to be performed.\n"
                f"point: {point}\n"
                f"box: {box}\n"
                f"number of shifts along coordinate {i_coord}: {n_shifts}\n"
            )

        new_coords[i_coord] = coord - n_shifts * sidelen

    return CartesianND(new_coords)
