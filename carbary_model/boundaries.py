"""
The Interface builds an auroral oval with geographic coordinates.
"""
from dataclasses import asdict

import numpy as np

from carbary_model.exceptions import UnexpectedError
from carbary_model.carbary_model import CarbaryAuroralModel
from carbary_model.types import AuroraBoundarySector, Point, AuroraBoundaryData
from carbary_model.const import GRAD_IN_SECTOR
from carbary_model.utils import mlat_mlon_to_glat_approx, get_intense_gauss, get_intense_linear, get_mag_pole, \
    glon_to_mlon_approx, get_geomag_pole


class AuroralBoundary:
    """Auroral oval class"""
    _mlt_sectors: int = 24
    _size: int = 360
    _shift: int = 180  # shift to 00 MLT
    _model: type[CarbaryAuroralModel] = CarbaryAuroralModel
    pole: Point
    boundaries: dict[int, AuroraBoundarySector]
    ut_hours: float

    def __init__(self,
                 kp: float,
                 ut_hours: float = 0.0,
                 advanced_mode: bool = False,
                 strict_mode: bool = False):

        self._is_advanced = advanced_mode
        self.ut_hours = ut_hours
        self.pole = get_geomag_pole() if strict_mode else get_mag_pole()
        self.boundaries = {}
        for i in range(self._size):
            # i (0-359) - glon
            glon = float(i)

            # calculations:
            # MLT = (([lon] - [mag pole lon] + 180 + ([time UTC] * 15)) % 360) / 15
            # 180 - shift
            # 15 - hourly meridian rotation (15 degrees)
            mlon = glon_to_mlon_approx(glon, self.pole)

            mlt = (mlon + self._shift + (ut_hours * GRAD_IN_SECTOR)) % self._size
            mlt_sector: float = int(mlt // GRAD_IN_SECTOR) % self._mlt_sectors

            data = self._model().get_boundaries(kp, mlt_sector)
            self.boundaries[i] = self._get_boundaries_geographic(glon, mlon, data)

    def _get_boundaries_geographic(self,
                                   glon: float,
                                   mlon: float,
                                   data: AuroraBoundaryData) -> AuroraBoundarySector:
        """
        Geographic coordinates for boundary:
            longitude: 0–359
            latitude: -90 – 90
        """

        bounds = asdict(data)

        result_dict = {"peak_intensity": bounds.pop("peak_intensity")}

        for key, mlat in bounds.items():
            if mlat is None:
                result_dict[key] = None
                continue

            glat = mlat_mlon_to_glat_approx(mlat, mlon, self.pole)

            result_dict[key] = Point(
                lon=int(round(glon)),  # longitude 0-359
                lat=int(round(glat))  # latitude -90..90
            )
        result = AuroraBoundarySector(**result_dict)
        if result.peak and not result.po_boundary and not result.eq_boundary:
            result.eq_boundary = result.po_boundary = result.peak
        return result

    @property
    def intensity_map(self) -> np.ndarray:
        """Intensity in every point belongs to auroral oval. Data format: [lon, lat, intense]"""

        get_intense = get_intense_gauss if self._is_advanced else get_intense_linear

        result = []
        step = 0.5
        for key, val in self.boundaries.items():
            if val is not None and val.peak and val.eq_boundary and val.po_boundary:
                item = [[val.eq_boundary.lon,
                         lat,
                         get_intense(lat,
                                     val.eq_boundary.lat,
                                     val.peak.lat,
                                     val.peak_intensity)]
                        for lat in np.arange(val.eq_boundary.lat, val.peak.lat, step)]
                tmp = [[val.eq_boundary.lon,
                       lat,
                       get_intense(lat,
                                   val.po_boundary.lat,
                                   val.peak.lat,
                                   val.peak_intensity)]
                       for lat in np.arange(val.peak.lat, val.po_boundary.lat + step, step)]
                item.extend(tmp)
                result.extend(item)
        return np.array(result)
