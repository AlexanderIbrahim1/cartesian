"""
This module contains the abstract class CartesianND, as well as the concrete
classes Cartesian1D, Cartesian2D, and Cartesian3D, for expressing points
in continuous cartesian space of their corresponding dimensions.
"""

from __future__ import annotations

from abc import ABC
from array import array


class CartesianND(ABC):
    """Defines the interface for concrete Cartesian classes."""

    _coords: array[float]

    def __init__(self, coords: array[float]) -> None:
        self._coords = coords

    @property
    def coordinates(self) -> array[float]:
        """Direct access to coordinates, mainly for iteration."""
        return self._coords

    @property
    def n_dims(self) -> int:
        return len(self._coords)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CartesianND):
            return NotImplemented
        return self._coords == other.coordinates

    def __hash__(self):
        return hash(tuple(self._coords))

    def __getitem__(self, i_dim: int) -> float:
        """Return the value of the `dim`th dimension of this point."""
        return self._coords[i_dim]

    def __repr__(self) -> str:
        """Printed representation of the point as a comma-separated tuple."""
        _repr_inner = ", ".join([f"{coord:.6f}" for coord in self._coords])
        return "(" + _repr_inner + ")"

    def __add__(self, other: CartesianND) -> CartesianND:
        """Element-wise addition of two points in cartesian space."""
        if self.n_dims != other.n_dims:
            return NotImplemented

        new_coords = [
            co_self + co_other
            for (co_self, co_other) in zip(self._coords, other.coordinates)
        ]

        return CartesianND(array("d", new_coords))

    def __sub__(self, other: CartesianND) -> CartesianND:
        """Element-wise subtraction of two points in cartesian space."""
        if self.n_dims != other.n_dims:
            return NotImplemented

        new_coords = [
            co_self - co_other
            for (co_self, co_other) in zip(self._coords, other.coordinates)
        ]

        return CartesianND(array("d", new_coords))

    def __mul__(self, other: float) -> CartesianND:
        """Scalar multiplication of the point in cartesian space by a number."""
        new_coords = [other * coord for coord in self._coords]

        return CartesianND(array("d", new_coords))

    def __rmul__(self, other: float) -> CartesianND:
        """Scalar multiplication of the point in cartesian space by a number."""
        return self.__mul__(other)

    def __floordiv__(self, other: float) -> CartesianND:
        if other == 0.0:
            raise ZeroDivisionError("cannot divide Cartesian1D coordinates by 0")
        else:
            new_coords = [coord // other for coord in self._coords]
            return CartesianND(array("d", new_coords))

    def __truediv__(self, other: float) -> CartesianND:
        if other == 0.0:
            raise ZeroDivisionError("cannot divide Cartesian1D coordinates by 0")
        else:
            new_coords = [coord / other for coord in self._coords]
            return CartesianND(array("d", new_coords))

    @classmethod
    def origin(self, size: int) -> CartesianND:
        if size <= 0:
            raise ValueError("CartesianND point must have a `size` of 1 or greater.")
        return CartesianND(array("d", [0.0] * size))


class Cartesian1D(CartesianND):
    """Represents a point in 1D cartesian space."""

    def __init__(self, x: float) -> None:
        self._coords = array("d", [x])

    @classmethod
    def origin(self) -> Cartesian1D:
        return Cartesian1D(0.0)


class Cartesian2D(CartesianND):
    """Represents a point in 2D cartesian space."""

    def __init__(self, x: float, y: float) -> None:
        self._coords = array("d", [x, y])

    @classmethod
    def origin(self) -> Cartesian2D:
        return Cartesian2D(0.0, 0.0)


class Cartesian3D(CartesianND):
    """Represents a point in 3D cartesian space."""

    def __init__(self, x: float, y: float, z: float) -> None:
        self._coords = array("d", [x, y, z])

    @classmethod
    def origin(self) -> Cartesian3D:
        return Cartesian3D(0.0, 0.0, 0.0)
