class Package:
    # Package Constructor
    def __init__(self, package_id, address, delivery_deadline, weight, special_notes, delivery_status='At the hub', delivery_time=None):
        self.package_id = package_id
        self.address = address
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.special_notes = special_notes
        self.delivery_status = delivery_status
        self.delivery_time = delivery_time
        self.truck_num = None

    # Print all elements of the package for UI
    def print_status(self):
        if self.delivery_status == 'At the hub':
            print(f'{self.package_id} | {self.address} | {self.delivery_deadline} | '
                  f'{self.weight} | {self.special_notes} | {self.delivery_status}')
        elif self.delivery_status == 'En route':
            print(f'{self.package_id} | {self.address} | {self.delivery_deadline} | '
                  f'{self.weight} | {self.special_notes} | {self.delivery_status} on Truck #{self.truck_num}')
        else:
            print(f'{self.package_id} | {self.address} | {self.delivery_deadline} | '
                  f'{self.weight} | {self.special_notes} | '
                  f'{self.delivery_status} by Truck #{self.truck_num} at {self.delivery_time:%H:%M:%S}')
