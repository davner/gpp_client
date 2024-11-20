"""Module for handling astropy.Angle in marshmallow."""

__all__ = ["AstropyAngleField"]

from astropy import units as u
from astropy.coordinates import Angle
from astropy.units import UnitConversionError
from marshmallow import fields
from typing import Any, Literal, Mapping


SerializeFormats = Literal["hms", "dms"]


class AstropyAngleField(fields.Field):
    """A custom Marshmallow field for handling Astropy Angle objects.

    This field supports serialization and deserialization of Astropy Angle objects
    into various units or string formats, such as 'hms' (hours, minutes, seconds)
    or 'dms' (degrees, minutes, seconds).

    Parameters
    ----------
    unit : `str | u.Unit | None`, optional
        The expected unit for numerical serialization, by default `None`.
    serialize_format : `SerializeFormats | None`, optional
        Special formats for string serialization ('hms' or 'dms'), by default `None`
    to_string_kwargs : `dict[str, Any] | None`, optional
        Keyword arguments for `Angle.to_string()` when serializing, by default
        `None`

    Raises
    ------
    ValidationError
        Raised if the provided unit is not a valid Astropy Unit.
    ValidationError
        Raised if If the provided serialize format is invalid.
    """

    SERIALIZE_FORMATS = {"hms", "dms"}

    default_error_messages = {
        "invalid": "Not a valid 'astropy.Angle'.",
        "invalid_unit": "'{input_unit}' is not a valid 'astropy.Unit'.",
        "invalid_serialization_format": "'{input_serialize_format}' is not a valid serialize format.",
        "serialize_error": "Value '{input}' cannot be serialized.",
        "deserialize_error": "Value '{input}' cannot be deserialized.",
    }

    def __init__(
        self,
        *,
        unit: str | u.Unit | None = None,
        serialize_format: SerializeFormats | None = None,
        to_string_kwargs: dict[str, Any] | None = None,
        **kwargs,
    ):
        try:
            self.unit = u.Unit(unit) if unit else None
        except UnitConversionError:
            raise self.make_error("invalid_unit", input_unit=unit)

        if serialize_format and serialize_format not in self.SERIALIZE_FORMATS:
            raise self.make_error(
                "invalid_serialize_format", input_serialize_format=serialize_format
            )

        self.serialize_format = serialize_format
        self.to_string_kwargs = to_string_kwargs or {}

        super().__init__(**kwargs)

    def _serialize(
        self, value: Angle, attr: str | None, obj: Any, **kwargs
    ) -> str | float | None:
        """Serialize the Angle to its value in the specified unit or format.

        Parameters
        ----------
        value : `Angle`
            The Angle object to serialize.
        attr : `str | None`
            The attribute/key being serialized (unused in this method).
        obj : `Any`
            The parent object containing the value (unused in this method).

        Returns
        -------
        `str | float | None`
            The serialized representation of the angle, either as a string
            (if 'hms' or 'dms' is specified) or as a float in the specified unit.

        Raises
        ------
        ValidationError
            Raised if the value is not a valid Astropy Angle or cannot be serialized.
        """
        if value is None:
            return None

        if not isinstance(value, Angle):
            raise self.make_error("invalid")

        try:
            # Handle special string formats.
            if self.serialize_format == "hms":
                # Convert to hourangle, then format as h:m:s.
                return value.to(u.hourangle).to_string(**self.to_string_kwargs)
            elif self.serialize_format == "dms":
                # Convert to degrees, then format as d:m:s.
                return value.to(u.deg).to_string(**self.to_string_kwargs)

            # For numerical values, use the specified Astropy unit.
            return value.to_value(self.unit).item()
        except Exception:
            raise self.make_error("serialize_error", input=value)

    def _deserialize(
        self, value: Any, attr: str | None, data: Mapping[str, Any] | None, **kwargs
    ) -> Angle:
        """Deserialize the input into an Astropy Angle.

        Parameters
        ----------
        value : `Any`
            The input value to deserialize (e.g., string or numeric).
        attr : `str | None`
            The attribute/key being deserialized (unused in this method).
        data : `Mapping[str, Any] | None`
            The full data dictionary being deserialized (unused in this method).

        Returns
        -------
        `Angle`
            The deserialized Astropy Angle object.

        Raises
        ------
        ValidationError
            Raised if the input value cannot be deserialized into an Astropy Angle.
        """
        try:
            unit = self.unit

            # Determine if need to override unit.
            if self.serialize_format == "hms":
                unit = u.hourangle
            elif self.serialize_format == "dms":
                unit = u.deg

            return Angle(value, unit=unit)

        except Exception:
            raise self.make_error("deserialize_error", input=value)
