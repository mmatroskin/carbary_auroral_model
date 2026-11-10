import numpy as np
import pytest

from carbary_model import AuroralBoundary


@pytest.mark.parametrize("strict_mode", [True, False])
def test_auroral_boundary_sectors(strict_mode):
    boundary = AuroralBoundary(kp=5.2, ut_hours=12.0, strict_mode=strict_mode)

    assert len(boundary.boundaries) == 360


@pytest.mark.parametrize("strict_mode", [True, False])
def test_auroral_boundary_points(strict_mode):
    boundary = AuroralBoundary(kp=5.2, ut_hours=0.0, strict_mode=strict_mode)
    assert len(boundary.boundaries) == 360
    res = []
    for k, v in boundary.boundaries.items():
        if v.peak is None:
            res.append(k)
    assert len(res) > 0

    initial = 0
    shift = 180

    sector = boundary.boundaries[initial]

    assert sector.peak is not None
    assert 0 <= sector.peak.lon <= 359
    assert 0 <= sector.peak.lat <= 90

    sector = boundary.boundaries[shift]

    assert sector.peak is None


@pytest.mark.parametrize("strict_mode", [True, False])
def test_auroral_boundary_intensity_map(strict_mode):
    boundary = AuroralBoundary(kp=5.2, strict_mode=strict_mode)

    assert isinstance(boundary.intensity_map, np.ndarray)
    assert boundary.intensity_map.ndim == 2
    assert boundary.intensity_map.shape[1] == 3
    assert len(boundary.intensity_map) > 0
