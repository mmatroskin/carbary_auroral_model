from dataclasses import dataclass


@dataclass
class Point:
    lat: int
    lon: int


@dataclass
class AuroraBondaryData:
    eq_boundary: float | None
    peak: float | None
    po_boundary: float | None
    peak_intensity: float | None


@dataclass
class AuroraBondarySector:
    eq_boundary: Point | None
    peak: Point | None
    po_boundary: Point | None
    peak_intensity: float | None
