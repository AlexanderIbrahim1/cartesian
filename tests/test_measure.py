import math

import pytest

from cartesian import Cartesian1D
from cartesian import Cartesian2D
from cartesian import Cartesian3D
from cartesian import measure
from cartesian import PeriodicBoxSides1D
from cartesian import PeriodicBoxSides2D
from cartesian import PeriodicBoxSides3D


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


@pytest.mark.parametrize(
    "pair_sep, actual_true_pair_sep",
    [
        (0.2, 0.2),
        (0.6, -0.4),
        (1.0, 0.0),
        (1.2, 0.2),
        (1.6, -0.4),
        (2.0, 0.0),
        (2.2, 0.2),
        (0.0, 0.0),
        (-0.2, -0.2),
        (-0.7, 0.3),
        (-1.0, 0.0),
        (-1.3, -0.3),
        (-1.6, 0.4),
        (-2.0, 0.0),
        (-2.2, -0.2),
    ],
)
def test__periodic_modulus_pairdist_sidelength1(pair_sep, actual_true_pair_sep):
    sidelength = 1.0

    expected_true_pair_sep = measure._periodic_modulus_pairdist(pair_sep, sidelength)
    assert (
        expected_true_pair_sep == pytest.approx(actual_true_pair_sep)
        and abs(expected_true_pair_sep) < 0.5 * sidelength
    )


def test_periodic_euclidean_distance():
    box = PeriodicBoxSides1D(1.0)
    point0 = Cartesian1D(0.2)
    point1 = Cartesian1D(0.8)

    expect_distance = 0.4
    expect_distance_sq = expect_distance**2

    actual_distance = measure.periodic_euclidean_distance(point0, point1, box)
    actual_distance_sq = measure.periodic_euclidean_distance_squared(
        point0, point1, box
    )

    # fmt: off
    assert (
        actual_distance == pytest.approx(expect_distance) and
        actual_distance_sq == pytest.approx(expect_distance_sq)
    )
    # fmt: on


def test_periodic_euclidean_distance_wrong_type():
    box = PeriodicBoxSides1D(1.0)
    point_1d = Cartesian1D(0.2)
    point_2d = Cartesian2D(0.2, 0.4)

    actual_distance = measure.periodic_euclidean_distance(point_1d, point_2d, box)
    actual_distance_sq = measure.periodic_euclidean_distance_squared(
        point_1d, point_2d, box
    )

    # fmt: off
    assert (
        actual_distance is NotImplemented and
        actual_distance_sq is NotImplemented
    )
    # fmt: on


def test_periodic_euclidean_distance_wrong_boxdimension():
    box = PeriodicBoxSides2D(1.0, 1.0)
    point0 = Cartesian1D(0.2)
    point1 = Cartesian1D(0.4)

    with pytest.raises(RuntimeError) as exc_info:
        measure.periodic_euclidean_distance(point0, point1, box)

    assert (
        str(exc_info.value)
        == "The points and the box must have the same number of dimensions."
    )


@pytest.mark.parametrize(
    "point, expect_norm",
    [
        (Cartesian1D(0.2), 0.2),
        (Cartesian1D(0.5), 0.5),
        (Cartesian1D(0.7), 0.3),
    ],
)
def test_periodic_euclidean_norm(point, expect_norm):
    box = PeriodicBoxSides1D(1.0)

    expect_norm_sq = expect_norm**2

    actual_norm = measure.periodic_euclidean_norm(point, box)
    actual_norm_sq = measure.periodic_euclidean_norm_squared(point, box)

    # fmt: off
    assert (
        actual_norm == pytest.approx(expect_norm) and
        actual_norm_sq == pytest.approx(expect_norm_sq)
    )
    # fmt: on


def test_periodic_euclidean_norm_wrong_boxdimension():
    box = PeriodicBoxSides3D(1.0, 1.0)
    point = Cartesian1D(0.2)

    with pytest.raises(RuntimeError):
        measure.periodic_euclidean_norm(point, box)

    with pytest.raises(RuntimeError):
        measure.periodic_euclidean_norm_squared(point, box)
