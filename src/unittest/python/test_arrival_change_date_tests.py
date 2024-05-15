"""Module for testing guest_arrival_change_date"""
#pylint: skip-file
from unittest import TestCase
import os
import hashlib
import json
from freezegun import freeze_time
from uc3m_travel import HotelManager
from uc3m_travel import HotelManagementException
from uc3m_travel import JSON_FILES_PATH
from uc3m_travel import JSON_FILES_GUEST_ARRIVAL
from uc3m_travel.cfg.hotel_management_config import JSON_FILES_ARRIVAL_DATE_CHANGE


class TestArrivalChangeDate(TestCase):
    """Class for testing guest_arrival_change_date"""
    @freeze_time("2023-03-08")
    def setUp(self):
        """first prepare the stores"""
        store_reservation = JSON_FILES_PATH + "store_reservation.json"


        if os.path.isfile(store_reservation):
            os.remove(store_reservation)

        my_manager = HotelManager()
        # add an order in the store
        file_test = JSON_FILES_GUEST_ARRIVAL + "key_ok.json"
        ##insert the reservation
        with freeze_time("2024/03/22 13:00:00"):
            hotel_mngr = HotelManager()
            #first reservation for valid
            localizer = hotel_mngr.room_reservation(credit_card="5105105105105100",
                                                    name_surname="JOSE LOPEZ",
                                                    id_card="12345678Z",
                                                    phone_number="+341234567",
                                                    room_type="SINGLE",
                                                    arrival_date="01/07/2024",
                                                    num_days=1)
            self.assertEqual(localizer, "450a53be9b39944e62e7164ca5f5aadf")



    @freeze_time("2024-07-02")
    def test_change_arrival_date_ok(self):
        my_manager = HotelManager()
        file_test = JSON_FILES_ARRIVAL_DATE_CHANGE + "key_ok.json"

        value = my_manager.modify_reservation_date(file_test)
        self.assertTrue(value)
