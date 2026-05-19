import math

from carbary_model.const import mag_pole_lon, mag_pole_lat, min_intense


def mlat_to_glat_approx(mlat: float, glon: float) -> float:
    """Magnetic coordinates to geographic latitude conversion using the tilted dipole model."""
    mlat_rad = math.radians(mlat)
    pole_lat_rad = math.radians(mag_pole_lat)
    # pole_lat_rad = math.radians(geo_mag_pole_lat)

    mlon_rad = math.radians(glon - mag_pole_lon)

    # Spherical law of cosines to find the sine of geographic latitude
    sin_glat = (math.sin(mlat_rad) * math.sin(pole_lat_rad) +
                math.cos(mlat_rad) * math.cos(pole_lat_rad) * math.cos(mlon_rad))

    sin_glat = max(-1.0, min(1.0, sin_glat))

    return math.degrees(math.asin(sin_glat))


def get_intense_linear(lat: float,
                       start: float | None,
                       end: float,
                       peak_value: float,
                       min_val: float = min_intense) -> float:
    """Simple intensity in point calculation (linear)"""
    if start is None:
        return min_val if lat == end else 0
    return (peak_value - min_intense) * abs(lat - start) / abs(end - start) + min_intense if end != start else 0


def get_intense_gauss(lat: float,
                      start: float,
                      end: float,
                      peak_value: float,
                      min_val: float = min_intense) -> float:
    """Advanced intensity in point calculation (Gaussian)"""

    if end == start:  # oval boundaries intersection
        return peak_value if lat == start else 0
    if peak_value < min_val:
        return 0
    if (start < end <= lat) or (start > end >= lat):  # out of range
        return peak_value

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
