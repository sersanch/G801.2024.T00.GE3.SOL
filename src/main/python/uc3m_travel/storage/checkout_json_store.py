"""Checkuots Store"""
from uc3m_travel.storage.json_store import JsonStore
from uc3m_travel.cfg.hotel_management_config import JSON_FILES_PATH
#pylint: disable=too-few-public-methods
class CheckoutJsonStore():
    """Checkouts Store for singleton"""
    class __CheckoutJsonStore(JsonStore):
        """"Checkouts Store singleton class"""
        #pylint: disable=invalid-name
        _file_name = JSON_FILES_PATH + "store_check_out.json"

        def add_item( self, item ):
            self.load_list_from_file()
            self._data_list.append(item.__dict__)
            self.save_list_to_file()

    checkout_store_intance = None

    def __new__(cls):
        if not CheckoutJsonStore.checkout_store_intance:
            CheckoutJsonStore.checkout_store_intance = (
                CheckoutJsonStore.__CheckoutJsonStore())
        return CheckoutJsonStore.checkout_store_intance

    def __getattr__(self, item):
        return getattr(CheckoutJsonStore.checkout_store_intance,
                       item)

    def __setattr__(self, key, value):
        return setattr(CheckoutJsonStore.checkout_store_intance,
                       key,
                       value)
