class Notice:
    def __init__(self, __message_id, __message, __camp_id, __priority_rating):
        self.__message_id = __message_id
        self.__message = __message
        self.__camp_id = __camp_id
        self.__priority_rating = __priority_rating

    @property
    def message(self):
        return self.__message

    @property
    def message_id(self):
        return self.__message_id

    @property
    def camp_id(self):
        return self.__camp_id

    @property
    def priority_rating(self):
        return self.__priority_rating

    @message.setter
    def message(self,updated_message):
        self.__message = updated_message                

    @camp_id.setter
    def camp_id(self, updated_camp_id):
        self.__camp_id = updated_camp_id

    @priority_rating.setter
    def priority_rating(self, upated_priority_rating):
        self.__priority_rating =  upated_priority_rating       