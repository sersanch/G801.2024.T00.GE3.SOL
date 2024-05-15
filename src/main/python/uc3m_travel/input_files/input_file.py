"""Generic parsers for Json input files"""
import json
from uc3m_travel.exception.hotel_management_exception import HotelManagementException

class InputFile():
    """Generic parser class"""

    _INPUT_FILE_KEYS=[]
    input_dict = None

    def __init__(self, file_input):
        self.load_input_file(file_input)
        self.validate()

    def load_input_file(self, file_input):
        """loads the content of the input file into a dictionary"""
        try:
            with open(file_input, "r", encoding="utf-8", newline="") as file:
                self.input_dict = json.load(file)
        except FileNotFoundError as ex:
            raise HotelManagementException("Error: file input not found") from ex
        except json.JSONDecodeError as ex:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def validate(self):
        """Validates the input data"""
        for input_key in self._INPUT_FILE_KEYS:
            if input_key not in self.input_dict.keys():
                raise HotelManagementException("Error - Invalid Key in JSON")
