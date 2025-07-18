# Hash table with chaining class
# Code obtained from Course Tips, C950 Webinar-1
class ChainingHashTable:
    # Constructor with optional initial capacity parameter
    # Assigns all buckets with an empty list
    def __init__(self, initial_capacity=10):
        # Initialize the hash table with empty bucket list entries
        self.table = []
        self.num_elements = 0
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new key, item into the hash table
    # If key already exists, item is updated
    def insert(self, key, item):
        # Get the bucket list where this item will go
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Update key if it is already in the bucket
        for key_value in bucket_list:
            if key_value[0] == key:
                key_value[1] = item
                return True

        # If not, key, item appended to end of the bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        self.num_elements += 1
        return True

    # Searches for an item with matching key in the hash table
    # Returns the item if found, or None is not found
    def search(self, key):
        # Get the bucket list where this key would be
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Search for the key in the bucket list
        for key_value in bucket_list:
            # Key found
            if key_value[0] == key:
                return key_value[1]

        # Key not found
        return None

    # Removes an item with matching key from the hash table
    def remove(self, key):
        # Get bucket list where this item will be removed from
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Remove the item from the bucket list if it is present
        for key_value in bucket_list:
            if key_value[0] == key:
                bucket_list.remove([key_value[0], key_value[1]])

    # Print hash table
    def print(self):
        for bucket in self.table:
            for key_value in bucket:
                print(f"{key_value[0]}, Package ID: {key_value[1].package_id} | ", end="")
            print()