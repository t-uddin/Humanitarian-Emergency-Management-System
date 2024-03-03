class VolunteerStatus:
    def __init__(self, __camp_id, __camp_name, __urgency_rating, __monday, __tuesday, __wednesday,
                 __thursday, __friday, __saturday, __sunday):
        self.__camp_id = __camp_id
        self.__camp_name = __camp_name
        self.__urgency_rating = __urgency_rating
        self.__monday = __monday
        self.__tuesday = __tuesday
        self.__wednesday = __wednesday
        self.__thursday = __thursday
        self.__friday = __friday
        self.__saturday = __saturday
        self.__sunday = __sunday

    @property
    def camp_id(self):
        return self.__camp_id     

    @property
    def camp_name(self):
        return self.__camp_name

    @property
    def urgency_rating(self):
        return self.__urgency_rating

    @property
    def monday(self):
        return self.__monday

    @property
    def tuesday(self):
        return self.__tuesday

    @property
    def wednesday(self):
        return self.__wednesday

    @property
    def thursday(self):
        return self.__thursday

    @property
    def friday(self):
        return self.__friday

    @property
    def saturday(self):
        return self.__saturday                           

    @property
    def sunday(self):
        return self.__sunday
        