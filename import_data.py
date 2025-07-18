from address import Address
from chaining_hash_table import ChainingHashTable
import csv
from package import Package

# Load package data from package.csv
# Code obtained from Course Tips, C950 Webinar-2
def load_package_data(filename):
    # Create new hash table to return
    hash_table = ChainingHashTable()

    # Read in package info
    with open(filename) as packages:
        packages_data = csv.reader(packages, delimiter=',')
        for package in packages_data:
            pID = int(package[0])
            pStreetAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipCode = package[4]
            pDeliveryDeadline = package[5]
            pWeight = int(package[6])
            pSpecialNotes = package[7]

            # Create new Address
            package_address = Address(pStreetAddress, pCity, pState, pZipCode)
            # Create new Package
            new_package = Package(pID, package_address, pDeliveryDeadline, pWeight, pSpecialNotes)

            # Add Package to hash table
            hash_table.insert(pID, new_package)

    # Return filled hash table
    return hash_table

# Load addresses for distance table
def load_addresses(filename):
    # Create address dictionary
    # (street address, Address object)
    address_dict = {}

    # Index of address from file
    address_num = 0

    # Read in address info
    with open(filename) as addresses:
        addresses_data = csv.reader(addresses, delimiter=',')
        for address in addresses_data:
            street_address = address[0]
            city = address[1]
            state = address[2]
            zip_code = address[3]

            # Create new Address
            new_address = Address(street_address, city, state, zip_code, address_num)
            # Add new Address to address dictionary
            address_dict[street_address] = new_address

            # Increment address_num
            address_num += 1

    # Return address list
    return address_dict

# Load distance matrix
def load_distance_matrix(filename):
    # Create distance matrix
    distance_matrix = []

    # Load distances
    with open(filename) as distances:
        distances_data = csv.reader(distances, delimiter=',')

        for distance_row in distances_data:
            # Add row of distances to distance matrix
            distance_matrix.append(distance_row)

    # Return filled distance matrix
    return distance_matrix