def nearest_neighbor(packages, address_dict, distance_matrix):
    num_packages = len(packages)
    undelivered_packages = packages[:]

    # Create empty lists
    delivery_route = []
    visited_locations = []

    # Set starting location to HUB
    hub = '4001 South 700 East'
    current_location = address_dict[hub]

    # Loop through packages until all packages are delivered
    while len(visited_locations) < num_packages:
        min_distance = float('inf')
        min_location_package = packages[0]

        # Find minimum distance from current location to next package delivery
        for package in undelivered_packages:
            # Find address indexes for current_location and package
            current_location_index = address_dict[current_location.street].id
            package_index = address_dict[package.address.street].id

            # Find distance between two addresses
            if current_location_index < package_index:
                distance = float(distance_matrix[package_index][current_location_index])
            else:
                distance = float(distance_matrix[current_location_index][package_index])

            # Check distance against min_distance
            if distance < min_distance:
                min_distance = distance
                min_location_package = package

        # Update current location
        current_location = min_location_package.address

        # Add next package to visited_locations
        visited_locations.append(current_location)

        # Add list [package, distance to delivery address] to delivery_route
        delivery_route.append([min_location_package, min_distance])

        # Remove delivered package from packages
        undelivered_packages.remove(min_location_package)

    # Add return route back to HUB
    last_visited_location = visited_locations[-1]
    delivery_route.append([None, float(distance_matrix[address_dict[last_visited_location.street].id][0])])

    # Return completed delivery route
    return delivery_route