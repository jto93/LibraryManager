#Patron class

class Patron:
    total_number = 0
    id_counter = 0

    def __init__(self, first, last): 
        Patron.add_patron()
        self.first = first
        self.last = last
        self.id = Patron.id_counter

#Class Methods

    @classmethod
    def number_of_patrons(cls):
        return cls.total_number

    @classmethod
    def add_patron(cls): 
        cls.total_number += 1
        cls.id_counter += 1

    @classmethod
    def remove_patron(cls):
        cls.total_number -= 1

#Get Methods

    def get_first_name(self):
        return self.first

    def get_last_name(self):
        return self.last

    