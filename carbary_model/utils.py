"""
Lib utils

GeoMagnetic pole location
----------------------
North GeoMagnetic Pole position calculation bases on The US/UK World Magnetic Model for 2025-2030:
https://www.ncei.noaa.gov/products/world-magnetic-model/wmm-coefficients

The solar declination
----------------------
# https://gml.noaa.gov/grad/solcalc/solareqns.PDF
# https://www.pveducation.org/pvcdrom/properties-of-sunlight/declination-angle
"""
import math
from datetime import datetime, UTC
import functools
import pathlib

import numpy as np
from scipy.ndimage import gaussian_filter, gaussian_filter1d

from carbary_model.exceptions import InvalidMLTError, InvalidKpError, UnexpectedError
from carbary_model.const import MIN_INTENSE, MAG_POLE_LOCATION, MAG_POLE_LOCATION_DEFAULT, KP_MAX, KP_MIN, \
    WMM_COEF_DATA_SOURCE, WGS84_FLAT_COEF, SUN_DECLINATION, GRAD_IN_SECTOR
from carbary_model.types import AuroraBoundarySector, Point


def magnetic_to_geographic(mlat: float, mlon: float, pole: Point) -> Point:
    """Magnetic to geographic coordinates conversion using the tilted dipole model"""

    mlat_rad = math.radians(mlat)
    mlon_rad = math.radians(mlon)
    pole_lat_rad = math.radians(pole.lat)

    # Spherical law of cosines to find the sine of geographic latitude
    sin_glat = (math.sin(mlat_rad) * math.sin(pole_lat_rad) +
                math.cos(mlat_rad) * math.cos(pole_lat_rad) * math.cos(mlon_rad))
    sin_glat = max(-1.0, min(1.0, sin_glat))
    glat = math.degrees(math.asin(sin_glat))

    # Spherical law of cosines to find the sine of geographic longitude
    # Delta = (glon - pole.lon)
    y = math.sin(mlon_rad) * math.cos(mlat_rad)
    x = (math.sin(mlat_rad) - math.sin(pole_lat_rad) * sin_glat) / math.cos(pole_lat_rad)

    delta = math.degrees(math.atan2(y, x))
    glon = (pole.lon + delta) % 360.0

    return Point(lat=glat, lon=glon)


def glon_to_mlon_approx(glon: float, pole: Point) -> float:
    """Geographic to Magnetic longitude conversion using the tilted dipole model."""

    pole_lat_rad = math.radians(pole.lat)
    pole_lon_rad = math.radians(pole.lon)
    glon_rad = math.radians(glon)

    # Spherical angle for geographic latitude
    y = math.sin(glon_rad - pole_lon_rad)
    x = math.cos(glon_rad - pole_lon_rad) * math.sin(pole_lat_rad)

    return math.degrees(math.atan2(y, x)) % 360.0


def mlat_mlon_to_glat_approx(mlat: float, mlon: float, pole: Point) -> float:
    """Magnetic coordinates to geographic latitude conversion using the tilted dipole model."""

    mlat_rad = math.radians(mlat)
    pole_lat_rad = math.radians(pole.lat)
    mlon_rad = math.radians(mlon)

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


@functools.lru_cache(maxsize=1)
def get_wmm_coeffs():
    """Returns g10, g11, h11 from WMM.COF"""

    file_name = pathlib.Path(__file__).parent.joinpath(WMM_COEF_DATA_SOURCE)
    error_msg = f"{WMM_COEF_DATA_SOURCE} Processing Error"
    with open(file_name) as fh:
            lines = fh.read().splitlines()

    try:
        result = {"base_year": float(lines[0].split()[0])}
    except ValueError:
        raise UnexpectedError(error_msg)
    for line in lines[1:3]:
        parts = line.split()
        if len(parts) >= 6:
            try:
               if int(parts[0]) == 1:
                    m = int(parts[1])
                    if m == 0:
                        result["g10"] = float(parts[2])
                        result["g10_ext"] = float(parts[4])
                    elif m == 1:
                        result["g11"] = float(parts[2])
                        result["h11"] = float(parts[3])
                        result["g11_ext"] = float(parts[4])
                        result["h11_ext"] = float(parts[5])
            except ValueError:
                raise UnexpectedError(error_msg)
    return result


