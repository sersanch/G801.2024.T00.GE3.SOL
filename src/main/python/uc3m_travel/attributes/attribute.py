"""Attribute definition"""
import re
from uc3m_travel.exception.hotel_management_exception import HotelManagementException

#pylint: disable= too-few-public-methods
class Attribute():
    """Attribute class definition"""
    def __init__( self ):
        self._validation_pattern = r""
        self._error_message = ""
        self._attr_value = ""

    def _validate( self, attr_value ):
        """Attribute validation definition"""
        myregex = re.compile(self._validation_pattern)
        regex_matches = myregex.fullmatch(attr_value)
        if not regex_matches:
            raise HotelManagementException(self._error_message)
        return attr_value

    @property
    def value( self ):
        """returns attr_value"""
        return self._attr_value
    @value.setter
    def value( self, attr_value ):
        self._attr_value = self._validate(attr_value)
