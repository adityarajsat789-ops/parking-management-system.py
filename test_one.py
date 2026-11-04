"""Basic automated tests for the Parking Management System."""

import tempfile
import unittest
from pathlib import Path

from one import ParkingLot


class ParkingManagementTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "parking.txt"
        self.lot = ParkingLot(self.data_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_car_entry_uses_first_slot(self):
        result = self.lot.entry("MH12AB1234", "car")
        self.assertIn("parked in slot 1", result)
        self.assertEqual(self.lot.free_slots(), 4)

    def test_half_hour_car_exit_charges_one_hour(self):
        self.lot.entry("MH12AB1234", "car")
        result = self.lot.exit_vehicle("MH12AB1234", 0.5)
        self.assertIn("Hours charged: 1", result)
        self.assertIn("Fee: Rs. 20", result)
        self.assertEqual(self.lot.free_slots(), 5)

    def test_duplicate_invalid_type_and_unknown_exit(self):
        self.lot.entry("MH12AB1234", "car")
        self.assertEqual(
            self.lot.entry("MH12AB1234", "car"),
            "Vehicle MH12AB1234 is already parked.",
        )
        self.assertEqual(
            self.lot.entry("XX00XX0001", "truck"),
            "Invalid type. Enter car or bike.",
        )
        self.assertEqual(
            self.lot.exit_vehicle("XX00XX0000", 1),
            "Vehicle XX00XX0000 not found.",
        )

    def test_bike_exit_rounds_up_and_status_is_empty(self):
        self.lot.entry("KA01AB1111", "bike")
        result = self.lot.exit_vehicle("KA01AB1111", 2.5)
        self.assertIn("Hours charged: 3", result)
        self.assertIn("Fee: Rs. 30", result)
        self.assertIn("Slots free: 5 of 5", self.lot.status())

    def test_full_lot_rejects_sixth_vehicle(self):
        for number in range(5):
            self.lot.entry(f"CG00AA000{number}", "car")
        self.assertEqual(self.lot.free_slots(), 0)
        self.assertEqual(self.lot.entry("CG00AA0099", "bike"), "Parking lot is full.")

    def test_data_persists_after_restart(self):
        self.lot.entry("DL01AB1234", "bike")
        loaded_lot = ParkingLot(self.data_file)
        self.assertIn("DL01AB1234", loaded_lot.status())
        self.assertEqual(loaded_lot.free_slots(), 4)

    def test_invalid_hours_do_not_remove_vehicle(self):
        self.lot.entry("MH12AB1234", "car")
        result = self.lot.exit_vehicle("MH12AB1234", "not-a-number")
        self.assertIn("Invalid hours", result)
        self.assertEqual(self.lot.free_slots(), 4)


if __name__ == "__main__":
    unittest.main()
