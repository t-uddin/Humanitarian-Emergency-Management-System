from Back_End.Camps.Camps import Camps
from Back_End.Refugee_Profile.refugee_profile_controller import RefugeeProfileController
from Back_End.Users.VolunteerController import VolunteerController
from Back_End.Maps.maps import MapsController

class CampsController:
    def __init__(self, connection):
        self.__connection = connection
        self.__refugee_controller = RefugeeProfileController(connection)
        self.__volunteer_controller = VolunteerController(connection)
        self.__maps_controller = MapsController(connection)

    # creates camp objects using data in the database, returns list of all camps as objects
    def initialise(self):
        c = self.__connection.cursor()
        c.execute("SELECT * FROM camps")

        data = c.fetchall()
        camps = []

        for camp in data:
            camp_object = Camps(camp[0], camp[2], camp[1], camp[3], camp[4], camp[5])
            if self.__is_valid(camp_object):
                camps.append(camp_object)
        return camps

    # saves camp to database if the camp object is valid, prints message if object is not valid
    def save(self, camp):
        if self.__is_valid(camp):
            self.__add_camp_to_database(camp)
            self.__maps_controller.generate_latlong(camp.location, self.get_latest_camp_id())

            return True
        else:
            return "Camp not saved, values inputted have an error, please ensure that all fields are valid"

    # gets id of the most recently added camp
    def get_latest_camp_id(self):
        try:
            c = self.__connection.cursor()
            sql = f"SELECT camp_id FROM camps ORDER BY camp_id DESC LIMIT 1"
            c.execute(sql)
            self.__connection.commit()
            return c.fetchone()[0]
        except Exception as e:
            print(f"The exception/error is: {e}")
            return False

    # only deletes a camp if it has no volunteers and no refugees and it is in the database
    def delete_camp(self,camp):
        if self.__refugee_controller.number_of_refugees_by_camp(camp.id) == 0 and \
                self.__volunteer_controller.get_number_volunteers_by_camp(camp.id) == 0 \
        and self.does_camp_exist(camp.id):
            self.__remove_camp_from_database(camp)
            self.__maps_controller.remove_address(camp.id)
            return True
        else:
            return "Camps have not been deleted as there are still volunteers or refugees assigned."

    #checking that the name,id and location functions in the camp object are valid, returns true if camp object is valid
    def __is_valid(self,camp):
        if camp.name != "" and camp.id != 0 and camp.location != "" and camp.capacity >= 0 and \
        camp.medicine >= 0 and camp.food >= 0:
           return True
        return False

    # adds the data from the camp object into the database
    def __add_camp_to_database(self, camp):
        try:
            cursor = self.__connection.cursor()
            query = f"INSERT INTO camps VALUES('{camp.name}','{camp.location}',NULL, \
            '{camp.capacity}', '{camp.medicine}','{camp.food}')"
            self.__connection.execute(query)
            self.__connection.commit()
            return True 
        except Exception as e:
            print(f"The exception/error is: {e}")
            return False

    # removes the camp from the database
    def __remove_camp_from_database(self, camp):
        try:
            cursor = self.__connection.cursor()
            query = f"DELETE FROM camps where camp_id = '{camp.id}'"
            cursor.execute(query)
            self.__connection.commit()
            return True 
        except Exception as e:
            print(f"The exception/error is: {e}")
            return False

    # returns the number of camps in the database
    def number_of_camps(self):
        c = self.__connection.cursor()
        c.execute("SELECT COUNT(DISTINCT camp_id) FROM camps")
        return c.fetchone()[0]

    # checks if the camp  in the database, returns true if it exists, false if it does not
    def does_camp_exist(self, camp_id):
        c = self.__connection.cursor()
        
        c.execute(f"SELECT camp_id FROM camps WHERE camp_id = {camp_id}")
        result = c.fetchone()

        if type(result) == tuple and type(result[0]) == int:
            return True
        return False   

    # update method - updates the camp object, through the database
    def update_camp(self, camp):
        if self.__is_valid(camp):
            self.__update_camp_object(camp)
            self.__maps_controller.update_address(camp.location, camp.id)
            return True
        else:
            return("Error: This camp was not updated due to invalid fields")  

    # updates all the fields of the camp object in the database
    def __update_camp_object(self, camp):
        try:
            c = self.__connection.cursor()
            query = f"UPDATE camps SET camp_name = '{camp.name}', camp_location = '{camp.location}', \
            capacity = '{camp.capacity}', num_medicine = '{camp.medicine}', num_food = '{camp.food}' \
            WHERE camp_id = '{camp.id}'"
            c.execute(query)
            self.__connection.commit()
            return True 
        except Exception as e:
            print(f"The exception/error is: {e}")
            return False    

    #gets all camp ids
    def get_list_of_camp_ids(self):
        c = self.__connection.cursor()
        c.execute("SELECT camp_id FROM camps")
        result = c.fetchall()

        if type(result) == list:
            result = self.__clean_list(result)
            return result
        return []

    #converts an array from [(1,), (2,), (3,)] into [1, 2, 3]
    def __clean_list(self,result):
        clean_result = []
        for data in result:
            clean_result.append(data[0])
        return clean_result    

    #returns the current and total capacities as a fraction
    def get_capacity_fraction(self,camp):

        num_refugees = self.__refugee_controller.number_of_refugees_by_camp(camp.id)

        if num_refugees == None or num_refugees == 0:
            return (f"0/{camp.capacity}")

        result = (f"{num_refugees}/{camp.capacity}")

        return result

    #get camp name associated with the id
    def get_camp_name(self, camp_id):
        c = self.__connection.cursor()
        c.execute(f"SELECT camp_name FROM camps WHERE camp_id = '{camp_id}'")
        result = c.fetchone()
        if self.does_camp_exist(camp_id):
            return result[0]
        return "Name unavaliable"            

    #gets the location of the camp associated with the camp id
    def get_camp_location(self, camp_id):
        c = self.__connection.cursor()
        c.execute(f"SELECT camp_location FROM camps WHERE camp_id = {camp_id}")
        result = c.fetchone()
        if self.does_camp_exist(camp_id):
            return result[0]
        return "location unavaliable"

    #returns the maximum capacity of a camp
    def get_max_capacity(self,camp_id):
        c = self.__connection.cursor()
        c.execute(f"SELECT capacity FROM camps WHERE camp_id = {camp_id}")
        return c.fetchone() 
