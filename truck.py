from datetime import datetime, time, timedelta

class Truck:
    # Truck Constructor
    def __init__(self, truck_id, capacity=0, start_time=time(8,0,0),  average_speed=18):
        self.truck_id = truck_id
        self.truck_status = 'At the hub'
        self.capacity = capacity
        self.average_speed = average_speed
        self.packages = []
        self.delivery_route = []
        self.start_time = start_time
        self.delivery_time = start_time
        self.total_milage = 0.0

    # Add package to packages list
    def add_package(self, package):
        self.packages.append(package)

    # Add delivery route
    def add_delivery_route(self, delivery_route):
        self.delivery_route = delivery_route[:]

    # Deliver packages for delivery route up to specific time or until delivery route it completed
    def deliver_packages(self, time):
        # Reset truck from HUB
        self.truck_status = 'At the hub'
        self.delivery_time = self.start_time
        self.total_milage = 0.0

        # Update all package statuses to en route in truck if start_time < time
        if self.start_time <= time:
            self.truck_status = 'Out on delivery'
            for package in self.packages:
                package.delivery_status = 'En route'

        # Update package status and delivery time as packages are delivered
        for package_distance in self.delivery_route:
            # Separate package and distance from package_distance list
            package = package_distance[0]
            distance = package_distance[1]

            # Calculate new delivery time for next package
            hours_traveled = distance / self.average_speed
            temp_dt = datetime.combine(datetime.today(), self.delivery_time) + timedelta(hours=hours_traveled)

            # If delivery time is before specific time, delivery next package
            if temp_dt.time() < time:
                # Add distance to total milage for the truck
                self.total_milage += distance

                # Update delivery time based on distance of current package
                self.delivery_time = temp_dt.time()

                # Check if delivering package
                # If package == None, truck is returning to HUB
                if package != None:
                    # Update package status as delivered
                    package.delivery_status = 'Delivered'

                    # Update package delivery time to current truck time
                    package.delivery_time = self.delivery_time

                # Last 'package' is truck returning to HUB
                # Update truck status to report back at the HUB
                if package == None:
                    self.truck_status = 'At the hub'
            else: # Next delivery time is after specific time, stop delivering packages
                break