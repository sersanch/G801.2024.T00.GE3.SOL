"""Module for the hotel manager"""
from datetime import datetime

from uc3m_travel import HotelManagementException
from uc3m_travel.attributes.arrival_date import ArrivalDate
from uc3m_travel.attributes.localizer import Localizer
from uc3m_travel.data.hotel_reservation import HotelReservation
from uc3m_travel.data.hotel_stay import HotelStay
from uc3m_travel.input_files.input_file_change_reservation_date import InputFileChangeReservationDate
from uc3m_travel.storage.reservation_json_store import ReservationJsonStore


class HotelManager:
    """Singleton class for HotelManager"""
    class __HotelManager:
        """Class with all the methods for managing reservations and stays"""
        def __init__(self):
            pass

        # pylint: disable=too-many-arguments
        def room_reservation(self,
                             credit_card:str,
                             name_surname:str,
                             id_card:str,
                             phone_number:str,
                             room_type:str,
                             arrival_date: str,
                             num_days:int)->str:
            """manges the hotel reservation: creates a reservation and saves it into a json file"""
            my_reservation = HotelReservation(id_card=id_card,
                                              credit_card_number=credit_card,
                                              name_surname=name_surname,
                                              phone_number=phone_number,
                                              room_type=room_type,
                                              arrival=arrival_date,
                                              num_days=num_days)

            return my_reservation.save()



        def guest_arrival(self, file_input:str)->str:
            """manages the arrival of a guest with a reservation"""
            my_checkin = HotelStay.create_guest_arrival_from_file(file_input)
            my_checkin.save()
            return my_checkin.room_key

        def guest_checkout(self, room_key:str)->bool:
            """manages the checkout of a guest"""
            stay_to_checkout = HotelStay.get_stay_from_roomkey(room_key)
            stay_to_checkout.check_out()
            return True

        def modify_reservation_date(self, file_input:str)->str:
            """manages the change of date of a reservation"""
            date_new_arr, reservation = HotelReservation.change_arrival_date(file_input)
            reservation.remove()
            reservation.arrival = date_new_arr
            return reservation.save()

    hotel_manager_instance = None

    def __new__(cls):
        if not HotelManager.hotel_manager_instance:
            HotelManager.hotel_manager_instance = HotelManager.__HotelManager()
        return HotelManager.hotel_manager_instance

    def __getattr__(self, item):
        return getattr(HotelManager.hotel_manager_instance, item)

    def __setattr__(self, key, value):
        return setattr(HotelManager.hotel_manager_instance,key,value)
