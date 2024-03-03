class User:
    def __init__(self, __username, __password, __is_admin, __first_name , __last_name):
        self.__username = __username
        self.__password = __password
        self.__is_admin = __is_admin
        self.__first_name = __first_name
        self.__last_name = __last_name

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        if username == "":
            raise ValueError("The username you entered is blank/empty")
        self.__username = username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        if password == "":
            raise ValueError("The password you entered is blank/empty")
        self.__password = password

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, is_admin):
        if is_admin != 0 or is_admin != 1:
            raise ValueError("The is_admin you entered is invalid")
        self.__is_admin = is_admin

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name):
        if first_name == '':
            raise ValueError("The first name cannot be empty")
        self.first_name = first_name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        if last_name == '':
            raise ValueError("The last name cannot be empty")
        self.last_name = last_name