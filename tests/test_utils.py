import pytest

from carbary_model.const import MIN_INTENSE
from carbary_model.utils import get_intense_gauss, get_intense_linear


def test_get_intense_linear_at_peak_0():
    intensity = get_intense_linear(lat=70.0, start=None, end=70.0, peak_value=30.0)
    assert intensity == pytest.approx(MIN_INTENSE)


def test_get_intense_linear_at_peak_1():
    intensity = get_intense_linear(lat=70.0, start=60.0, end=60.0, peak_value=30.0)
    assert intensity == pytest.approx(0)

def test_get_intense_linear_at_peak_2():
    intensity = get_intense_linear(lat=70.0, start=60.0, end=70.0, peak_value=30.0)
    assert intensity == pytest.approx(30.0)


def test_get_intense_linear_midpoint():
    intensity = get_intense_linear(lat=65.0, start=60.0, end=70.0, peak_value=30.0)
    assert intensity == pytest.approx(17.0)


def test_get_intense_gauss_at_peak():
    intensity = get_intense_gauss(lat=70.0, start=60.0, end=70.0, peak_value=30.0)
    assert intensity == pytest.approx(30.0)


def test_get_intense_gauss_at_boundary():
    intensity = get_intense_gauss(lat=70.0, start=60.0, end=70.0, peak_value=30.0)
    assert intensity == pytest.approx(30.0)


def test_get_intense_gauss_at_midpoint():
    peak_val = 30.0
    intensity = get_intense_gauss(lat=65.0, start=60.0, end=70.0, peak_value=peak_val)
    assert intensity < peak_val
    assert intensity > MIN_INTENSE


def test_get_intense_gauss_out_of_range():
    intensity = get_intense_gauss(lat=80.0, start=60.0, end=70.0, peak_value=30.0)
    assert intensity == pytest.approx(30.0)


def test_gauss_intersecting_boundaries():
    lat_val = 70.0
    peak_val = 30.0

    res_match = get_intense_gauss(lat=70.0, start=lat_val, end=lat_val, peak_value=peak_val)
    assert res_match == pytest.approx(30.0)

    res_miss = get_intense_gauss(lat=71.0, start=lat_val, end=lat_val, peak_value=peak_val)
    assert res_miss == 0


def test_gauss_collapsed_boundaries_outside():
    res = get_intense_gauss(lat=70.0, start=60.0, end=60.0, peak_value=30.0)
    assert res == 0

