"""Definition of attribute RoomKey"""
from uc3m_travel.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class RoomKey(Attribute):
    """Definition of attribute RoomKey class"""

    # pylint: disable=super-init-not-called
    def __init__(self, attr_value):
        """Definition of attribute TrackingCode init"""
        self._validation_pattern = r"[0-9a-fA-F]{64}$"
        self._error_message = "Invalid room key format"
        self._attr_value = self._validate(attr_value)
