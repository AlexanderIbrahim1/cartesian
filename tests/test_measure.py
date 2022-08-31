import math

import pytest

from cartesian import Cartesian1D
from cartesian import Cartesian2D
from cartesian import Cartesian3D
from cartesian import measure


@pytest.mark.parametrize(
    "point0, point1, distance",
    [
        (Cartesian1D(-1.0), Cartesian1D(1.0), 2.0),
        (Cartesian2D(-1.0, -1.0), Cartesian2D(1.0, 1.0), (8.0) ** 0.5),
        (Cartesian3D(-1.0, -1.0, -1.0), Cartesian3D(1.0, 1.0, 1.0), (12.0) ** 0.5),
    ],
)
def test_euclidean_distance(point0, point1, distance):
    assert measure.euclidean_distance(point0, point1) == pytest.approx(distance)


@pytest.mark.parametrize(
    "distance_func",
    [
        measure.euclidean_distance,
        measure.euclidean_distance_squared,
    ],
)
def test_euclidean_distance_notimpl(distance_func):
    p_dim1 = Cartesian1D(2.0)
    p_dim2 = Cartesian2D(3.0, -1.0)

    assert distance_func(p_dim1, p_dim2) == NotImplemented


def test_euclidean_distance_squared():
    p0 = Cartesian2D(0.0, 0.0)
    p1 = Cartesian2D(3.0, 4.0)

    dist_numeric = math.sqrt(3.0**2 + 4.0**2)
    dist_euclid = measure.euclidean_distance(p0, p1)
    dist_euclid_sq = measure.euclidean_distance_squared(p0, p1)

    assert (
        dist_euclid_sq
        == pytest.approx(dist_euclid**2)
        == pytest.approx(dist_numeric**2)
    )


@pytest.mark.parametrize(
    "point, norm",
    [
        (Cartesian1D(1.0), 1.0),
        (Cartesian2D(1.0, 1.0), (2.0) ** 0.5),
        (Cartesian3D(1.0, 1.0, 1.0), (3.0) ** 0.5),
    ],
)
def test_euclidean_norm(point, norm):
    assert measure.euclidean_norm(point) == pytest.approx(norm)


def test_euclidean_norm_squared():
    point = Cartesian2D(3.0, 4.0)

    norm_numeric = math.sqrt(3.0**2 + 4.0**2)
    norm_euclid = measure.euclidean_norm(point)
    norm_euclid_sq = measure.euclidean_norm_squared(point)

    assert (
        norm_euclid_sq
        == pytest.approx(norm_euclid**2)
        == pytest.approx(norm_numeric**2)
    )