def get_decimal_year(date: datetime) -> float:
    """Returns decimal year value
        :param date: datetime (with UTC)
        :returns: decimal year value (float)
    """

    start_year = datetime(date.year, 1, 1, tzinfo=UTC)
    next_year = datetime(date.year + 1, 1, 1, tzinfo=UTC)
    seconds_in_year = (next_year - start_year).total_seconds()
    seconds = (date - start_year).total_seconds()

    return date.year + (seconds / seconds_in_year)


def get_geomag_pole(date: float | None = None) -> Point:
    """Coordinates of North Geomagnetic Pole"""

    date = date or get_decimal_year(datetime.now(UTC))
    wmm_coeffs = get_wmm_coeffs()
    delta = date - wmm_coeffs.get("base_year")

    # Extrapolation
    g10 = wmm_coeffs["g10"] + wmm_coeffs["g10_ext"] * delta
    g11 = wmm_coeffs["g11"] + wmm_coeffs["g11_ext"] * delta
    h11 = wmm_coeffs["h11"] + wmm_coeffs["h11_ext"] * delta

    lon_rad = math.atan2(h11, g11)
    lon = math.degrees(lon_rad)
    lon = (lon + 180.0) % 360.0

    h0 = math.sqrt(g10**2 + g11**2 + h11**2)
    cos_colatitude = -g10 / h0
    colatitude_rad = math.acos(cos_colatitude)
    lat_geocentric = math.degrees(math.pi / 2 - colatitude_rad)

    # Geocentric latitude to WGS84 latitude conversion
    # First eccentricity squared of the WGS84 ellipsoid
    e2 = 2 * WGS84_FLAT_COEF - WGS84_FLAT_COEF ** 2
    lat_rad = math.atan(math.tan(math.radians(lat_geocentric)) / (1 - e2))

    return Point(lat=math.degrees(lat_rad), lon=lon)


def get_sun_declination(day_num: int | None = None) -> float:
    """Returns sun declination value for given day of year by Cooper formula
    https://www.pveducation.org/pvcdrom/properties-of-sunlight/declination-angle
    :param day_num: day number (1-365)
    :returns: declination value in degrees (float)
    """

    day_num = day_num or int(datetime.now(UTC).strftime('%j'))
    return -SUN_DECLINATION * math.cos(math.radians((360 / 365) * (day_num + 10)))

def get_sun_mlon(shift: int,
                 ut_hours: float,
                 size: int,
                 pole: Point) -> float:
    """Returns sun magnetic longitude"""

    sun_glat = get_sun_declination()
    sun_glon = (shift - ut_hours * GRAD_IN_SECTOR) % size

    sun_lat_rad = math.radians(sun_glat)
    sun_lon_rad = math.radians(sun_glon)
    pole_lat_rad = math.radians(pole.lat)
    pole_lon_rad = math.radians(pole.lon)

    y_sun = math.cos(sun_lat_rad) * math.sin(sun_lon_rad - pole_lon_rad)
    x_sun = (math.cos(sun_lat_rad) * math.cos(sun_lon_rad - pole_lon_rad) * math.sin(pole_lat_rad)
             - math.sin(sun_lat_rad) * math.cos(pole_lat_rad))

    return math.degrees(math.atan2(y_sun, x_sun)) % size


def get_smooth_gauss(data: np.ndarray,
                     x: int,
                     y: int,
                     mode_2d: bool,
                     sigma_x: float = 2.0,
                     sigma_y: float = 1.0) -> np.ndarray:
    """Returns grid of values smoothed by gaussian_filter"""

    grid = np.zeros((x, y))

    for row in data:
        lon_idx = int(round(row[0])) % x
        lat_idx = int(round(row[1] + (y // 2))) % y
        intense = row[2]
        # max intense
        grid[lon_idx, lat_idx] = max(grid[lon_idx, lat_idx], intense)

    # apply gaussian filter, mode=['wrap', 'constant'] for 2D, 'wrap' for another case
    # TODO: simplify
    smoothed_grid = gaussian_filter(grid, sigma=[sigma_x, sigma_y], mode=['wrap', 'constant']) if mode_2d \
        else gaussian_filter1d(grid, sigma=sigma_x, axis=0, mode='wrap')

    result = []
    lons, lats = np.where(smoothed_grid > MIN_INTENSE)

    for lon, lat in zip(lons, lats):
        # step 0.5 for original grid imitation
        result.append([float(lon), float(lat - (y // 2)), smoothed_grid[lon, lat]])
        result.append([float(lon), float(lat - (y // 2)) + 0.5, smoothed_grid[lon, lat]])

    return np.array(result)