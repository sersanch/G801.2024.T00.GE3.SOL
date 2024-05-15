"""Class for parsing the input files for hotel arrivals"""
from .input_file import InputFile
class InputFileStay(InputFile):
    """Class for parsing input files for hotel arrivals"""
    # pylint: disable= too-few-public-methods

    _INPUT_FILE_KEYS = ["Localizer", "IdCard"]
