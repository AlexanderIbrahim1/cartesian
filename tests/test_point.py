import random

import pytest

from cartesian import Cartesian1D
from cartesian import Cartesian2D
from cartesian import Cartesian3D


def test_origins():
    assert Cartesian1D.origin() == Cartesian1D(0.0)
    assert Cartesian2D.origin() == Cartesian2D(0.0, 0.0)
    assert Cartesian3D.origin() == Cartesian3D(0.0, 0.0, 0.0)


def test_addition_and_subtraction_1D():
    # TODO: replace this boilerplate with a fixture
    n_samples = 10
    lower_bound = -10.0
    upper_bound = 10.0

    for i in range(n_samples):
        x0 = random.uniform(lower_bound, upper_bound)
        x1 = random.uniform(lower_bound, upper_bound)

        p0 = Cartesian1D(x0)
        p1 = Cartesian1D(x1)

        p_add01 = p0 + p1
        assert p_add01[0] == pytest.approx(x0 + x1)

        p_sub01 = p0 - p1
        assert p_sub01[0] == pytest.approx(x0 - x1)


def test_addition_and_subtraction_2D():
    # TODO: replace this boilerplate with a fixture
    n_samples = 10
    lower_bound = -10.0
    upper_bound = 10.0

    for i in range(n_samples):
        x0 = random.uniform(lower_bound, upper_bound)
        x1 = random.uniform(lower_bound, upper_bound)
        y0 = random.uniform(lower_bound, upper_bound)
        y1 = random.uniform(lower_bound, upper_bound)

        p0 = Cartesian2D(x0, y0)
        p1 = Cartesian2D(x1, y1)

        p_add01 = p0 + p1
        assert p_add01[0] == pytest.approx(x0 + x1)
        assert p_add01[1] == pytest.approx(y0 + y1)

        p_sub01 = p0 - p1
        assert p_sub01[0] == pytest.approx(x0 - x1)
        assert p_sub01[1] == pytest.approx(y0 - y1)


def test_addition_and_subtraction_3D():
    # TODO: replace this boilerplate with a fixture
    n_samples = 10
    lower_bound = -10.0
    upper_bound = 10.0

    for i in range(n_samples):
        x0 = random.uniform(lower_bound, upper_bound)
        x1 = random.uniform(lower_bound, upper_bound)
        y0 = random.uniform(lower_bound, upper_bound)
        y1 = random.uniform(lower_bound, upper_bound)
        z0 = random.uniform(lower_bound, upper_bound)
        z1 = random.uniform(lower_bound, upper_bound)

        p0 = Cartesian3D(x0, y0, z0)
        p1 = Cartesian3D(x1, y1, z1)

        p_add01 = p0 + p1
        assert p_add01[0] == pytest.approx(x0 + x1)
        assert p_add01[1] == pytest.approx(y0 + y1)
        assert p_add01[2] == pytest.approx(z0 + z1)

        p_sub01 = p0 - p1
        assert p_sub01[0] == pytest.approx(x0 - x1)
        assert p_sub01[1] == pytest.approx(y0 - y1)
        assert p_sub01[2] == pytest.approx(z0 - z1)


def test_multiplication_1D2D3D():
    # TODO: replace this boilerplate with a fixture
    n_samples = 10
    lower_bound = -10.0
    upper_bound = 10.0

    for i in range(n_samples):
        scale = random.uniform(lower_bound, upper_bound)
        x0 = random.uniform(lower_bound, upper_bound)
        y0 = random.uniform(lower_bound, upper_bound)
        z0 = random.uniform(lower_bound, upper_bound)

        p0_1d = Cartesian1D(x0)
        p0_2d = Cartesian2D(x0, y0)
        p0_3d = Cartesian3D(x0, y0, z0)

        p0_1d_left = scale * p0_1d
        p0_1d_right = p0_1d * scale
        assert p0_1d_left[0] == pytest.approx(scale * x0)
        assert p0_1d_right[0] == pytest.approx(scale * x0)

        p0_2d_left = scale * p0_2d
        p0_2d_right = p0_2d * scale
        assert p0_2d_left[0] == pytest.approx(scale * x0)
        assert p0_2d_right[0] == pytest.approx(scale * x0)
        assert p0_2d_left[1] == pytest.approx(scale * y0)
        assert p0_2d_right[1] == pytest.approx(scale * y0)

        p0_3d_left = scale * p0_3d
        p0_3d_right = p0_3d * scale
        assert p0_3d_left[0] == pytest.approx(scale * x0)
        assert p0_3d_right[0] == pytest.approx(scale * x0)
        assert p0_3d_left[1] == pytest.approx(scale * y0)
        assert p0_3d_right[1] == pytest.approx(scale * y0)
        assert p0_3d_left[2] == pytest.approx(scale * z0)
        assert p0_3d_right[2] == pytest.approx(scale * z0)
