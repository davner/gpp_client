"""Module for schemas for marshmallow."""

__all__ = [
    "AngleSchema",
    "PosAngleConstraintSchema",
    "ProgramReferenceSchema",
    "ObservationReferenceSchema",
    "ObservationSchema",
]

import enums
from astropy import units as u
from astropy_angle_field import AstropyAngleField
from marshmallow import (
    Schema,
    fields,
    post_load,
)
from marshmallow.validate import Range
from models import Observation


class AngleSchema(Schema):
    microarcseconds = AstropyAngleField(unit=u.microarcsecond, required=True)
    microseconds = AstropyAngleField(unit=u.microsecond, required=True)
    milliarcseconds = AstropyAngleField(unit=u.milliarcsecond, required=True)
    milliseconds = AstropyAngleField(unit=u.millisecond, required=True)
    arcseconds = AstropyAngleField(unit=u.arcsecond, required=True)
    seconds = AstropyAngleField(unit=u.second, required=True)
    arcminutes = AstropyAngleField(unit=u.arcminute, required=True)
    minutes = AstropyAngleField(unit=u.minute, required=True)
    degrees = AstropyAngleField(unit=u.degree, required=True)
    hours = AstropyAngleField(unit=u.hour, required=True)
    hms = AstropyAngleField(unit=u.hour, serialize_format="hms", required=True)
    dms = AstropyAngleField(unit=u.degree, serialize_format="dms", required=True)


class PosAngleConstraintSchema(Schema):
    mode = fields.Enum(enums.PosAngleConstraintMode, by_value=True, required=True)
    # angle = fields.Nested(AngleSchema, required=True)


class ProgramReferenceSchema(Schema):
    label = fields.Str(required=True)
    type = fields.Enum(enums.ProgramType, by_value=True, required=True)


class ObservationReferenceSchema(Schema):
    label = fields.Str(required=True)
    program = fields.Nested(ProgramReferenceSchema, allow_null=True)
    index = fields.Int(required=True, validate=Range(min=1))


class ObservationSchema(Schema):
    id = fields.Str(required=True, attribute="observation_id")
    existence = fields.Enum(enums.Existence, by_value=True)
    index = fields.Int(required=True, validate=Range(min=1))
    title = fields.Str(required=True)
    subtitle = fields.Str(allow_none=True)
    science_band = fields.Enum(
        enums.ScienceBand, by_value=True, data_key="scienceBand", allow_none=True
    )
    observation_time = fields.DateTime(
        format="iso", data_key="observationTime", allow_none=True
    )
    instrument = fields.Enum(enums.Instrument, by_value=True, allow_none=True)
    pos_angle_constraint = fields.Nested(PosAngleConstraintSchema, required=True, data_key="posAngleConstraint")

    @post_load
    def make_observation(self, data, **kwargs):
        """Convert validated data to an Observation instance."""
        return Observation(**data)
