import pytest

from carbary_model.carbary_model import CarbaryAuroralModel
from carbary_model.exceptions import InvalidKpError, InvalidMLTError


@pytest.fixture
def model():
    return CarbaryAuroralModel()


def test_invalid_kp_low(model):
    with pytest.raises(InvalidKpError):
        model.get_boundaries(kp=-0.1, mlt=0.0)


def test_invalid_kp_high(model):
    with pytest.raises(InvalidKpError):
        model.get_boundaries(kp=9.1, mlt=0.0)


def test_invalid_mlt(model):
    with pytest.raises(InvalidMLTError):
        model.get_boundaries(kp=3.0, mlt=24.0)


def test_none_value_mlt(model):
    """The boundary should not exist"""
    data = model.get_boundaries(kp=2.0, mlt=12.0)

    assert data.eq_boundary is None
    assert data.po_boundary is None


def test_valid_boundaries(model):
    """The boundary should exist"""
    data = model.get_boundaries(kp=3.0, mlt=0.0)

    assert data.eq_boundary is not None
    assert data.peak is not None
    assert data.po_boundary is not None
    assert data.peak_intensity is not None


def test_known_point_kp0_mlt0(model):
    """At Kp=0, MLT=0 the boundary should be C0."""
    data = model.get_boundaries(kp=0.0, mlt=0.0)

    assert data.eq_boundary == pytest.approx(67.22, abs=0.01)
    assert data.peak == pytest.approx(69.96, abs=0.01)
    assert data.po_boundary == pytest.approx(71.83, abs=0.01)
    assert data.peak_intensity == pytest.approx(3.71, abs=0.01)


def test_get_boundaries_missing_sectors(model):
    """The boundary should not exist"""
    data = model.get_boundaries(kp=5.0, mlt=10)

    assert data.eq_boundary is None
    assert data.peak is None
    assert data.po_boundary is None
    assert data.peak_intensity is None


def test_peak_intensity_is_non_negative(model):
    """The intensity should be non-negative"""
    intensity = model.get_peak_intensity(kp=9.0, mlt=19)

    assert intensity is not None
    assert intensity >= 0.0

