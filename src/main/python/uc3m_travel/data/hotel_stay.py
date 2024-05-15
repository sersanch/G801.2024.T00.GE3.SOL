''' Class HotelStay (GE2.2) '''

from datetime import datetime
import hashlib
from freezegun import freeze_time
from uc3m_travel.data.hotel_reservation import HotelReservation
from uc3m_travel.exception.hotel_management_exception import HotelManagementException
from uc3m_travel.storage.stay_json_store import StayJsonStore
from uc3m_travel.attributes.room_key import RoomKey
from uc3m_travel.attributes.room_type import RoomType
from uc3m_travel.attributes.localizer import Localizer
from uc3m_travel.attributes.id_card import IdCard
from uc3m_travel.attributes.num_days import NumDays
from uc3m_travel.input_files.input_file_stay import InputFileStay
from uc3m_travel.data.checkout_log_entry import CheckOutEntry
class HotelStay():
    """Class for representing hotel stays"""
    def __init__(self,
                 idcard:str,
                 localizer:str,
                 numdays:int,
                 roomtype:str):
        """constructor for HotelStay objects"""
        self.__alg = "SHA-256"
        self.__type = RoomType(roomtype).value
        self.__idcard = IdCard(idcard).value
        self.__localizer = Localizer(localizer).value
        justnow = datetime.utcnow()
        self.__arrival = datetime.timestamp(justnow)
        #timestamp is represented in seconds.miliseconds
        #to add the number of days we must express num_days in seconds
        self.__departure = self.__arrival + (NumDays(numdays).value * 24 * 60 * 60)
        self.__room_key = hashlib.sha256(self.__signature_string().encode()).hexdigest()

    def __signature_string(self):
        """Composes the string to be used for generating the key for the room"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",localizer:" + \
            self.__localizer + ",arrival:" + str(self.__arrival) + \
            ",departure:" + str(self.__departure) + "}"

    @property
    def id_card(self):
        """Property that represents the product_id of the patient"""
        return self.__idcard

    @id_card.setter
    def id_card(self, value):
        self.__idcard = value

    @property
    def localizer(self):
        """Property that represents the order_id"""
        return self.__localizer

    @localizer.setter
    def localizer(self, value):
        self.__localizer = value

    @property
    def arrival(self):
        """Property that represents the phone number of the client"""
        return self.__arrival

    @property
    def room_key(self):
        """Returns the sha256 signature of the date"""
        return self.__room_key

    @property
    def departure(self):
        """Returns the issued at value"""
        return self.__departure

    @departure.setter
    def departure(self, value):
        """returns the value of the departure date"""
        self.__departure = value


    @classmethod
    def create_guest_arrival_from_file(cls, file_input):
        """creates the guest arrival from the content of the input file"""
        input_file = InputFileStay(file_input)
        new_reservation = (HotelReservation.create_reservation_from_arrival
                           (input_file.input_dict["IdCard"],
                            input_file.input_dict["Localizer"]))
        # compruebo si hoy es la fecha de checkin
        reservation_format = "%d/%m/%Y"
        date_obj = datetime.strptime(new_reservation.arrival, reservation_format)
        if date_obj.date() != datetime.date(datetime.utcnow()):
            raise HotelManagementException("Error: today is not reservation date")
        # genero la room key para ello llamo a Hotel Stay

        my_checkin = HotelStay(idcard=input_file.input_dict["IdCard"],
                               numdays=int(new_reservation.num_days),
                               localizer=input_file.input_dict["Localizer"],
                               roomtype=new_reservation.room_type)
        return my_checkin

    @classmethod
    def get_stay_from_roomkey(cls, room_key):
        """retrieves from the stays store one stay based on the roomkey"""
        room_key = RoomKey(room_key).value
        # check thawt the roomkey is stored in the checkins file
        stays_store = StayJsonStore()
        stay_to_checkout = stays_store.find_item(key="_HotelStay__room_key",
                                                 value=room_key)
        if stay_to_checkout is None:
            raise HotelManagementException("Error: room key not found")

        new_reservation = HotelReservation.create_reservation_from_arrival(
            my_id_card=stay_to_checkout["_HotelStay__idcard"],
            my_localizer=stay_to_checkout["_HotelStay__localizer"])
        print(stay_to_checkout["_HotelStay__arrival"])
        with freeze_time(datetime.fromtimestamp(stay_to_checkout["_HotelStay__arrival"])):
            stay = cls(idcard=stay_to_checkout["_HotelStay__idcard"],
                       localizer=stay_to_checkout["_HotelStay__localizer"],
                       roomtype=stay_to_checkout["_HotelStay__type"],
                       numdays=new_reservation.num_days)
        return stay

    def check_out(self):
        """executes the checkout of the stay itself"""
        if datetime.utcnow().date() != datetime.fromtimestamp(self.__departure).date():
            raise HotelManagementException("Error: today is not the departure day")
        check_out_log = CheckOutEntry(self.room_key)
        check_out_log.save_log_entry()

    def save(self):
        """Saves the stay into the JsonStore"""
        stays_store = StayJsonStore()
        stays_store.add_item(self)
