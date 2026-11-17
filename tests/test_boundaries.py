import numpy as np
import pytest

from carbary_model import AuroralBoundary


def test_auroral_boundary_sectors():
    boundary = AuroralBoundary(kp=5.2, ut_hours=12.0)

    assert len(boundary.boundaries) == 360


@pytest.mark.parametrize("shift", [0, 180])
def test_auroral_boundary_points(shift):
    boundary = AuroralBoundary(kp=5.2, ut_hours=0.0)
    assert len(boundary.boundaries) == 360
    res = []
    for k, v in boundary.boundaries.items():
        if v.peak is None:
            res.append(k)
    assert len(res) > 0

    sector = boundary.boundaries[shift]

    if shift:
        assert sector.peak is None
    else:
        assert sector.peak is not None
        assert 0 <= sector.peak.lon <= 359
        assert 0 <= sector.peak.lat <= 90


def test_auroral_boundary_intensity_map():
    boundary = AuroralBoundary(kp=5.2)

    assert isinstance(boundary.intensity_map, np.ndarray)
    assert boundary.intensity_map.ndim == 2
    assert boundary.intensity_map.shape[1] == 3
    assert len(boundary.intensity_map) > 0
