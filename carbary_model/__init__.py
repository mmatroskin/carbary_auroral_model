"""
Carbary (2005) Kp-based auroral oval model.

Citation
--------
Carbary, J. F. (2005), A Kp-based model of auroral boundaries,
Space Weather, 3, S10001, doi:10.1029/2005SW000162.
"""
from carbary_model.boundaries import AuroralBoundary
from carbary_model.exceptions import CarbaryModelCommonError, InvalidKpError, InvalidMLTError, UnexpectedError
from carbary_model.types import Point, AuroraBoundarySector
from carbary_model.__about__ import __author__, __copyright__, __version__


__all__ = (
    "__author__",
    "__copyright__",
    "__version__",
    "AuroralBoundary",
    "AuroraBoundarySector",
    "Point",
    "CarbaryModelCommonError",
    "InvalidKpError",
    "InvalidMLTError",
    "UnexpectedError",
)
