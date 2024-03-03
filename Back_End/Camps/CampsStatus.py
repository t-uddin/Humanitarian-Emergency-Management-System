class CampsStatus:
    def __init__(self, __name, __id, __location, __capacity_status, __medicine_status, __food_status, __urgency_rating,
                 __capacity_rating, __medicine_rating, __food_rating):
        self.__name = __name
        self.__id = __id
        self.__location = __location
        self.__capacity_status = __capacity_status
        self.__medicine_status = __medicine_status
        self.__food_status = __food_status

        self.__capacity_rating = __capacity_rating
        self.__medicine_rating = __medicine_rating
        self.__food_rating = __food_rating

        self.__urgency_rating = __urgency_rating

    @property
    def name(self):
        return self.__name

    @property
    def location(self):
        return self.__location

    @property
    def id(self):
        return self.__id

    @property
    def medicine_status(self):
        return self.__medicine_status

    @property
    def capacity_status(self):
        return self.__capacity_status

    @property
    def food_status(self):
        return self.__food_status

    @property
    def urgency_rating(self):
        return self.__urgency_rating

    @property
    def capacity_rating(self):
        return self.__capacity_rating

    @property
    def medicine_rating(self):
        return self.__medicine_rating

    @property
    def food_rating(self):
        return self.__food_rating
