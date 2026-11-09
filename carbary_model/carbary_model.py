"""
Core Carbary (2005) Kp-based auroral boundary model.

Implements the linear relations:

    boundary(MLT) = C0(MLT) + C1(MLT) * Kp

from Tables 1–4 of the original paper.
"""

from carbary_model.data import CarbaryTableCoeffsData
from carbary_model.types import AuroraBoundaryData
from carbary_model.utils import validate_kp, validate_mlt


class CarbaryAuroralModel:
    """Kp-based auroral oval model, developed by James F. Carbary (2005).
    https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2005SW000162
    """
    _hours: int = 24
    data: CarbaryTableCoeffsData = CarbaryTableCoeffsData()

    def get_boundaries(self, kp: float, mlt: float) -> AuroraBoundaryData:
        """Returns auroral boundaries and peak for Kp и MLT."""
        return AuroraBoundaryData(
            eq_boundary=self.get_equatorward_boundary(kp, mlt),
            peak=self.get_peak_line(kp, mlt),
            po_boundary=self.get_poleward_boundary(kp, mlt),
            peak_intensity=self.get_peak_intensity(kp, mlt))

    def _get_coeffs(self,
                    mlt: int,
                    coeffs_dict: dict[int, tuple[float, float]]) -> tuple[float, float] | None:
        """Coefficients for nearest MLT (rounded)."""
        return coeffs_dict.get(mlt)  # None for 9-12 MLT

    def get_equatorward_boundary(self, kp: float, mlt: int) -> float | None:
        """Equatorward (EQ) point (mlat, degrees)."""
        validate_kp(kp)
        validate_mlt(mlt)
        coeffs = self._get_coeffs(mlt, self.data.eq_coeffs)
        if coeffs is None:
            return None
        c0, c1 = coeffs
        return c0 + c1 * kp

    def get_peak_line(self, kp: float, mlt: int) -> float | None:
        """Peak (PK) point (mlat, degrees)."""
        validate_kp(kp)
        validate_mlt(mlt)
        coeffs = self._get_coeffs(mlt, self.data.pk_coeffs)
        if coeffs is None:
            return None
        c0, c1 = coeffs
        return c0 + c1 * kp

    def get_poleward_boundary(self, kp: float, mlt: int) -> float | None:
        """Poleward (PO) point (mlat, degrees)."""
        validate_kp(kp)
        validate_mlt(mlt)
        coeffs = self._get_coeffs(mlt, self.data.po_coeffs)
        if coeffs is None:
            return None
        c0, c1 = coeffs
        return c0 + c1 * kp

    def get_peak_intensity(self, kp: float, mlt: int) -> float | None:
        """Peak intensity (photons cm^-2 s)."""
        validate_kp(kp)
        validate_mlt(mlt)
        coeffs = self._get_coeffs(mlt, self.data.intensity_coeffs)
        if coeffs is None:
            return None
        c0, c1 = coeffs
        intensity = c0 + c1 * kp
        return max(0.0, intensity)  # non-negative
