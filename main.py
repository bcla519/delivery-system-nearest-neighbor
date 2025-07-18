# Created by Brittany Clark, Student ID# 011384964
from import_data import *
from truck import Truck
from driver import Driver
from nearest_neighbor import nearest_neighbor
from datetime import time, datetime

# Load addresses, distances, and packages
address_dict = load_addresses('data_files/AddressList.csv')
distance_matrix = load_distance_matrix('data_files/DistanceMatrix.csv')
package_hash_table = load_package_data('data_files/PackageInfo.csv')

# Create the three trucks
# Packages in Truck 1 can start leaving at 8:00am
truck1 = Truck(1, 16, time(8, 0, 0))

# Packages in Truck 2 can start leaving at 9:05am due to some packages being delayed
truck2 = Truck(2, 16, time(9, 5, 0))

# Packages in Truck 3 can start leaving at 10:20am due to unknown address, but must wait for one truck to come back
truck3 = Truck(3, 16, time(10, 20, 0))

# Create the two drivers
driver1 = Driver(truck1)
driver2 = Driver(truck2)

# Manually load trucks with package IDs
truck1_packages = [15, 16, 34, 14, 19, 13, 39, 20, 21, 7, 29, 31, 4, 40]
for package_id in truck1_packages:
    package = package_hash_table.search(package_id)
    package.truck_num = truck1.truck_id
    truck1.add_package(package)

truck2_packages = [3, 18, 36, 38, 37, 5, 25, 26, 1, 6, 30]
for package_id in truck2_packages:
    package = package_hash_table.search(package_id)
    package.truck_num = truck2.truck_id
    truck2.add_package(package)

truck3_packages = [9, 8, 28, 27, 35, 32, 2, 33, 10, 11, 12, 17, 22, 23, 24]
for package_id in truck3_packages:
    package = package_hash_table.search(package_id)
    package.truck_num = truck3.truck_id
    truck3.add_package(package)

# Find and add delivery routes for Truck 1 & Truck 2
# Truck 3 must wait until 10:20am since Package 9 has the wrong address
delivery_route_truck1 = nearest_neighbor(truck1.packages, address_dict, distance_matrix)
truck1.add_delivery_route(delivery_route_truck1)

delivery_route_truck2 = nearest_neighbor(truck2.packages, address_dict, distance_matrix)
truck2.add_delivery_route(delivery_route_truck2)

# Set up new address for package #9
package9_new_address = Address('410 S State St', 'Salt Lake City', 'UT', '84111')
package9_old_address = Address('300 State St', 'Salt Lake City', 'UT', '84103')

