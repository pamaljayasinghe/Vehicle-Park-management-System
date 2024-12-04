# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ztcx-4B3CXAj7Reur3Tkg8wDqMHZ2fHe
"""

import sqlite3
from datetime import datetime, timedelta

class Vehicle:
    def __init__(self, vehicle_id, vehicle_type, license_plate):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.license_plate = license_plate
        self.entry_time = datetime.now()

class ParkingLot:
    def __init__(self, db_name="parking_lot.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create the parking lot table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS parking_lot (
                vehicle_id INTEGER PRIMARY KEY,
                vehicle_type TEXT,
                license_plate TEXT,
                entry_time TEXT,
                exit_time TEXT,
                fee REAL
            )
        ''')
        self.conn.commit()

    def add_vehicle(self, vehicle):
        """Add a new vehicle to the parking lot."""
        entry_time = vehicle.entry_time.strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
            INSERT INTO parking_lot (vehicle_id, vehicle_type, license_plate, entry_time, exit_time, fee)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (vehicle.vehicle_id, vehicle.vehicle_type, vehicle.license_plate, entry_time, None, 0))
        self.conn.commit()
        print(f"Vehicle {vehicle.license_plate} entered the parking lot.")

    def remove_vehicle(self, vehicle_id):
        """Remove a vehicle from the parking lot and calculate the fee."""
        exit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
            UPDATE parking_lot
            SET exit_time = ?, fee = ?
            WHERE vehicle_id = ? AND exit_time IS NULL
        ''', (exit_time, self.calculate_fee(vehicle_id), vehicle_id))
        self.conn.commit()
        print(f"Vehicle {vehicle_id} left the parking lot.")

    def calculate_fee(self, vehicle_id):
        """Calculate parking fee based on the duration."""
        self.cursor.execute('''
            SELECT entry_time FROM parking_lot WHERE vehicle_id = ? AND exit_time IS NULL
        ''', (vehicle_id,))
        entry_time = self.cursor.fetchone()[0]
        entry_time = datetime.strptime(entry_time, '%Y-%m-%d %H:%M:%S')
        duration = datetime.now() - entry_time
        # Assuming $2 per hour parking fee
        return round(duration.total_seconds() / 3600 * 2, 2)

    def check_availability(self):
        """Check the number of parked vehicles."""
        self.cursor.execute('''
            SELECT COUNT(*) FROM parking_lot WHERE exit_time IS NULL
        ''')
        occupied_slots = self.cursor.fetchone()[0]
        print(f"Parking Lot: {occupied_slots} vehicle(s) currently parked.")

    def display_parked_vehicles(self):
        """Display all currently parked vehicles."""
        self.cursor.execute('''
            SELECT vehicle_id, vehicle_type, license_plate, entry_time FROM parking_lot WHERE exit_time IS NULL
        ''')
        parked_vehicles = self.cursor.fetchall()
        if not parked_vehicles:
            print("No vehicles are currently parked.")
        else:
            print("Currently Parked Vehicles:")
            for vehicle in parked_vehicles:
                print(f"ID: {vehicle[0]}, Type: {vehicle[1]}, Plate: {vehicle[2]}, Entry Time: {vehicle[3]}")

    def search_vehicle_by_id(self, vehicle_id):
        """Search for a vehicle by its ID."""
        self.cursor.execute('''
            SELECT * FROM parking_lot WHERE vehicle_id = ?
        ''', (vehicle_id,))
        vehicle = self.cursor.fetchone()
        if vehicle:
            print(f"Vehicle ID: {vehicle[0]}, Type: {vehicle[1]}, Plate: {vehicle[2]}, Entry: {vehicle[4]}")
        else:
            print("Vehicle not found.")

    def generate_report(self):
        """Generate a parking lot report (e.g., total fee, total parked vehicles)."""
        self.cursor.execute('''
            SELECT vehicle_type, SUM(fee) FROM parking_lot WHERE exit_time IS NOT NULL GROUP BY vehicle_type
        ''')
        report = self.cursor.fetchall()
        print("Parking Fee Report:")
        for row in report:
            print(f"Vehicle Type: {row[0]}, Total Fee Collected: ${row[1]:.2f}")

    def close(self):
        """Close the database connection."""
        self.conn.close()

def main():
    # Initialize the parking lot system
    parking_lot = ParkingLot()

    # Add some vehicles
    vehicle1 = Vehicle(1, "Car", "ABC123")
    vehicle2 = Vehicle(2, "Truck", "XYZ456")
    vehicle3 = Vehicle(3, "Motorbike", "MNO789")

    parking_lot.add_vehicle(vehicle1)
    parking_lot.add_vehicle(vehicle2)
    parking_lot.add_vehicle(vehicle3)

    # Check availability
    parking_lot.check_availability()

    # Display parked vehicles
    parking_lot.display_parked_vehicles()

    # Simulate vehicle leaving after some time
    parking_lot.remove_vehicle(1)

    # Check availability again
    parking_lot.check_availability()

    # Search for a vehicle by ID
    parking_lot.search_vehicle_by_id(2)

    # Generate a report
    parking_lot.generate_report()

    # Close the database connection
    parking_lot.close()

if __name__ == "__main__":
    main()