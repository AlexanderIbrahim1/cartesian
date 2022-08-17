"""
This module contains the abstract class CartesianND, as well as the concrete
classes Cartesian1D, Cartesian2D, and Cartesian3D, for expressing points
in continuous cartesian space of their corresponding dimensions.
"""

from __future__ import annotations

from abc import abstractmethod, ABC
from array import array

from typing import Any
from typing import Type
from typing import TypeVar

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

    @abstractmethod
    def __add__(self, other: Any) -> Any:
        """Element-wise addition of two points in cartesian space."""

    @abstractmethod
    def __sub__(self, other: Any) -> Any:
        """Element-wise subtraction of two points in cartesian space."""

    @abstractmethod
    def __mul__(self, other: float) -> Any:
        """Element-wise multiplication of the point in cartesian space by a number."""

    @abstractmethod
    def __rmul__(self, other: float) -> Any:
        """Element-wise multiplication of the point in cartesian space by a number."""

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

    def __add__(self, other: Any) -> Cartesian1D:
        if not isinstance(other, Cartesian1D):
            return NotImplemented
        return Cartesian1D(self._coords[0] + other._coords[0])

    def __sub__(self, other: Any) -> Cartesian1D:
        if not isinstance(other, Cartesian1D):
            return NotImplemented
        return Cartesian1D(self._coords[0] - other._coords[0])

    def __mul__(self, other: Any) -> Cartesian1D:
        if not isinstance(other, float):
            return NotImplemented
        return Cartesian1D(other * self._coords[0])

    def __rmul__(self, other: Any) -> Cartesian1D:
        return self.__mul__(other)

    @classmethod
    def origin(cls: Type[Cartesian1D]) -> Cartesian1D:
        return Cartesian1D(0.0)


class Cartesian2D(CartesianND):
    """Represents a point in 2D cartesian space."""

    def __init__(self, x: float, y: float) -> None:
        self._coords = array("d", [x, y])

    def __add__(self, other: Any) -> Cartesian2D:
        if not isinstance(other, Cartesian2D):
            return NotImplemented
        return Cartesian2D(
            self._coords[0] + other._coords[0],
            self._coords[1] + other._coords[1],  # noqa; want to both on separate lines
        )

    def __sub__(self, other: Any) -> Cartesian2D:
        if not isinstance(other, Cartesian2D):
            return NotImplemented
        return Cartesian2D(
            self._coords[0] - other._coords[0],
            self._coords[1] - other._coords[1],  # noqa; want to both on separate lines
        )

    def __mul__(self, other: Any) -> Cartesian2D:
        if not isinstance(other, float):
            return NotImplemented
        return Cartesian2D(other * self._coords[0], other * self._coords[1])

    def __rmul__(self, other: Any) -> Cartesian2D:
        return self.__mul__(other)

    @classmethod
    def origin(cls: Type[Cartesian2D]) -> Cartesian2D:
        return Cartesian2D(0.0, 0.0)


class Cartesian3D(CartesianND):
    """Represents a point in 3D cartesian space."""

    def __init__(self, x: float, y: float, z: float) -> None:
        self._coords = array("d", [x, y, z])

    def __add__(self, other: Any) -> Cartesian3D:
        if not isinstance(other, Cartesian3D):
            return NotImplemented
        return Cartesian3D(
            self._coords[0] + other._coords[0],
            self._coords[1] + other._coords[1],
            self._coords[2] + other._coords[2],
        )

    def __sub__(self, other: Any) -> Cartesian3D:
        if not isinstance(other, Cartesian3D):
            return NotImplemented
        return Cartesian3D(
            self._coords[0] - other._coords[0],
            self._coords[1] - other._coords[1],
            self._coords[2] - other._coords[2],
        )

    def __mul__(self, other: Any) -> Cartesian3D:
        if not isinstance(other, float):
            return NotImplemented
        return Cartesian3D(
            other * self._coords[0],
            other * self._coords[1],
            other * self._coords[2],
        )

    def __rmul__(self, other: Any) -> Cartesian3D:
        return self.__mul__(other)

    @classmethod
    def origin(cls: Type[Cartesian3D]) -> Cartesian3D:
        return Cartesian3D(0.0, 0.0, 0.0)
