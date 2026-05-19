from carbary_model.data import CarbaryTableCoeffsData
from carbary_model.types import AuroraBondaryData


class CarbaryAuroralModel:
    """Kp-based auroral oval model, developed by James F. Carbary (2005).
    https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2005SW000162
    """
    _hours: int = 24
    data: CarbaryTableCoeffsData = CarbaryTableCoeffsData()

    def get_boundaries(self, kp: float, mlt: float) -> AuroraBondaryData:
        """Returns auroral boundaries and peak for Kp и MLT."""
        return AuroraBondaryData(
            eq_boundary=self.get_equatorward_boundary(kp, mlt),
            peak=self.get_peak_line(kp, mlt),
            po_boundary=self.get_poleward_boundary(kp, mlt),
            peak_intensity=self.get_peak_intensity(kp, mlt))

    def _get_coeffs(self, mlt: float, coeffs_dict: dict[int, tuple[float, float]]) -> tuple[float, float] | None:
        """Coefficients for nearest MLT (rounded)."""
        mlt_int = int(round(mlt)) % self._hours
        return coeffs_dict.get(mlt_int)  # No boundaries for 9-12 MLT

    def get_equatorward_boundary(self, kp: float, mlt: float) -> float | None:
        """Equatorward (EQ) point (degrees)."""
        coeffs = self._get_coeffs(mlt, self.data.eq_coeffs)
        if coeffs is None:
            return None
        c0, c1 = coeffs
        return c0 + c1 * kp

    def get_peak_line(self, kp: float, mlt: float) -> float | None:
        """Peak (PK) point (degrees)."""
        coeffs = self._get_coeffs(mlt, self.data.pk_coeffs)
        if coeffs is None:
            return None
        c0, c1 = coeffs
        return c0 + c1 * kp

    def get_poleward_boundary(self, kp: float, mlt: float) -> float | None:
        """Poleward (PO) point (degrees)."""
        coeffs = self._get_coeffs(mlt, self.data.po_coeffs)
        if coeffs is None:
            return None
        c0, c1 = coeffs
        return c0 + c1 * kp

    def get_peak_intensity(self, kp: float, mlt: float) -> float | None:
        """Peak intensity (photons cm^-2 s)."""
        coeffs = self._get_coeffs(mlt, self.data.intensity_coeffs)
        if coeffs is None:
            return None
        c0, c1 = coeffs
        intensity = c0 + c1 * kp
        return max(0.0, intensity)  # non-negative
