import pytest

from cartesian import PeriodicBoxSides1D
from cartesian import PeriodicBoxSides2D
from cartesian import PeriodicBoxSides3D


def test_periodic_box_sides_1d():
    box = PeriodicBoxSides1D(1.5)
    assert box[0] == pytest.approx(1.5)


def test_periodic_box_sides_2d():
    box = PeriodicBoxSides2D(3.0, 2.0)
    # fmt: off
    assert (
        box[0] == pytest.approx(3.0)
        and box[1] == pytest.approx(2.0)
    )
    # fmt: on


def test_periodic_box_sides_3d():
    box = PeriodicBoxSides3D(0.5, 2.2, 3.3)
    assert (
        box[0] == pytest.approx(0.5)
        and box[1] == pytest.approx(2.2)
        and box[2] == pytest.approx(3.3)
    )


@pytest.mark.parametrize(
    "box1, box2",
    [
        (PeriodicBoxSides1D(2.0), PeriodicBoxSides1D(2.0)),
        (PeriodicBoxSides2D(1.0, 3.0), PeriodicBoxSides2D(1.0, 3.0)),
        (PeriodicBoxSides3D(4.1, 5.2, 6.3), PeriodicBoxSides3D(4.1, 5.2, 6.3)),
    ],
)
def test_periodic_box_eq(box1, box2):
    assert box1 == box2


@pytest.mark.parametrize(
    "box1, box2",
    [
        (PeriodicBoxSides1D(2.0), PeriodicBoxSides1D(2.2)),
        (PeriodicBoxSides2D(1.0, 3.0), PeriodicBoxSides2D(1.1, 3.0)),
        (PeriodicBoxSides3D(4.1, 5.2, 6.3), PeriodicBoxSides3D(4.1, 5.201, 6.301)),
        (PeriodicBoxSides3D(1.0, 2.0, 3.0), "This is not a box"),
    ],
)
def test_periodic_box_not_eq(box1, box2):
    assert box1 != box2


def test_periodic_box_repr():
    box = PeriodicBoxSides2D(1.5, 3.3)
    assert repr(box) == "PeriodicBoxSides(1.500000, 3.300000)"


def test_periodic_box_coordinates():
    box = PeriodicBoxSides2D(1.5, 3.3)
    coord_itr = iter(box.coordinates)
    # fmt: off
    assert (
        next(coord_itr) == pytest.approx(1.5)
        and next(coord_itr) == pytest.approx(3.3)
    )
    # fmt: on


@pytest.mark.parametrize("sidelengths", [(1.0, -1.0), (0.0, 1.0), (3.0, 0.0)])
def test_periodic_box_invalid(sidelengths):
    with pytest.raises(ValueError):
        PeriodicBoxSides2D(*sidelengths)
