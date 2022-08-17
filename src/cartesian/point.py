"""
This module contains the abstract class CartesianND, as well as the concrete
classes Cartesian1D, Cartesian2D, and Cartesian3D, for expressing points
in continuous cartesian space of their corresponding dimensions.
"""

from __future__ import annotations

from abc import abstractmethod, ABC
from array import array

from typing import TypeVar, Type

T = TypeVar("T", bound="CartesianND")


class CartesianND(ABC):
    """Defines the interface for concrete Cartesian classes."""

    _coords: array[float]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CartesianND):
            return NotImplemented
        return self._coords == other._coords

    def __getitem__(self, i_dim: int) -> float:
        """Return the value of the `dim`th dimension of this point."""
        return self._coords[i_dim]

    def __repr__(self) -> str:
        """Printed representation of the point as a comma-separated tuple."""
        _repr_inner = ", ".join([f"{coord:.6f}" for coord in self._coords])
        return "(" + _repr_inner + ")"

    def coordinates(self) -> array[float]:
        """Direct access to coordinates, mainly for iteration."""
        return self._coords

    @classmethod
    @abstractmethod
    def origin(cls: Type[T]) -> T:
        """Return the origin for a cartesian point in this dimensionality.
        i.e.
            (0.0)      for 1D
            (0.0, 0.0) for 2D, etc.
        """


class Cartesian1D(CartesianND):
    """Represents a point in 1D cartesian space."""

    def __init__(self, x: float) -> None:
        self._coords = array("d", [x])

    @classmethod
    def origin(cls: Type[Cartesian1D]) -> Cartesian1D:
        return Cartesian1D(0.0)


class Cartesian2D(CartesianND):
    """Represents a point in 2D cartesian space."""

    def __init__(self, x: float, y: float) -> None:
        self._coords = array("d", [x, y])

    @classmethod
    def origin(cls: Type[Cartesian2D]) -> Cartesian2D:
        return Cartesian2D(0.0, 0.0)


class Cartesian3D(CartesianND):
    """Represents a point in 3D cartesian space."""

    def __init__(self, x: float, y: float, z: float) -> None:
        self._coords = array("d", [x, y, z])

    @classmethod
    def origin(cls: Type[Cartesian3D]) -> Cartesian3D:
        return Cartesian3D(0.0, 0.0, 0.0)
