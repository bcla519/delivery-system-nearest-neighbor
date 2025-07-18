class Address:
    # Address Constructor
    def __init__(self, street, city, state, zip_code, id=None):
        self.id = id
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code

    # Overload str formatting for Address class
    # Will print Address in form: street address, city, state zip_code
    def __str__(self):
        return "{0}, {1}, {2} {3}".format(self.street, self.city, self.state, self.zip_code)