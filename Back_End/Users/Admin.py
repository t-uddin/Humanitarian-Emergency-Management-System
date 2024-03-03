from Back_End.Users.User import User

class Admin(User):

    def __init__(self, __username, __password, __is_admin):
        super().__init__(__username, __password, __is_admin)
