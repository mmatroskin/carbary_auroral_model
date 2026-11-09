"""Carbary Model Exceptions"""

class CarbaryModelCommonError(Exception):
    """Base exception for the package."""


class InvalidKpError(CarbaryModelCommonError, ValueError):
    """Raised when Kp is outside the valid range [0, 9]."""


class InvalidMLTError(CarbaryModelCommonError, ValueError):
    """Raised when Magnetic Local Time is outside the valid range [0, 24)."""

class UnexpectedError(CarbaryModelCommonError, ValueError):
    """Raised when DataSource has invalid format or in other unexpected cause"""
