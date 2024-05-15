"""Definition of attribute address"""
from uc3m_travel.attributes.attribute import Attribute

class NameSurname(Attribute):
    """Definition of address class"""
    #pylint: disable=super-init-not-called, too-few-public-methods
    def __init__(self, attr_value):
        """overrides init method"""
        self._validation_pattern = r"^(?=^.{10,50}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
        self._error_message = "Invalid name format"
        self._attr_value = self._validate(attr_value)
