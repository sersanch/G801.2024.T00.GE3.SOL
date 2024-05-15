"""StayJsonStore storage"""
from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.cfg.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.exception.hotel_management_exception import HotelManagementException
#pylint: disable=invalid-name

class StayJsonStore:
    """Stay json store for singleton"""
    class __StayJsonStore(JsonStore):
        """StayJsonStore singleton class"""

        _file_name = JSON_FILES_PATH + "store_check_in.json"

        def add_item( self, item ):
            if self.find_item(key="_HotelStay__room_key",
                              value=item.room_key):
                raise HotelManagementException("ckeckin  ya realizado")
            super().add_item(item)

    stay_json_store_instance = None

    def __new__(cls):
        if not StayJsonStore.stay_json_store_instance:
            StayJsonStore.stay_json_store_instance = (
                StayJsonStore.__StayJsonStore())
        return StayJsonStore.stay_json_store_instance

    def __getattr__(self, item):
        return getattr(StayJsonStore.stay_json_store_instance,
                       item)

    def __setattr__(self, key, value):
        return setattr(StayJsonStore.stay_json_store_instance,
                       key,
                       value)
