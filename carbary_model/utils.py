import math
from datetime import datetime, UTC

from carbary_model.exceptions import InvalidMLTError, InvalidKpError
from carbary_model.const import MIN_INTENSE, MAG_POLE_LOCATION, MAG_POLE_LOCATION_DEFAULT, KP_MAX, KP_MIN
from carbary_model.types import Point


def mlat_to_glat_approx(mlat: float, glon: float, pole: Point) -> float:
    """Magnetic coordinates to geographic latitude conversion using the tilted dipole model."""
    mlat_rad = math.radians(mlat)
    pole_lat_rad = math.radians(pole.lat)
    mlon_rad = math.radians(glon - pole.lon)

    # Spherical law of cosines to find the sine of geographic latitude
    sin_glat = (math.sin(mlat_rad) * math.sin(pole_lat_rad) +
                math.cos(mlat_rad) * math.cos(pole_lat_rad) * math.cos(mlon_rad))

    sin_glat = max(-1.0, min(1.0, sin_glat))

    return math.degrees(math.asin(sin_glat))


def get_intense_linear(lat: float,
                       start: float | None,
                       end: float,
                       peak_value: float,
                       min_val: float = MIN_INTENSE) -> float:
    """Simple intensity in point calculation (linear)"""
    if start is None:
        return min_val if lat == end else 0
    return (peak_value - MIN_INTENSE) * abs(lat - start) / abs(end - start) + MIN_INTENSE if end != start else 0


def get_intense_gauss(lat: float,
                      start: float,
                      end: float,
                      peak_value: float,
                      min_val: float = MIN_INTENSE) -> float:
    """Advanced intensity in point calculation (Gaussian)"""

    if end == start:  # oval boundaries intersection
        return peak_value if lat == start else 0
    if peak_value < min_val:
        return 0
    if (start < end <= lat) or (start > end >= lat):  # out of range
        return peak_value

    # NOTES:
    # Gaussian distribution equation:
    # f(x) = mult * exp(-((x - mu)^2) / (2 * sigma^2))
    # mult = (1 / (sigma * sqrt(2 * pi)))
    # mult = peak_value
    # mu - expected value (peak coordinate) -> mu == end
    # sigma - standard deviation
    # sigma = = sqrt(sum((x(i) - mu^2) / N)
    # in this case ( f(x) >= min_val) we can get sigma due Gaussian equation (f(x) and x at boundaries are known):
    # sigma = (x_max - x_min) / sqrt(2 * ln(f_max / f_min))

    sigma = abs(end - start) / math.sqrt(2 * math.log(peak_value / min_val))

    # peak_value (mu) is always in the end (mu = end)
    val = peak_value * math.exp(-((lat - end) ** 2) / (2 * (sigma ** 2)))

    return val


def validate_kp(kp: float) -> None:
    """Validates kp value"""
    if not (KP_MIN <= kp <= KP_MAX):
        raise InvalidKpError(f"Kp must be in [{KP_MIN}, {KP_MAX}], got {kp}")


def validate_mlt(mlt: float) -> None:
    """Validates mlt value"""
    if not (0.0 <= mlt < 24.0):
        raise InvalidMLTError(f"MLT must be in [0, 24), got {mlt}")


def get_mag_pole() -> Point:
    """Coordinates of North Magnetic Pole"""
    point = MAG_POLE_LOCATION.get(datetime.now(UTC).year) or MAG_POLE_LOCATION_DEFAULT
    return Point(**point)
