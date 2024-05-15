"""Class for parsing the input files for hotel reservation date changes"""
from .input_file import InputFile
class InputFileChangeReservationDate(InputFile):
    """Class for parsing input files for hotel reservation date changes"""
    # pylint: disable= too-few-public-methods

    _INPUT_FILE_KEYS = ["Localizer", "NewArrivalDate"]
