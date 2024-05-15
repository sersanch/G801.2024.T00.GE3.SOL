"""File for registering the entries of the checkout log"""
from datetime import datetime
from uc3m_travel.attributes.room_key import RoomKey
from uc3m_travel.storage.checkout_json_store import CheckoutJsonStore
from uc3m_travel.exception.hotel_management_exception import HotelManagementException
class CheckOutEntry:
    """Class for registering the checkout data"""
    def __init__(self, room_key):
        self.__room_key = RoomKey(room_key).value
        self.__checkout_date = datetime.timestamp(datetime.utcnow())

    def save_log_entry(self):
        """saves the log entry into the json file"""
        checkouts_store = CheckoutJsonStore()
        if checkouts_store.find_item(key="_CheckOutEntry__room_key",
                                         value=self.__room_key):
            raise HotelManagementException("Guest is already out")
        checkouts_store.add_item(self)

    @property
    def checkout_date(self):
        """getter for checkout date"""
        return self.__checkout_date

    @property
    def room_key(self):
        """getter for roomkey"""
        return self.__room_key
