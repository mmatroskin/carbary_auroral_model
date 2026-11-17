"""
Constant values

Magnetic pole location
----------------------
North Magnetic Pole position (WMM2025):
https://www.ncei.noaa.gov/products/wandering-geomagnetic-poles

The magnetic poles or dip poles are computed from all the Gauss coefficients using an iterative method.
Magnetic poles derived in this fashion are geographically closer to the experimentally observed poles.
Based on the current WMM, the 2025 location of the North Magnetic Pole is 85.762°N and 139.298°E and
the South Magnetic Pole is 63.851°S and 135.078°E.
https://www.ncei.noaa.gov/sites/default/files/2024-12/WMM2025_NP.txt :

139.298 85.762 2025
135.938 85.558 2026
132.995 85.350 2027
130.407 85.141 2028
128.121 84.931 2029
126.092 84.723 2030

GeoMagnetic pole location
----------------------
https://www.ncei.noaa.gov/products/wandering-geomagnetic-poles
Based on the WMM2025 coefficients for 2025.0, the Geomagnetic North Pole is at 72.76°W longitude
and 80.85°N geodetic latitude (80.79°N geocentric), and the Geomagnetic South Pole is at 107.24°E longitude
and 80.85°S geodetic latitude (80.79°S geocentric).

Scientists, map makers, and polar explorers have an interest in the locations of the dip and geomagnetic poles.
Although geomagnetic pole positions cannot be observed, they are arguably of greater significance than the dip poles
because the auroral ovals (approximate 5° latitude bands where the spectacular aurora is likely visible)
are closely centered on the geomagnetic poles. They are usually displaced slightly to the night-side
of the geomagnetic poles and greatly vary in size: bands of greatest activity occur
between 15° and 25° from the geomagnetic poles.

Intense
----------------------
After background correction, the boundary latitudes of each profile are determined at
a threshold of 4 photons cm^2 s^-1 (с)
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2005SW000162

WGS84 Coordinates
----------------------
WGS84 Earth ellipsoid flattening factor used for Geo coordinates calculation
https://en.wikipedia.org/wiki/Earth_ellipsoid
"""

# WMM2025
MAG_POLE_LOCATION_DEFAULT: dict = {"lat": 85.762, "lon": 139.298}

MAG_POLE_LOCATION = {
    2026: {"lat": 85.558, "lon": 135.938},
    2027: {"lat": 85.350, "lon": 132.995},
    2028: {"lat": 85.141, "lon": 130.407},
    2029: {"lat": 84.931, "lon": 128.121},
    2030: {"lat": 84.7238, "lon": 126.092},
}

# degrees 1 MLT
GRAD_IN_SECTOR: int = 15

# boundary intense value
MIN_INTENSE: int = 4

# Valid Kp range for the model
KP_MIN: float = 0.0
KP_MAX: float = 9.0

# https://gml.noaa.gov/grad/solcalc/glossary.html
# The solar declination varies from -23.44° at the (northern hemisphere) winter solstice,
# through 0° at the vernal equinox, to +23.44° at the summer solstice
SUN_DECLINATION: float = 24.45
