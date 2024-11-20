"""Module for models to unpack to."""

__all__ = ["Observation"]

from dataclasses import dataclass
from datetime import datetime
import enums

    
@dataclass
class PosAngleConstraint:
    mode: enums.PosAngleConstraintMode | None = None
    
    
@dataclass
class Observation:
    observation_id: str
    existence: enums.Existence | None = None
    title: str | None = None
    subtitle: str | None = None
    index: int | None = None
    science_band: str | None = None
    observation_time: datetime | None = None
    instrument: str | None = None
    pos_angle_constraint: PosAngleConstraint | None = None

