from __future__ import annotations

from abc import abstractmethod, ABC
from array import array


class PeriodicBoxSidesND(ABC):
    """Describe the side lengths of a box in N-dimensional cartesian space."""

    _coords: array[float]

    @abstractmethod
    def __init__(self, coords: array[float]) -> None:
        self._coords = coords

        if any([coord <= 0.0 for coord in self._coords]):
            err_msg = (
                "All side lengths in the periodic box must be positive.\n"
                f"Found: {self.__repr__()}"
            )
            raise ValueError(err_msg)

    def coordinates(self) -> array[float]:
        """Direct access to coordinates, mainly for iteration."""
        return self._coords

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PeriodicBoxSidesND):
            return NotImplemented
        return self._coords == other._coords

    def __getitem__(self, i_dim: int) -> float:
        """Return the value of the `dim`th dimension of this box."""
        return self._coords[i_dim]

    def __repr__(self) -> str:
        """Printed representation of the point as a comma-separated tuple."""
        _repr_inner = ", ".join([f"{coord:.6f}" for coord in self._coords])
        return "PeriodicBoxSides(" + _repr_inner + ")"


class PeriodicBoxSides1D(PeriodicBoxSidesND):
    """Represents the sides of a periodic box in 1D cartesian space."""

    def __init__(self, xlen: float) -> None:
        super().__init__(array("d", [xlen]))


class PeriodicBoxSides2D(PeriodicBoxSidesND):
    """Represents the sides of a periodic box in 2D cartesian space."""

    def __init__(self, xlen: float, ylen: float) -> None:
        super().__init__(array("d", [xlen, ylen]))


class PeriodicBoxSides3D(PeriodicBoxSidesND):
    """Represents the sides of a periodic box in 3D cartesian space."""

    def __init__(self, xlen: float, ylen: float, zlen: float) -> None:
        super().__init__(array("d", [xlen, ylen, zlen]))
