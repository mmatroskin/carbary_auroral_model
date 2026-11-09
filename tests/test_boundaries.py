import numpy as np

from carbary_model import AuroralBoundary
from carbary_model.types import PoleType


def test_auroral_boundary_sectors():
    boundary = AuroralBoundary(kp=5.2, ut_hours=12.0)

    assert len(boundary.boundaries) == 360


def test_auroral_boundary_points():
    boundary = AuroralBoundary(kp=5.2, ut_hours=0.0, strict_mode=True)
    assert len(boundary.boundaries) == 360
    res = []
    for k, v in boundary.boundaries.items():
        if v.peak is None:
            res.append(k)
    assert len(res) > 0

    initial = 0
    shift = 270

    sector = boundary.boundaries[initial]

    assert sector.peak is not None
    assert 0 <= sector.peak.lon <= 359
    assert 0 <= sector.peak.lat <= 90

    sector = boundary.boundaries[shift]

    assert sector.peak is None


def test_auroral_boundary_intensity_map():
    boundary = AuroralBoundary(kp=5.2)

    assert isinstance(boundary.intensity_map, np.ndarray)
    assert boundary.intensity_map.ndim == 2
    assert boundary.intensity_map.shape[1] == 3
    assert len(boundary.intensity_map) > 0
