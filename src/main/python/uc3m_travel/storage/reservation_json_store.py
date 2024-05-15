"""ReservationJsonStore definitoin"""
from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.cfg.hotel_management_config import JSON_FILES_PATH
from uc3m_travel.exception.hotel_management_exception import HotelManagementException

#pylint: disable=too-few-public-methods
class ReservationJsonStore():
    """Reservation JSON Store (singleton)"""
    class __ReservationJsonStore(JsonStore):
        """ReservationJsonStore singleton class"""
        #pylint: disable=invalid-name
        _file_name = JSON_FILES_PATH + "store_reservation.json"

        def add_item( self, item ):
            reservation_found = self.find_item(item.localizer, "_HotelReservation__localizer")
            if reservation_found:
                raise HotelManagementException("Reservation already exists")
            reservation_found = self.find_item(item.id_card, "_HotelReservation__id_card")
            if reservation_found:
                raise HotelManagementException("This ID card has another reservation")
            super().add_item(item)

    reservation_store_instance = None

    def __new__(cls):
        if not ReservationJsonStore.reservation_store_instance:
            ReservationJsonStore.reservation_store_instance = (
                ReservationJsonStore.__ReservationJsonStore())
        return ReservationJsonStore.reservation_store_instance

    def __getattr__(self, item):
        return getattr(ReservationJsonStore.reservation_store_instance,
                       item)

    def __setattr__(self, key, value):
        return setattr(ReservationJsonStore.reservation_store_instance,
                       key,
                       value)
