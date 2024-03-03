import sqlite3


class dbConnection:

    def __init__(self):
        self.__connection = None

    # create db connection
    def connect(self):
        try:
            self.__connection = sqlite3.connect('RFG.db')
            print("database has been opened")
            if self.__connection:
                return self.__connection
        except Exception as e:
            print(f"connection error: {e}")
            return None

    # disconnect the connection / close the database , returns true if the databse has been disconnected
    def disconnect(self):
        if self.__connection:
            self.__connection.close()
            print("database has been closed")
            return True
        else:
            print("Database has not been closed or the database was never open")
            return False
