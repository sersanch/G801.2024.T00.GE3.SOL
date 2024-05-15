"""Hotel reservation class"""
import hashlib
from datetime import datetime
from freezegun import freeze_time
from uc3m_travel.exception.hotel_management_exception import HotelManagementException
from uc3m_travel.attributes.id_card import IdCard
from uc3m_travel.attributes.localizer import Localizer
from uc3m_travel.attributes.room_type import RoomType
from uc3m_travel.attributes.arrival_date import ArrivalDate
from uc3m_travel.attributes.credit_card import CreditCard
from uc3m_travel.attributes.num_days import NumDays
from uc3m_travel.attributes.name_surname import NameSurname
from uc3m_travel.attributes.phone_number import PhoneNumber
from uc3m_travel.input_files.input_file_change_reservation_date import InputFileChangeReservationDate
from uc3m_travel.storage.reservation_json_store import ReservationJsonStore

class HotelReservation:
    """Class for representing hotel reservations"""
    #pylint: disable=too-many-arguments, too-many-instance-attributes


    @classmethod
    def create_reservation_from_localizer(cls, my_localizer):
        """gets the reservation from the store using the localizer """
        reservations_store = ReservationJsonStore()
        my_localizer = Localizer(my_localizer).value
        reservation = reservations_store.find_item(key="_HotelReservation__localizer",
                                                   value=my_localizer)
        if reservation is None:
            raise HotelManagementException("Error: localizer not found")

        reservation_date = datetime.fromtimestamp(
            reservation["_HotelReservation__reservation_date"])
        with freeze_time(reservation_date):
            new_reservation = cls(credit_card_number=
                                  reservation["_HotelReservation__credit_card_number"],
                                  id_card=reservation["_HotelReservation__id_card"],
                                  num_days=reservation["_HotelReservation__num_days"],
                                  room_type=reservation["_HotelReservation__room_type"],
                                  arrival=reservation["_HotelReservation__arrival"],
                                  name_surname=reservation["_HotelReservation__name_surname"],
                                  phone_number=reservation["_HotelReservation__phone_number"])
        if new_reservation.localizer != my_localizer:
            raise HotelManagementException("Error: reservation has been manipulated")
        return new_reservation
    @classmethod
    def create_reservation_from_arrival(cls, my_id_card, my_localizer):
        """Creates a reservation object from the data received for an arrival"""
        my_id_card = IdCard(my_id_card).value
        my_localizer = Localizer(my_localizer).value
        reservation = HotelReservation.create_reservation_from_localizer(my_localizer)
        if my_id_card != reservation.id_card:
            raise HotelManagementException("Error: Localizer is not correct for this IdCard")
        return reservation
        # regenrar clave y ver si coincide

    @classmethod
    def change_arrival_date(cls, file_input):
        input_file = InputFileChangeReservationDate(file_input)
        new_arrival_date = ArrivalDate(input_file.input_dict["NewArrivalDate"]).value
        date_new_arr = datetime.strptime(new_arrival_date, "%d/%m/%Y")
        date_today = datetime.now()
        if date_new_arr <= date_today:
            raise HotelManagementException("Invalid new arrival date. Must be greater than today")
        reservation = HotelReservation.create_reservation_from_localizer(input_file.input_dict["Localizer"])
        actual_arr_date = reservation.arrival
        date_act_arr = datetime.strptime(actual_arr_date, "%d/%m/%Y")
        print(str(date_new_arr))
        print(str(date_act_arr))
        if date_new_arr <= date_act_arr:
            raise HotelManagementException("Invalid new arrival date. Must be greater than the current arrival date")
        return new_arrival_date, reservation

    def __init__(self,
                 id_card:str,
                 credit_card_number:str,
                 name_surname:str,
                 phone_number:str,
                 room_type:str,
                 arrival:str,
                 num_days:int):
        """constructor of reservation objects"""
        self.__credit_card_number = CreditCard(credit_card_number).value
        self.__id_card = IdCard(id_card).value
        justnow = datetime.utcnow()
        self.__arrival = ArrivalDate(arrival).value
        self.__reservation_date = datetime.timestamp(justnow)
        self.__name_surname = NameSurname(name_surname).value
        self.__phone_number = PhoneNumber(phone_number).value
        self.__room_type = RoomType(room_type).value
        self.__num_days = NumDays(num_days).value
        self.__localizer =  hashlib.md5(str(self).encode()).hexdigest()


    def save(self):
        """Saves the reservation into the ReservationsJsonStore"""
        reservations_store = ReservationJsonStore()
        reservations_store.add_item(self)
        return self.localizer

    def remove(self):
        """Saves the reservation into the ReservationsJsonStore"""
        reservations_store = ReservationJsonStore()
        reservations_store.remove_item(self.localizer, "_HotelReservation__localizer")

    def __str__(self):
        """return a json string with the elements required to calculate the localizer"""
        #VERY IMPORTANT: JSON KEYS CANNOT BE RENAMED
        json_info = {"id_card": self.__id_card,
                     "name_surname": self.__name_surname,
                     "credit_card": self.__credit_card_number,
                     "phone_number:": self.__phone_number,
                     "reservation_date": self.__reservation_date,
                     "arrival_date": self.__arrival,
                     "num_days": self.__num_days,
                     "room_type": self.__room_type,
                     }
        return "HotelReservation:" + json_info.__str__()
    @property
    def credit_card(self):
        """property for getting and setting the credit_card number"""
        return self.__credit_card_number
    @credit_card.setter
    def credit_card(self, value):
        self.__credit_card_number = value

    @property
    def id_card(self):
        """property for getting and setting the id_card"""
        return self.__id_card
    @id_card.setter
    def id_card(self, value):
        self.__id_card = value


    @property
    def localizer(self):
        """Returns the md5 signature"""
        return self.__localizer

    @property
    def arrival(self):
        """getter for the arrival"""
        return self.__arrival

    @arrival.setter
    def arrival(self, value):
        self.__arrival = value

    @property
    def num_days(self):
        """getter for the num_days"""
        return self.__num_days
    @property
    def room_type(self):
        """getter for the room_type"""
        return self.__room_type
