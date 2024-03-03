from Back_End.Users.UserController import UserController
from Back_End.Users.Volunteer import Volunteer

class VolunteerController(UserController):

    def __init__(self, connection):
        super().__init__(connection)

    def initialise(self):
        c = self.connection.cursor()
        c.execute("SELECT * FROM users WHERE is_admin = 0")

        data = c.fetchall()
        volunteers = []

        for volunteer in data:
            volunteer_object = Volunteer(volunteer[0], volunteer[1], volunteer[2], volunteer[3],
                                         volunteer[4], volunteer[5], volunteer[6], volunteer[7],
                                         volunteer[8], volunteer[9])
            if self.__is_valid(volunteer_object):
                volunteers.append(volunteer_object)
        
        return volunteers

    def get_number_volunteers_by_camp(self, camp_id):
        c = self.connection.cursor()
        query = "SELECT * FROM users WHERE camp_id = ?"
        c.execute(query, [camp_id])
        result = c.fetchall()
        total = len(result)
        return total
    
    def get_volunteer_details(self, username):
        c = self.connection.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}'"
        c.execute(query)
        volunteer = c.fetchall()[0]

        volunteer_object = Volunteer(volunteer[0], volunteer[1], volunteer[2], volunteer[3],
                                        volunteer[4], volunteer[5], volunteer[6], volunteer[7],
                                     volunteer[8], volunteer[9])
    
        return volunteer_object

    def __is_valid(self, volunteer):
        return (volunteer.username != "" and not (len(volunteer.availability) != 7 or 
        any(c not in 'TF' for c in volunteer.availability)))

    # Public methods to add, remove and edit volunteer object
    def add_volunteer(self, volunteer):
        if self.__is_valid(volunteer):
            if self.get_user(volunteer.username) == None:
                self.__add_volunteer_to_database(volunteer)
                return True
            else:
                return(
                    "An account with this username already exists. Please insert a different username!")
        else:
            return("Error: unable to add volunteer due to invalid inputs")

    def remove_volunteer(self, volunteer):
        if self.__is_valid(volunteer):
            self.__remove_volunteer_from_database(volunteer)
            return True
        else:
            return ("Error: unable to remove volunteer")

    def update_volunteer(self, volunteer):
        if self.__is_valid(volunteer):
            self.__edit_volunteer_details(volunteer)
            return True
        else:
            return("Error: unable to update volunteer due to invalid inputs")

    # Private methods to add, remove and edit volunteer object
    def __add_volunteer_to_database(self, volunteer):
        try:
            cursor = self.connection.cursor()
            query = f"INSERT INTO users VALUES(\
                        '{volunteer.username}', \
                        '{self.password_hash_function(volunteer.password)}', \
                        '{volunteer.is_admin}', \
                        '{volunteer.first_name}', \
                        '{volunteer.last_name}', \
                        '{volunteer.is_active}', \
                        '{volunteer.phone_number}', \
                        '{volunteer.address}', \
                        '{volunteer.camp_id}', \
                        '{volunteer.availability}' \
                     )"
            result = cursor.execute(query)
            self.connection.commit()
            return result
        except Exception as e:
            return None

    def __remove_volunteer_from_database(self, volunteer):
        try:
            cursor = self.connection.cursor()
            query = f"DELETE FROM users where username = '{volunteer.username}'"
            cursor.execute(query)
            self.connection.commit()

            return True
        except Exception as e:
            return False

    def __edit_volunteer_details(self, volunteer):
        try:
            cursor = self.connection.cursor()
            query = f"UPDATE users SET \
                        username = '{volunteer.username}', \
                        is_active =  {volunteer.is_active}, \
                        first_name = '{volunteer.first_name}', \
                        last_name = '{volunteer.last_name}', \
                        phone_number = '{volunteer.phone_number}', \
                        camp_id = '{volunteer.camp_id}', \
                        address = '{volunteer.address}',\
                        availability = '{volunteer.availability}' \
                        WHERE username = '{volunteer.username}'"
            cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            return

    def update_volunteer_activity(self, volunteer):
        try:
            cursor = self.connection.cursor()

            if volunteer.is_active == 1:
                active_status = 1
            elif volunteer.is_active == 0:
                active_status = 0

            query = f"UPDATE users SET is_active = '{active_status}' \
                    WHERE username = '{volunteer.username}'"
            cursor.execute(query)
            self.connection.commit()
            return True
        except Exception as e:
            return False

    def deactivate(self, username):
        c = self.connection.cursor()
        c.execute(f"UPDATE users SET is_active = 0 WHERE username = '{username}'")
        self.connection.commit()
        return True

    def activate(self,username):
        c = self.connection.cursor()
        c.execute(f"UPDATE users SET is_active = 1 WHERE username = '{username}'")
        self.connection.commit()
        return True
