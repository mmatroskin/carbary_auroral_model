"""
Constant values

North Magnetic Pole position (2025)
https://www.ncei.noaa.gov/products/wandering-geomagnetic-poles
The magnetic poles or dip poles are computed from all the Gauss coefficients using an iterative method.
Magnetic poles derived in this fashion are geographically closer to the experimentally observed poles.
Based on the current WMM, the 2025 location of the North Magnetic Pole is 85.762°N and 139.298°E and
the South Magnetic Pole is 63.851°S and 135.078°E.
https://www.ncei.noaa.gov/sites/default/files/2024-12/WMM2025_NP.txt

After background correction, the boundary latitudes of each profile are determined at
a threshold of 4 photons cm^2 s^-1 (с)
https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2005SW000162
"""

# Geomagnetic North Pole
geo_mag_pole_lat: float = 80.85
geo_mag_pole_lon: float = -72.76 + 360

# WMM2025
mag_pole_lat: float = 85.762
mag_pole_lon: float = 139.298

# degrees 1 MLT
grad_in_sector: int = 15

# boundary intense value
min_intense: int = 4
