"""Class for testing Sigleton classess"""
#pylint: skip-file
from unittest import TestCase
from uc3m_travel.hotel_manager import HotelManager
from uc3m_travel.storage.reservation_json_store import ReservationJsonStore
from uc3m_travel.storage.stay_json_store import StayJsonStore
from uc3m_travel.storage.checkout_json_store import CheckoutJsonStore

class TestHotelManager(TestCase):
    """Class for testing the singletons"""
    def test_singleton_hotel_manager(self):
        """Testing the singleton for Hotel+Manager"""
        instance1 = HotelManager()
        instance2 = HotelManager()
        instance3 = HotelManager()
        self.assertEqual(instance1,instance2)
        self.assertEqual(instance1, instance3)
        self.assertEqual(instance3, instance2)

    def test_singleton_reservation_json_store(self):
        """Testing the singleton for Hotel+Manager"""
        instance1 = ReservationJsonStore()
        instance2 = ReservationJsonStore()
        instance3 = ReservationJsonStore()
        self.assertEqual(instance1,instance2)
        self.assertEqual(instance1, instance3)
        self.assertEqual(instance2, instance3)

    def test_singleton_stay_json_store(self):
        """Testing the singleton for Hotel+Manager"""
        instance1 = StayJsonStore()
        instance2 = StayJsonStore()
        instance3 = StayJsonStore()
        self.assertEqual(instance1,instance2)
        self.assertEqual(instance1, instance3)
        self.assertEqual(instance2, instance3)

    def test_singleton_checkout_json_store(self):
        """Testing the singleton for Hotel+Manager"""
        instance1 = CheckoutJsonStore()
        instance2 = CheckoutJsonStore()
        instance3 = CheckoutJsonStore()
        self.assertEqual(instance1,instance2)
        self.assertEqual(instance1, instance3)
        self.assertEqual(instance2, instance3)