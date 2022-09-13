import pytest

from cartesian import Cartesian3D
from cartesian import operations


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
            1.0 * 3.0 + 2.0 * 6.0 + 3.0 * 9.0
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
