import pytest

from cartesian import Cartesian2D
from cartesian import Cartesian3D
from cartesian import measure
from cartesian import operations
from cartesian import PeriodicBoxSides2D


class TestLinearCombination:

    default_points = [
        Cartesian3D(1.0, 2.0, 3.0),
        Cartesian3D(4.0, 5.0, 6.0),
        Cartesian3D(7.0, 8.0, 9.0),
    ]
    default_coeffs = [1.0, 2.0, 3.0]

    def test_linear_combination(self):
        points = self.default_points
        coeffs = self.default_coeffs

        expect_point = Cartesian3D(
            1.0 * 1.0 + 2.0 * 4.0 + 3.0 * 7.0,
            1.0 * 2.0 + 2.0 * 5.0 + 3.0 * 8.0,
            1.0 * 3.0 + 2.0 * 6.0 + 3.0 * 9.0,
        )
        actual_point = operations.linear_combination(points, coeffs)

        assert actual_point == expect_point

    def test_incorrect_lengths(self):
        points = self.default_points
        coeffs = [1.0, 2.0]

        with pytest.raises(AssertionError):
            operations.linear_combination(points, coeffs)

    def test_empty(self):
        points = []
        coeffs = []

        with pytest.raises(AssertionError):
            operations.linear_combination(points, coeffs)


class TestCentroid:
    def test_centroid(self):
        points = [
            Cartesian2D(-1.0, -1.0),
            Cartesian2D(-1.0, 1.0),
            Cartesian2D(1.0, -1.0),
            Cartesian2D(1.0, 1.0),
        ]

        centroid_point = operations.centroid(points)
        assert measure.approx_eq(centroid_point, Cartesian2D.origin())

    def test_centroid_brute_force(self):
        points = [
            Cartesian3D(1.0, 2.0, 3.0),
            Cartesian3D(4.0, 5.0, 6.0),
            Cartesian3D(7.0, 8.0, 9.0),
        ]

        expect_point = (points[0] + points[1] + points[2]) / len(points)

        centroid_point = operations.centroid(points)
        assert measure.approx_eq(centroid_point, expect_point)


class Test_dot_product:
    def test_basic_functionality(self):
        p0 = Cartesian2D(1.0, 1.0)
        p1 = Cartesian2D(2.0, 0.0)

        assert operations.dot_product(p0, p1) == pytest.approx(2.0)

    def test_raises_different_sizes(self):
        p_dim2 = Cartesian2D(1.0, 2.0)
        p_dim3 = Cartesian3D(3.0, 4.0, 5.0)

        with pytest.raises(ValueError) as exc_info:
            operations.dot_product(p_dim2, p_dim3)

        assert (
            "Two points must have the same dimensionality to calculate their dot product.\n"
            f"p0.n_dims = 2\n"
            f"p1.n_dims = 3" in str(exc_info.value)
        )


class Test_shift_points_together:
    def test_basic_functionality(self):
        points = [
            Cartesian2D(0.1, 0.1),
            Cartesian2D(0.5, 0.1),
            Cartesian2D(0.5, 0.9),
        ]
        box = PeriodicBoxSides2D(1.0, 1.0)

        shifted_points = operations.shift_points_together(points, box)

        assert measure.approx_eq(shifted_points[0], Cartesian2D(0.0, 0.0))
        assert measure.approx_eq(shifted_points[1], Cartesian2D(0.4, 0.0))
        assert measure.approx_eq(shifted_points[2], Cartesian2D(0.4, -0.2))

    def test_0_points(self):
        box = PeriodicBoxSides2D(1.0, 1.0)
        points = []

        assert operations.shift_points_together(points, box) == []

    def test_1_points(self):
        box = PeriodicBoxSides2D(1.0, 1.0)
        points = [Cartesian3D(1.0, 2.0, 3.0)]

        shifted_points = operations.shift_points_together(points, box)
        assert points == shifted_points

    def test_raises_too_far(self):
        points = [
            Cartesian2D(0.1, 0.1),
            Cartesian2D(0.5, 0.1),
            Cartesian2D(0.5, 1.9),  # y-position is too far away
        ]
        box = PeriodicBoxSides2D(1.0, 1.0)

        with pytest.raises(RuntimeError) as exc_info:
            operations.shift_points_together(points, box, err_if_too_far=True)

        assert (
            "The point is too far from the origin relative to the size of the box.\n"
            "More than a single shift had to be performed.\n" in str(exc_info.value)
        )


class Test_relative_pair_distances:
    def test_basic_functionality(self):
        points = [
            Cartesian2D(0.0, 0.0),
            Cartesian2D(0.0, 1.0),
            Cartesian2D(0.0, 2.0),
        ]

        pair_distances = operations.relative_pair_distances(points)
        assert pair_distances[0] == pytest.approx(1.0)
        assert pair_distances[1] == pytest.approx(2.0)
        assert pair_distances[2] == pytest.approx(1.0)

    def test_one_point(self):
        points = [Cartesian2D(0.0, 0.0)]

        pair_distances = operations.relative_pair_distances(points)
        assert pair_distances == []

    def test_no_points(self):
        assert operations.relative_pair_distances([]) == []
