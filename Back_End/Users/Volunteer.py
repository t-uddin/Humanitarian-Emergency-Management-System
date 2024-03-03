from Back_End.Users.User import User


class Volunteer(User):

    def __init__(self, __username, __password, __is_admin, __first_name, __last_name, __is_active,
                 __phone_number, __address, __camp_id, __availability):
        super().__init__(__username, __password, __is_admin, __first_name, __last_name)
        self.__is_active = __is_active
        self.__phone_number = __phone_number
        self.__address = __address
        self.__camp_id = __camp_id
        self.__availability = __availability

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, is_active):
        if is_active == "":
            raise ValueError("The is_active you entered is blank/empty")
        self.__is_active = is_active

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, phone_number):
        if phone_number == "":
            raise ValueError("The phone_number you entered is blank/empty")
        self.__phone_number = phone_number

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        if address == "":
            raise ValueError("The address you entered is blank/empty")
        self.__address = address

    @property
    def camp_id(self):
        return self.__camp_id

    @camp_id.setter
    def camp_id(self, camp_id):
        if camp_id == "":
            raise ValueError("The camp_id you entered is blank/empty")
        self.__camp_id = camp_id

    @property
    def availability(self):
        return self.__availability

    @availability.setter
    def availability(self, availability):
        if availability == "":
            raise ValueError("The availability you entered is blank/empty")
        self.__availability = availability
