"""JsonStore definition"""
import json
from uc3m_travel.exception.hotel_management_exception import HotelManagementException

class JsonStore():
    """JsonStore class"""

    _data_list = []
    _file_name = ""

    def __init__(self):
        self.load_list_from_file()

    def save_list_to_file( self ):
        """saves the list in the store"""
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise HotelManagementException("Wrong file or file path") from ex

    def load_list_from_file( self ):
        """load the list of items from the store"""
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex
            # append the delivery info

    def add_item( self, item ):
        """add a new item in the store"""
        self.load_list_from_file()
        self._data_list.append(item.__dict__)
        self.save_list_to_file()

    def find_item (self, value, key):
        """finds an item in the store"""
        self.load_list_from_file()
        print(key)
        print(value)
        for item in self._data_list:
            print(item)
            if item[key] == value:
                print("found")
                return item
        return None

    def remove_item(self, value, key):
        """deletes key + value identified item from the store"""
        self.load_list_from_file()
        print("Largo antes: " + str(len(self._data_list )))
        self._data_list = [item for item in self._data_list if item.get(key) != value]
        print("Largo despues: " + str(len(self._data_list)))
        self.save_list_to_file()
