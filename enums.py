"""Module for enums."""

__all__ = [
    "Existence",
    "ScienceBand",
    "ProgramType",
    "PosAngleConstraintMode",
    "Instrument",
]

from enum import Enum


class Existence(Enum):
    PRESENT = "PRESENT"
    DELETED = "DELETED"


class ScienceBand(Enum):
    BAND_1 = "BAND1"
    BAND_2 = "BAND2"
    BAND_3 = "BAND3"
    BAND_4 = "BAND4"


class ProgramType(Enum):
    CALIBRATION = "CALIBRATION"
    ENGINEERING = "ENGINEERING"
    EXAMPLE = "EXAMPLE"
    LIBRARY = "LIBRARY"
    SCIENCE = "SCIENCE"
    SYSTEM = "SYSTEM"


class PosAngleConstraintMode(Enum):
    UNBOUNDED = "UNBOUNDED"
    FIXED = "FIXED"
    ALLOW_FLIP = "ALLOW_FLIP"
    AVERAGE_PARALLACTIC = "AVERAGE_PARALLACTIC"
    PARALLACTIC_OVERRIDE = "PARALLACTIC_OVERRIDE"


class Instrument(Enum):
    ACQ_CAM = "ACQ_CAM"
    BHROS = "BHROS"
    FLAMINGOS2 = "FLAMINGOS2"
    GHOST = "GHOST"
    GMOS_NORTH = "GMOS_NORTH"
    GMOS_SOUTH = "GMOS_SOUTH"
    GNIRS = "GNIRS"
    GPI = "GPI"
    GSAOI = "GSAOI"
    MICHELLE = "MICHELLE"
    NICI = "NICI"
    NIFS = "NIFS"
    NIRI = "NIRI"
    PHOENIX = "PHOENIX"
    TRECS = "TRECS"
    VISITOR = "VISITOR"
    SCORPIO = "SCORPIO"
    ALOPEKE = "ALOPEKE"
    ZORRO = "ZORRO"
