"""Parking Management System - PS 47
Python 3 | Console application
"""

import json
import math
from pathlib import Path

TOTAL_SLOTS = 5
RATES = {"car": 20, "bike": 10}
DATA_FILE = Path(__file__).with_name("parking.txt")


class ParkingLot:
    """Manage five parking slots and persist parked-vehicle records."""

    def __init__(self, data_file=DATA_FILE):
        self.data_file = Path(data_file)
        self.slots = [None] * TOTAL_SLOTS
        self.load_data()

    def load_data(self):
        """Load saved slot data; start with an empty lot if no data exists."""
        if not self.data_file.exists():
            return
        try:
            data = json.loads(self.data_file.read_text(encoding="utf-8"))
            saved_slots = data.get("slots", [])
            if len(saved_slots) != TOTAL_SLOTS:
                raise ValueError("Invalid slot count in parking data.")
            for index, vehicle in enumerate(saved_slots):
                if vehicle is not None:
                    number = vehicle.get("number")
                    vehicle_type = vehicle.get("type")
                    if not number or vehicle_type not in RATES:
                        raise ValueError("Invalid vehicle record in parking data.")
                    self.slots[index] = {
                        "number": str(number).strip().upper(),
                        "type": vehicle_type,
                    }
        except (OSError, json.JSONDecodeError, AttributeError, TypeError, ValueError):
            print("Warning: parking.txt could not be read. Starting with an empty lot.")
            self.slots = [None] * TOTAL_SLOTS

    def save_data(self):
        """Save the current parking slots after every successful change."""
        data = {"slots": self.slots}
        self.data_file.write_text(json.dumps(data, indent=4), encoding="utf-8")

    @staticmethod
    def validate_vehicle_number(number):
        number = number.strip().upper()
        if not number or any(character.isspace() for character in number):
            raise ValueError("Vehicle number cannot be empty or contain spaces.")
        return number

    def entry(self, vehicle_number, vehicle_type):
        """Park a car or bike in the first available slot."""
        try:
            number = self.validate_vehicle_number(vehicle_number)
        except ValueError as error:
            return str(error)

        kind = vehicle_type.strip().lower()
        if kind not in RATES:
            return "Invalid type. Enter car or bike."

        if any(vehicle and vehicle["number"] == number for vehicle in self.slots):
            return f"Vehicle {number} is already parked."

        for index, vehicle in enumerate(self.slots):
            if vehicle is None:
                self.slots[index] = {"number": number, "type": kind}
                self.save_data()
                return (
                    f"Vehicle {number} parked in slot {index + 1}.\n"
                    f"Slots free: {self.free_slots()}"
                )

        return "Parking lot is full."

    @staticmethod
    def calculate_fee(vehicle_type, hours):
        """Round parking time up to a whole hour; minimum one hour."""
        kind = vehicle_type.strip().lower()
        if kind not in RATES:
            raise ValueError("Invalid type. Enter car or bike.")
        try:
            duration = float(hours)
        except (TypeError, ValueError):
            raise ValueError("Invalid hours. Enter a positive number.") from None
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError("Invalid hours. Enter a positive number.")
        charged_hours = max(1, math.ceil(duration))
        return charged_hours, charged_hours * RATES[kind]

    def exit_vehicle(self, vehicle_number, hours):
        """Remove a parked vehicle and calculate its parking fee."""
        try:
            number = self.validate_vehicle_number(vehicle_number)
        except ValueError as error:
            return str(error)

        for index, vehicle in enumerate(self.slots):
            if vehicle is not None and vehicle["number"] == number:
                try:
                    charged_hours, fee = self.calculate_fee(vehicle["type"], hours)
                except ValueError as error:
                    return str(error)

                self.slots[index] = None
                self.save_data()
                return (
                    f"Vehicle {number} exited from slot {index + 1}.\n"
                    f"Hours charged: {charged_hours}\n"
                    f"Fee: Rs. {fee}\n"
                    f"Slot {index + 1} is now free."
                )

        return f"Vehicle {number} not found."

    def free_slots(self):
        return sum(vehicle is None for vehicle in self.slots)

    def status(self):
        """Display occupied and free parking slots."""
        lines = ["Parking Status:"]
        for index, vehicle in enumerate(self.slots, start=1):
            if vehicle is None:
                lines.append(f"Slot {index}: Free")
            else:
                lines.append(
                    f"Slot {index}: {vehicle['number']} ({vehicle['type']})"
                )
        lines.append(f"Slots free: {self.free_slots()} of {TOTAL_SLOTS}")
        return "\n".join(lines)



# Required problem-statement functions
def entry(parking_lot, vehicle_number, vehicle_type):
    return parking_lot.entry(vehicle_number, vehicle_type)


def exit_vehicle(parking_lot, vehicle_number, hours):
    return parking_lot.exit_vehicle(vehicle_number, hours)


def calculate_fee(vehicle_type, hours):
    return ParkingLot.calculate_fee(vehicle_type, hours)


def status(parking_lot):
    return parking_lot.status()


def main():
    parking_lot = ParkingLot()

    while True:
        print("\n===== PARKING MANAGEMENT SYSTEM =====")
        print("1. Entry")
        print("2. Exit")
        print("3. Status")
        print("4. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            number = input("Enter vehicle number: ")
            vehicle_type = input("Enter vehicle type (car/bike): ")
            print(entry(parking_lot, number, vehicle_type))
        elif choice == "2":
            number = input("Enter vehicle number: ")
            hours = input("Enter parking hours: ")
            print(exit_vehicle(parking_lot, number, hours))
        elif choice == "3":
            print(status(parking_lot))
        elif choice == "4":
            print("Thank you for using the Parking Management System.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
