class Camps:
    def __init__(self, __name, __id, __location, __capacity, __num_medicine, __num_food):
        self.__name = __name
        self.__id = __id
        self.__location = __location
        self.__capacity = __capacity
        self.__num_medicine = __num_medicine
        self.__num_food = __num_food 

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
    def medicine(self):
        return self.__num_medicine

    @property
    def capacity(self):
        return self.__capacity

    @property
    def food(self):
        return self.__num_food        

    @name.setter
    def name(self, name):
        if name == "":
            raise ValueError("The name you entered is blank/empty")
        self.__name = name   

    @capacity.setter
    def capacity(self, new_capacity):
        if new_capacity < 0:
            raise ValueError("The number entered is less than 0")
        self.__capacity = new_capacity       

    @medicine.setter
    def medicine(self, num):
        if num < 0:
            raise ValueError("The number entered is less than 0")
        self.__num_medicine = num 

    @location.setter
    def location(self, new_location):
        if not new_location:
            raise ValueError("The location you entered is empty/blank")
        self.__location = new_location

    @food.setter
    def food(self, num):
        if num < 0:
            raise ValueError("The number entered is less than 0")
        self.__num_food = num  
