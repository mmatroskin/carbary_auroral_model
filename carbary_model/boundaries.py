from dataclasses import asdict

import numpy as np

from carbary_model.carbary_model import CarbaryAuroralModel
from carbary_model.types import AuroraBondarySector, Point, AuroraBondaryData
from carbary_model.const import grad_in_sector, mag_pole_lon
from carbary_model.utils import mlat_to_glat_approx, get_intense_gauss, get_intense_linear


class AuroralBoundary:
    """Auroral oval class"""
    _mlt_sectors = 24
    _size = 360
    _model = CarbaryAuroralModel
    boundaries: dict[int, AuroraBondarySector] = {}

    def __init__(self, kp: float, ut_hours: float = 0.0, advanced_mode: bool = False):
        self._is_advanced = advanced_mode
        for i in range(self._size):
            # i (0-359) - glon
            glon = float(i)

            # calculations:
            # MLT = (([lon] - [mag pole lon] + 180 + ([time UTC] * 15)) % 360) / 15
            # 180 - shift to 00 MLT
            # 15 - hourly meridian rotation (15 degrees)

            mlt_sector = int((glon - mag_pole_lon + 180.0 + (ut_hours * grad_in_sector)) % self._size // grad_in_sector)
            data = self._model().get_boundaries(kp, mlt_sector)
            self.boundaries[i] = self._get_boundaries_geographic(glon, data)

    def _get_boundaries_geographic(self,
                                   glon: float,
                                   data: AuroraBondaryData) -> AuroraBondarySector:
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

            glat = mlat_to_glat_approx(mlat, glon)

            result_dict[key] = Point(
                lon=int(round(glon)),  # longitude 0-359
                lat=int(round(glat))  # latitude -90..90
            )
        result = AuroraBondarySector(**result_dict)
        if result.peak and not result.po_boundary and not result.eq_boundary:
            result.eq_boundary = result.po_boundary = result.peak
        return AuroraBondarySector(**result_dict)

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
