"""Definition of attribute NumDays"""
from uc3m_travel.attributes.attribute import Attribute
from uc3m_travel.exception.hotel_management_exception import HotelManagementException

class NumDays(Attribute):
    """Definition of attribute ZipCode class"""

    # pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """Definition of attribute NumDays init"""
        self._attr_value = self._validate(attr_value)

    def _validate(self, attr_value):
        """Definition of attribute ZipCocd validation"""
        try:
            days = int(attr_value)
        except ValueError as ex:
            raise HotelManagementException("Invalid num_days datatype") from ex
        if (days < 1 or days > 10):
            raise HotelManagementException("Numdays should be in the range 1-10")
        return attr_value