# Run user interface
user_choice = None
while user_choice != '4':
    # Reset package status and delivery time
    for i in range(package_hash_table.num_elements):
        package = package_hash_table.search(i + 1)
        package.delivery_status = 'At the hub'
        package.delivery_time = None

        # Reset package 9 address to old address
        if (i + 1) == 9:
            package.address = package9_old_address

    # Reset drivers
    driver1.truck = truck1
    driver2.truck = truck2

    # Print menu options to screen
    print('WGUPS Menu Options:')
    print('1: Print all Package Statuses and Total Milage')
    print('2: Get a Single Package Status at a Specific Time')
    print('3: Get All Package Statuses at a Specific Time')
    print('4: Exit the Program')

    user_choice = input("Enter your choice: ")
    match user_choice:
        # Print all package statuses and total milage
        case '1':
            # Deliver packages for all trucks with EOD time of 9:00 pm (21:00:00)
            eod = time(21,0,0)
            driver1.truck.deliver_packages(eod)
            driver2.truck.deliver_packages(eod)

            # Find driver who is back first & update truck3's start time based on last truck's end time
            if driver1.truck.delivery_time < driver2.truck.delivery_time:
                former_truck_end_time = driver1.truck.delivery_time
                driver1.truck = truck3
                # Make sure truck 3 does not start before 10:20am
                if former_truck_end_time > truck3.start_time:
                    driver1.truck.start_time = former_truck_end_time

                # Update Package 9 address
                package9 = package_hash_table.search(9)
                package9.address = package9_new_address

                # Add delivery route with new package 9 address
                delivery_route_truck3 = nearest_neighbor(driver1.truck.packages, address_dict, distance_matrix)
                driver1.truck.add_delivery_route(delivery_route_truck3)

                # Deliver truck 3 packages
                driver1.truck.deliver_packages(eod)
            else:
                former_truck_end_time = driver2.truck.delivery_time
                driver2.truck = truck3
                # Make sure truck 3 does not start before 10:20am
                if former_truck_end_time > truck3.start_time:
                    driver2.truck.start_time = former_truck_end_time

                # Update Package 9 address
                package9 = package_hash_table.search(9)
                package9.address = package9_new_address

                # Add delivery route with new package 9 address
                delivery_route_truck3 = nearest_neighbor(driver2.truck.packages, address_dict, distance_matrix)
                driver2.truck.add_delivery_route(delivery_route_truck3)

                # Deliver truck 3 packages
                driver2.truck.deliver_packages(eod)

            # Print status of every package
            print('Package Status:')
            print('Package ID | Address | Delivery Deadline | Weight | Special Notes | '
                  'Delivery Status with Truck # (if en route) and Delivery Time (if delivered)')
            for i in range(package_hash_table.num_elements):
                package_hash_table.search(i + 1).print_status()

            # Print total milage for the trucks
            print()
            total_milage = truck1.total_milage + truck2.total_milage + truck3.total_milage
            print(f'Truck #{truck1.truck_id} Total Milage: {truck1.total_milage: .2f}')
            print(f'Truck #{truck2.truck_id} Total Milage: {truck2.total_milage: .2f}')
            print(f'Truck #{truck3.truck_id} Total Milage: {truck3.total_milage: .2f}')
            print(f'Total Milage for all trucks: {total_milage: .2f}')
            print()

        # Print single package status at a specific time
        case '2':
            # Prompt user for package and time
            package_id = int(input('Enter Package ID: '))
            specific_time = input('Enter Specific Time in the form HH:MM : ')

            # Look up package in package hash table
            package = package_hash_table.search(package_id)

            # Create time from user time
            specific_time = datetime.strptime(specific_time, '%H:%M').time()

            # Find truck with specified package
            if package in driver1.truck.packages: # Package in truck 1
                driver1.truck.deliver_packages(specific_time)
            elif package in driver2.truck.packages: # Package in truck 2
                driver2.truck.deliver_packages(specific_time)
            else: # Package in truck 3
                driver1.truck.deliver_packages(specific_time)
                driver2.truck.deliver_packages(specific_time)

                # Check if driver1 is back first and completed all package deliveries
                if driver1.truck.delivery_time < driver2.truck.delivery_time and driver1.truck.truck_status == 'At the hub':
                    former_truck_end_time = driver1.truck.delivery_time
                    driver1.truck = truck3
                    # Make sure truck 3 does not start before 10:20am
                    if former_truck_end_time > truck3.start_time:
                        driver1.truck.start_time = former_truck_end_time

                    # Update Package 9 address if specific time is 10:20am or after
                    if specific_time >= time(10,20):
                        package9 = package_hash_table.search(9)
                        package9.address = package9_new_address

                    # Add delivery route with new (or old based on time) package 9 address
                    delivery_route_truck3 = nearest_neighbor(driver1.truck.packages, address_dict, distance_matrix)
                    driver1.truck.add_delivery_route(delivery_route_truck3)

                    # Deliver truck 3 packages
                    driver1.truck.deliver_packages(specific_time)
                # Check if driver1 is back first and completed all package deliveries
                elif driver2.truck.delivery_time < driver1.truck.delivery_time and driver2.truck.truck_status == 'At the hub':
                    former_truck_end_time = driver2.truck.delivery_time
                    driver2.truck = truck3
                    # Make sure truck 3 does not start before 10:20am
                    if former_truck_end_time > truck3.start_time:
                        driver2.truck.start_time = former_truck_end_time

                    # Update Package 9 address if specific_time is 10:20am or after
                    if specific_time >= time(10,20):
                        package9 = package_hash_table.search(9)
                        package9.address = package9_new_address

                    # Add delivery route with new (or old address based on time) package 9 address
                    delivery_route_truck3 = nearest_neighbor(driver2.truck.packages, address_dict, distance_matrix)
                    driver2.truck.add_delivery_route(delivery_route_truck3)

                    # Deliver truck 3 packages
                    driver2.truck.deliver_packages(specific_time)

            # Print package status
            package.print_status()

        # Print all package statuses at a specific time
        case '3':
            # Prompt user for specific time
            specific_time = input('Enter Specific Time in the form HH:MM : ')

            # Change user string to time
            specific_time = datetime.strptime(specific_time, '%H:%M').time()

            # Start delivering packages in first two trucks
            driver1.truck.deliver_packages(specific_time)
            driver2.truck.deliver_packages(specific_time)

            # Check if driver1 is back first and completed all package deliveries
            if driver1.truck.delivery_time < driver2.truck.delivery_time and driver1.truck.truck_status == 'At the hub':
                former_truck_end_time = driver1.truck.delivery_time
                driver1.truck = truck3
                # Make sure truck 3 does not start before 10:20am
                if former_truck_end_time > truck3.start_time:
                    driver1.truck.start_time = former_truck_end_time

                # Update Package 9 address if specific time is 10:20am or after
                if specific_time >= time(10, 20):
                    package9 = package_hash_table.search(9)
                    package9.address = package9_new_address

                # Add delivery route with new (or old based on time) package 9 address
                delivery_route_truck3 = nearest_neighbor(driver1.truck.packages, address_dict, distance_matrix)
                driver1.truck.add_delivery_route(delivery_route_truck3)

                # Deliver truck 3 packages
                driver1.truck.deliver_packages(specific_time)
            # Check if driver1 is back first and completed all package deliveries
            elif driver2.truck.delivery_time < driver1.truck.delivery_time and driver2.truck.truck_status == 'At the hub':
                former_truck_end_time = driver2.truck.delivery_time
                driver2.truck = truck3
                # Make sure truck 3 does not start before 10:20am
                if former_truck_end_time > truck3.start_time:
                    driver2.truck.start_time = former_truck_end_time

                # Update Package 9 address if specific_time is 10:20am or after
                if specific_time >= time(10, 20):
                    package9 = package_hash_table.search(9)
                    package9.address = package9_new_address

                # Add delivery route with new (or old address based on time) package 9 address
                delivery_route_truck3 = nearest_neighbor(driver2.truck.packages, address_dict, distance_matrix)
                driver2.truck.add_delivery_route(delivery_route_truck3)

                # Deliver truck 3 packages
                driver2.truck.deliver_packages(specific_time)

            # Print status of every package
            print('Package Status:')
            print('Package ID | Address | Delivery Deadline | Weight | Special Notes | '
                  'Delivery Status with Truck # (if en route) and Delivery Time (if delivered)')
            for i in range(package_hash_table.num_elements):
                package_hash_table.search(i + 1).print_status()

        # Exit the Program
        case '4':
            print('Exiting the Program...')

        # Default case if user types invalid option
        case _:
            print('Invalid Choice')