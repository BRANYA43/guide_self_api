from decimal import Decimal
from unittest import TestCase

from django.core.exceptions import ValidationError

from travels.validators import GPSCoordinateValidator


class GPSCoordinateValidatorTest(TestCase):
    def test_validator_raises_error_with_invalid_coordinate_name(self):
        GPSCoordinateValidator('latitude')  # not raise error
        GPSCoordinateValidator('longitude')  # not raise error
        self.assertRaisesRegex(
            ValueError,
            r'Coordinate name must be only "latitude" or "longitude".',
            GPSCoordinateValidator,
            'invalid_name',
        )

    def test_validate_raises_error_with_invalid_value(self):
        validate = GPSCoordinateValidator('latitude')
        validate(Decimal('1'))  # not raise
        validate('1')  # not raise
        validate(1)  # not raise
        validate(1.1)  # not raise

        self.assertRaisesRegex(
            ValidationError,
            r'Got value cannot convert to decimal type. Value must be a number of any type.',
            validate,
            'sdf',
        )

    def test_validator_raises_error_with_invalid_latitude_value(self):
        validate = GPSCoordinateValidator('latitude')
        validate(-90)  # not raise
        validate(90)  # not raise

        self.assertRaisesRegex(
            ValidationError,
            r'Latitude must be in the range from -90 to 90 inclusive.',
            validate,
            -90.1,
        )

        self.assertRaisesRegex(
            ValidationError,
            r'Latitude must be in the range from -90 to 90 inclusive.',
            validate,
            90.1,
        )

    def test_validator_raises_error_with_invalid_longitude_value(self):
        validate = GPSCoordinateValidator('longitude')
        validate(-180)  # not raise
        validate(180)  # not raise

        self.assertRaisesRegex(
            ValidationError,
            r'Longitude must be in the range from -180 to 180 inclusive.',
            validate,
            -180.1,
        )

        self.assertRaisesRegex(
            ValidationError,
            r'Longitude must be in the range from -180 to 180 inclusive.',
            validate,
            180.1,
        )
