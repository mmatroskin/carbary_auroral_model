from dataclasses import dataclass
from enum import Enum, IntEnum


@dataclass
class Point:
    lat: float
    lon: float


@dataclass
class AuroraBoundaryData:
    eq_boundary: float | None
    peak: float | None
    po_boundary: float | None
    peak_intensity: float | None


@dataclass
class AuroraBoundarySector:
    eq_boundary: Point | None
    peak: Point | None
    po_boundary: Point | None
    peak_intensity: float | None


class PoleType(IntEnum):
    """Pole type (for experiments)"""
    CGM = 0
    GEOMAGNETIC = 1
    MAGNETIC = 2
