from datetime import date

class Emergency:

    def __init__(self, __ep_id, __emergency_type, __description, __geog_area, __camp_id=None, 
                 __start_date=date.today().strftime('%Y-%m-%d'), __closing_date="None", __is_closed=0):

        self.__ep_id = __ep_id
        self.__emergency_type = __emergency_type
        self.__description = __description
        self.__geog_area = __geog_area
        self.__camp_id = int(__camp_id)
        self.__start_date = __start_date
        self.__closing_date = __closing_date
        self.__is_closed = __is_closed
        
    @property
    def camp_id(self):
        return self.__camp_id

    @camp_id.setter
    def camp_id(self, camp_id):
        self.__camp_id = camp_id

    @property
    def closing_date(self):
        return self.__closing_date

    @closing_date.setter
    def closing_date(self, closing_date):
        self.__closing_date = closing_date

    @property
    def is_closed(self):
        return self.__is_closed

    @is_closed.setter
    def is_closed(self, is_closed):
        self.__is_closed = is_closed

    @property
    def ep_id(self):
        return self.__ep_id

    @ep_id.setter
    def ep_id(self, ep_id):
        self.__ep_id = ep_id

    @property
    def emergency_type(self):
        return self.__emergency_type

    @emergency_type.setter
    def emergency_type(self, emergency_type):
        self.__emergency_type = emergency_type

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def geog_area(self):
        return self.__geog_area

    @geog_area.setter
    def geog_area(self, geog_area):
        self.__geog_area = geog_area

    @property
    def start_date(self):
        return self.__start_date

    @start_date.setter
    def start_date(self, start_date):
        self.__start_date = start_date
