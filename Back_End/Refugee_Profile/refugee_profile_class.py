class RefugeeProfile:
    def __init__(self, __id, __first_name, __last_name, __camp_id, __family_size, __med_con):
        self.__id = __id
        self.__first_name = __first_name.title()  # lead family member only
        self.__last_name = __last_name.title()  # lead family member only
        self.__camp_id = __camp_id
        self.__family_size = int(__family_size)  # family size, in numbers, including the family lead
        self.__med_con = __med_con
    
    @property
    def id(self):
        return self.__id

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def camp_id(self):
        return self.__camp_id

    @property
    def family_size(self):
        return self.__family_size
        
    @property
    def med_con(self):
        return self.__med_con

    # Setters

    @first_name.setter
    def first_name(self, first_name):
        if first_name == "":
            raise ValueError("This field cannot be empty")
        self.__first_name = first_name

    @last_name.setter
    def last_name(self, last_name):
        if last_name == "":
            raise ValueError("This field cannot be empty")
        self.__last_name = last_name
    
    @camp_id.setter
    def camp_id(self, camp_id):
        if camp_id == 0:  # will change to: if camp_id != existing camps, then etc.
            raise ValueError("The camp ID you entered does not exist")
        self.__camp_id = camp_id

    @family_size.setter
    def family_size(self, family_size):
        if family_size <= 0:
            raise ValueError("Family size must be greater than 0")
        self.__family_size = family_size  
        
    @med_con.setter
    def med_con(self, med_con):
        if med_con == "": 
            raise ValueError("Please enter a recognised medical condition")
        self.__med_con = med_con
