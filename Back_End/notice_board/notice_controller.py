from Back_End.notice_board.notice import Notice

class NoticeBoardController:
    
    def __init__(self,__connection):
        self.__connection = __connection
    
    #returns an array of notice objects generated from all values in the database, for admin
    def initialise(self):
        c = self.__connection.cursor()
        c.execute(f"SELECT * FROM notice_board")

        data = c.fetchall()
        notices = []

        for notice_data in data:
            notice_object = Notice(notice_data[0], notice_data[1], notice_data[2], notice_data[3])
            if self.__is_valid(notice_object):
                notices.append(notice_object)
            else:
                print(f"notice data is not valid, notice with ID: {notice_object.message_id}, has not been added")
        notices.sort(key=lambda c: c.priority_rating, reverse=True)
        return notices     

    #get list of messages associated with camp, sorted the list based on the priority rating
    #priority rating is between 0 to 10
    #for the volunteers dashboard
    def get_notices(self, camp_id):
        notices = []
        
        c = self.__connection.cursor()
        c.execute(f"SELECT * FROM notice_board WHERE camp_id = '{camp_id}'")

        data = c.fetchall()

        for notice_data in data:
            notice_object = Notice(notice_data[0], notice_data[1], notice_data[2], notice_data[3])
            if self.__is_valid(notice_object):
                if notice_object.priority_rating > 0:
                    notice_object.message = self.__add_pinned_message(notice_object)

                notices.append(notice_object)
                 
        notices.sort(key=lambda c: c.priority_rating, reverse=True)
        return notices

    #saves message to dataabse if message is valid, prints message if object is not valid
    def save(self, notice):
        if self.__is_valid(notice):
            self.__add_message_to_database(notice)
        else:
            print("notice not saved, values inputted have an error, please ensure that all fields are valid")

    def delete_message(self, notice):
        if self.__does_message_exist(notice):
            self.__remove_message_from_database(notice)
        else:
            print("Error, when trying to delete message")

    #updates the message only if the changes are valid AND the message is present in the table
    def update_message(self, notice):
        if self.__is_valid(notice) and self.__does_message_exist(notice):
            self.__update_message_object(notice)
            return True
        else:
            print("The message was not updated as the object is not valid, or has invalid fields")  
            return False  

    #checks if the message with the message_id exists in the database
    def __does_message_exist(self, notice):
        c = self.__connection.cursor()
        
        c.execute(f"SELECT message_id FROM notice_board WHERE message_id = '{notice.message_id}'")
        result = c.fetchone()
        if type(result) == tuple and type(result[0]) == int:
            return True
        return False   

    def __add_message_to_database(self, notice):
        try:
            query = f"INSERT INTO notice_board VALUES(NULL,'{notice.message}','{notice.camp_id}', \
            '{notice.priority_rating}')"
            self.__connection.execute(query)
            self.__connection.commit()
            return True 
        except Exception as e:
            print(f"The exception/error is: {e}")
            return False

    def __remove_message_from_database(self, notice):
        try:
            cursor = self.__connection.cursor()
            query = f"DELETE FROM notice_board where message_id = '{notice.message_id}'"
            cursor.execute(query)
            self.__connection.commit()
            return True 
        except Exception as e:
            print(f"The exception/error is: {e}")
            return False

    def __update_message_object(self,notice):
        try:
            c = self.__connection.cursor()
            query = f"UPDATE notice_board SET message = '{notice.message}', camp_id = '{notice.camp_id}', \
            priority_rating = '{notice.priority_rating}' \
            WHERE message_id = '{notice.message_id}'"
            c.execute(query)
            self.__connection.commit()
            return True 
        except Exception as e:
            print(f"The exception/error is: {e}")
            return False    

    def __is_valid(self, notice):
        if notice.message != "" and len(notice.message) <= 120 and notice.camp_id >= 0:
            return True
        return False  

    def get_volunteer_camp(self, username):
        c = self.__connection.cursor()
        c.execute(f"SELECT camp_id FROM users WHERE is_admin = 0 AND is_active = 1 AND username = '{username}' ")
        result = c.fetchone()
        if type(result) == tuple:
            return result[0]
        if type(result) == int:
            return result        
        return 0                      

    def __add_pinned_message(self,notice):
        message = notice.message

        rating = notice.priority_rating

        if rating == 1:
            prefix = "⭐: "
        elif rating == 2:
            prefix = "❗: "
        elif rating == 3:
            prefix = "❗❗: "
        else:
            prefix = "URGENT❗: "

        new_message = prefix + message

        return new_message
