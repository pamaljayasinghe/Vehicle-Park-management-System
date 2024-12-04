# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ztcx-4B3CXAj7Reur3Tkg8wDqMHZ2fHe
"""

class Vehicle:
    def __init__(self, vehicle_id, vehicle_type, license_plate):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.license_plate = license_plate

class ParkingLot:
    def __init__(self, capacity):
        self.capacity = capacity
        self.parking_slots = {}  # Dictionary to store parked vehicles by slot number

    def add_vehicle(self, vehicle):
        if len(self.parking_slots) < self.capacity:
            # Find an available parking slot
            for i in range(1, self.capacity + 1):
                if i not in self.parking_slots:
                    self.parking_slots[i] = vehicle
                    print(f"Vehicle {vehicle.license_plate} parked in slot {i}")
                    return
        else:
            print("Parking Lot is Full!")

    def remove_vehicle(self, vehicle_id):
        for slot, vehicle in self.parking_slots.items():
            if vehicle.vehicle_id == vehicle_id:
                del self.parking_slots[slot]
                print(f"Vehicle {vehicle.license_plate} removed from slot {slot}")
                return
        print("Vehicle not found!")

    def check_availability(self):
        available_slots = self.capacity - len(self.parking_slots)
        print(f"{available_slots} parking slots are available.")

    def display_parked_vehicles(self):
        if not self.parking_slots:
            print("No vehicles are currently parked.")
        else:
            print("Parked Vehicles:")
            for slot, vehicle in self.parking_slots.items():
                print(f"Slot {slot}: {vehicle.vehicle_type} - {vehicle.license_plate}")

    def search_vehicle_by_id(self, vehicle_id):
        for vehicle in self.parking_slots.values():
            if vehicle.vehicle_id == vehicle_id:
                print(f"Vehicle found: {vehicle.vehicle_type} - {vehicle.license_plate}")
                return
        print("Vehicle not found!")

def main():
    # Initialize a parking lot with 5 slots
    parking_lot = ParkingLot(5)

    # Add some vehicles to the parking lot
    vehicle1 = Vehicle(1, "Car", "ABC123")
    vehicle2 = Vehicle(2, "Truck", "XYZ456")
    vehicle3 = Vehicle(3, "Motorbike", "MNO789")
    vehicle4 = Vehicle(4, "Car", "PQR101")
    vehicle5 = Vehicle(5, "SUV", "LMN202")

    parking_lot.add_vehicle(vehicle1)
    parking_lot.add_vehicle(vehicle2)
    parking_lot.add_vehicle(vehicle3)
    parking_lot.add_vehicle(vehicle4)
    parking_lot.add_vehicle(vehicle5)

    # Try adding another vehicle (should print parking lot is full)
    vehicle6 = Vehicle(6, "Van", "STU303")
    parking_lot.add_vehicle(vehicle6)

    # Check availability
    parking_lot.check_availability()

    # Display parked vehicles
    parking_lot.display_parked_vehicles()

    # Search for a vehicle by ID
    parking_lot.search_vehicle_by_id(3)

    # Remove a vehicle
    parking_lot.remove_vehicle(2)

    # Check availability again
    parking_lot.check_availability()

    # Display parked vehicles after removal
    parking_lot.display_parked_vehicles()

if __name__ == "__main__":
    main()