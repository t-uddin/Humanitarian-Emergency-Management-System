from datetime import date, datetime
from Back_End.Emergency_Plan.EmergencyPlan import Emergency

class EPController:

    def __init__(self, connection):
        self.__connection = connection

    def initialise(self):
        c = self.__connection.cursor()
        c.execute("SELECT * FROM emergency_plan")
        data = c.fetchall()
        plans = []
        for emergency_plan in data:
            emergency_plan_object = Emergency(emergency_plan[0], emergency_plan[1], emergency_plan[2],
                                              emergency_plan[3], emergency_plan[4], emergency_plan[5],
                                              emergency_plan[6], self.__is_closed_display(emergency_plan[7]))
            if self.__is_valid(emergency_plan_object):
                plans.append(emergency_plan_object)
            else:
                print(f"Emergency Plan object data is not valid, Emergency Plan with ID {emergency_plan_object.ep_id} "
                      f"has not been added")
        return plans

    def __is_closed_display(self,is_closed):
        if is_closed == 0:
            return "OPEN"
        return "CLOSED"

    def __is_valid(self, emergency):
        if emergency.ep_id != "" and emergency.emergency_type != "" and emergency.description != "" and \
            emergency.geog_area != "" and self.__is_date_format_valid(emergency.start_date) \
            and self.__is_closing_date_valid(emergency):
            return True
        return False

    # saves an emergency plan to the database if it is valid
    def save(self, emergency):
        if self.__is_valid(emergency):
            emergency.is_closed = self.__set_plan_status(emergency)
            self.__add_emergency_plan(emergency)
            return True
        else:
            return("Emergency Plan not saved. Please ensure all fields are completed!")

    # returns true if the date is in the correct format i.e. YYYY-MM-DD
    def __is_date_format_valid(self, date):
        try:
            datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return False
        return True

    # Validates start and closing date and sets is_closed by checking against start_date and today's date
    def __is_closing_date_valid(self, emergency):
        start_date = emergency.start_date 
        closing_date = emergency.closing_date
        #if set to None, there is no closing date set
        if closing_date == "None":
            return True
        
        #if closing date is not in the correct format raise an error
        if not self.__is_date_format_valid(closing_date):
            return False  
        #checking if start date is AFTER closing date    
        elif start_date > closing_date:
            return False
        return True

    #sets the status, depending on the dates, open is 0, closed is 1
    def __set_plan_status(self, emergency):
        
        start_date = datetime.strptime(emergency.start_date, '%Y-%m-%d').date() 
        
        #if the start date has not been reached, set to closed i.e. 1
        if date.today() < start_date:
            return 1
        #if the closing date hasnt been set, set is_closed to open
        elif emergency.closing_date == "None":
            return 0

        closing_date = datetime.strptime(emergency.closing_date, '%Y-%m-%d').date() 
        
        #if the closing date has already passed, set to closed i.e. 1
        if closing_date < date.today():
            return 1
        return 0

    #Open/Closed override of an emergency plan
    def open_or_close_plan(self, emergency):
        #get current status
        current_status = emergency.is_closed

        if current_status == 1:
            updated_status = 0
        else:
            updated_status = 1

        try:
            query = f"""
                UPDATE emergency_plan
                SET is_closed = '{updated_status}'
                WHERE ep_id = '{emergency.ep_id}' 
                """
            self.__connection.execute(query)
            self.__connection.commit()
            return True
        except Exception as e:
            return(f"Error could not update status: {e}")

    #returns true if the dates have been changed, false if they have not changed
    def __have_dates_changed(self,emergency_plan_updated):
        c = self.__connection.cursor()
        c.execute("SELECT * FROM emergency_plan")
        data = c.fetchall()
        for emergency_plan in data:
            emergency_plan_old = Emergency(emergency_plan[0], emergency_plan[1], emergency_plan[2],
                                              emergency_plan[3], emergency_plan[4], emergency_plan[5],
                                              emergency_plan[6], emergency_plan[7])

        if emergency_plan_updated.start_date != emergency_plan_old.start_date:
            return True                                 
        elif emergency_plan_updated.closing_date != emergency_plan_old.closing_date:
            return True  
        return False    

    def __add_emergency_plan(self, emergency):
        with self.__connection:
            try:
                c = self.__connection.cursor()
                query = f"""
                INSERT INTO emergency_plan VALUES(
                NULL,
                '{emergency.emergency_type}',
                '{emergency.description}',
                '{emergency.geog_area}',
                '{emergency.camp_id}',
                '{emergency.start_date}',
                '{emergency.closing_date}',
                '{emergency.is_closed}'
                )"""
                self.__connection.execute(query)
                return True
            except Exception as e:
                print(f"Error: {e}")
                return False

    #updates the information in the emergency plan database, only changes the status
    #if the dates have been changed so, the override of opening the emergency plan
    #will no longer take affect
    def update_ep(self, emergency):
        if self.__is_valid(emergency):
            #only change the status if the date was changed
            if self.__have_dates_changed(emergency):
                emergency.is_closed = self.__set_plan_status(emergency)
            self.__update_ep_object(emergency)
            return True
        else:
            return("Update FAILED. Please ensure all fields have been completed!")

    def __update_ep_object(self, emergency):
        with self.__connection:
            try:
                c = self.__connection.cursor()
                query = f"""
                UPDATE emergency_plan
                SET emergency_type = '{emergency.emergency_type}',
                description = '{emergency.description}',
                geog_area = '{emergency.geog_area}',
                camp_id = '{emergency.camp_id}',
                start_date = '{emergency.start_date}',
                closing_date = '{emergency.closing_date}', 
                is_closed = '{emergency.is_closed}'
                WHERE ep_id = '{emergency.ep_id}' 
                """
                self.__connection.execute(query)
                return True
            except Exception as e:
                print(f"Error: {e}")
                return False

    def delete_emergency_plan(self, ep_id):
        with self.__connection:
            try:
                c = self.__connection.cursor()
                query = f"""
                DELETE FROM emergency_plan
                WHERE ep_id = '{ep_id}' 
                """
                self.__connection.execute(query)
                return True
            except Exception as e:
                return (f"Error: {e}")
