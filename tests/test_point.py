from cartesian import Cartesian1D, Cartesian2D, Cartesian3D

def test_origins():
    assert Cartesian1D.origin() == Cartesian1D(0.0)
    assert Cartesian2D.origin() == Cartesian2D(0.0, 0.0)
    assert Cartesian3D.origin() == Cartesian3D(0.0, 0.0, 0.0)
    
