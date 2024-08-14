from decimal import Decimal, InvalidOperation
from typing import Literal

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class GPSCoordinateValidator:
    def __init__(self, coordinate_name: Literal['latitude', 'longitude']):
        if coordinate_name not in ('latitude', 'longitude'):
            raise ValueError('Coordinate name must be only "latitude" or "longitude".')
        self._coordinate_name = coordinate_name

    __value_type = Decimal | str | int | float

    def __call__(self, value: __value_type, *args, **kwargs):
        try:
            if not isinstance(value, Decimal):
                value = Decimal(str(value))
        except InvalidOperation:
            raise ValidationError('Got value cannot convert to decimal type. Value must be a number of any type.')

        if self._coordinate_name == 'latitude' and not Decimal('-90') <= value <= Decimal('90'):
            raise ValidationError('Latitude must be in the range from -90 to 90 inclusive.')
        elif self._coordinate_name == 'longitude' and not Decimal('-180') <= value <= Decimal('180'):
            raise ValidationError('Longitude must be in the range from -180 to 180 inclusive.')
