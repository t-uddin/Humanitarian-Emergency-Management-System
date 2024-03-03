import sqlite3 as sqli
from Back_End.Refugee_Profile.refugee_profile_class import *

class RefugeeProfileController:
    def __init__(self, connection):
        self.__connection = connection

    def initialise(self):
        c = self.__connection.cursor()
        c.execute("SELECT * FROM refugeeProfile")

        data = c.fetchall()
        refugee_profiles = []

        for refugee_profile in data:
            refugee_profile_object = RefugeeProfile(refugee_profile[0],
                                                    refugee_profile[1],
                                                    refugee_profile[2],
                                                    refugee_profile[4],
                                                    refugee_profile[3],
                                                    refugee_profile[5])
            if self.__is_valid(refugee_profile_object):
                refugee_profiles.append(refugee_profile_object)
        return refugee_profiles

    # Use this function to create the a refugee profile
    def save(self, refugee_profile):
        if self.__is_valid(refugee_profile):
            self.__add_refugee_profile_to_database(refugee_profile)
            return True
        else:
            return("Refugee profile not saved, values inputted have an error, please ensure that all fields are valued")
   
    # Inserts a new refugee profile into the database. Save function creates the profile
    def __add_refugee_profile_to_database(self, refugee_profile):
        try:
            params = (refugee_profile.first_name, refugee_profile.last_name, refugee_profile.family_size, \
                      refugee_profile.camp_id, refugee_profile.med_con)
            c = self.__connection.cursor()     
            sql = "INSERT INTO refugeeProfile VALUES (NULL, ?, ?, ?, ?, ?)"
            c.execute(sql, params)
            self.__connection.commit()
            return True
        except Exception as e:
            return False  

    # Checks whether a refugee profile is valid
    def __is_valid(self, refugee_profile):
        if refugee_profile.id != -1 and refugee_profile.first_name != "" and refugee_profile.last_name != "" and \
           refugee_profile.camp_id != "" and refugee_profile.family_size >= 1 and refugee_profile.med_con != "":
            return True
        return False

    # update method - updates the refugee_profile object, through the database
    def update_refugee_profile(self,refugee_profile):
        if self.__is_valid(refugee_profile):
            self.__update_refugee_profile_object(refugee_profile)
            return True
        else:
            return("This camp could not be updated due to invalid fields")  

    # updates all the fields of the refugee_profile object in the database
    def __update_refugee_profile_object(self,refugee_profile):
        try:
            c = self.__connection.cursor()
            query = f"UPDATE refugeeProfile SET firstName = '{refugee_profile.first_name}', \
            lastName = '{refugee_profile.last_name}', \
            campID = '{refugee_profile.camp_id}', \
            familySize = '{refugee_profile.family_size}', \
            medicalConditions = '{refugee_profile.med_con}' \
            WHERE refugeeProfileId = '{refugee_profile.id}'"
            c.execute(query)
            self.__connection.commit()
            return True 
        except Exception as e:
            print(f"The exception/error is: {e}")
            return False    

    # checks to see if the refugee profile is in a camp,  returns true if in a camp, false if not in a camp
    def is_refugee_profile_assigned_camp(self, refugee_id):
        c = self.__connection.cursor()
        query = f"SELECT campID FROM refugeeProfile where refugeeProfileId = '{refugee_id}' AND campID IS NOT NULL"
        c.execute(query)
        result = c.fetchall()
        
        if result:
            return True
        return False

    # Deletes a refugee profile from the database. Their ID needs to be entered.
    def delete_refugee_profile_from_database(self,refugee_profile_id):
        
        c = self.__connection.cursor()
        if self.is_refugee_profile_assigned_camp(refugee_profile_id): 
            return("Error, this refugee is assigned to a camp and cannot be deleted")
        else:
            try:
                query = f"DELETE FROM refugeeProfile where refugeeProfileId = '{refugee_profile_id}'"
                c.execute(query)
                self.__connection.commit()
                return True 
            except Exception as e:
                return(f"Error: {e}")

    # Returns the total count of refugees in a camp (lead family member + family members)
    def number_of_refugees_by_camp(self,camp_id):
            c = self.__connection.cursor()
            c.execute(f"SELECT SUM (familySize) FROM refugeeProfile where campID = '{camp_id}'")
            result = c.fetchone()[0]
            if type(result) == int:
                return result
            return 0

    # remove refuge profile from camp
    def remove_refugee_profile_from_camp(self,refugee_id,camp_id):
        c = self.__connection.cursor()
        if self.is_refugee_profile_assigned_camp(refugee_id):
            c.execute(f"UPDATE refugeeProfile SET campID = NULL WHERE refugeeProfileId = '{refugee_id}'")
            self.__connection.commit()
            print("Refugee profile has been unassigned from this camp")
        else:
            print("This refugee profile doesn't exist within this camp")

    # Returns all of the refugee profiles in a camp
    def return_refugee_profiles_by_camp_id(self, camp_id):
        c = self.__connection.cursor()
        c.execute(f"SELECT * FROM refugeeProfile WHERE campID = {camp_id}")
        
        data = c.fetchall()
        refugee_profiles = []

        for refugee_profile in data:
            refugee_profile_object = RefugeeProfile(refugee_profile[0],
                                                    refugee_profile[1],
                                                    refugee_profile[2],
                                                    refugee_profile[4],
                                                    refugee_profile[3],
                                                    refugee_profile[5])
            if self.__is_valid(refugee_profile_object):
                refugee_profiles.append(refugee_profile_object)
        return refugee_profiles
