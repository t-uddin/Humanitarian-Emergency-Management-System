from Back_End.Users.UserController import UserController

class databaseSetup:
    def __init__(self, connection):
        self.__connection = connection
        self.user_controller = UserController(connection)
        print("databaseSetup init")

    # Drop charts tables
    def drop_charts_tables(self):
        self.__connection.execute("DROP TABLE camps")
        self.__connection.execute("DROP TABLE users")
        self.__connection.execute("DROP TABLE refugeeProfile")

        self.__connection.commit()
        print("Charts tables dropped")

    # Setup tables
    def setup_table(self):

        # Create camps table
        self.__connection.execute("""CREATE TABLE IF NOT EXISTS camps(
            camp_name text,
            camp_location text,
            camp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            capacity INTEGER,
            num_medicine INTEGER,
            num_food INTEGER,
            unique(camp_id)
            )""")
        self.__connection.commit()

        # Create refugeeProfile table
        self.__connection.execute("""CREATE TABLE IF NOT EXISTS refugeeProfile(
	        refugeeProfileId INTEGER PRIMARY KEY AUTOINCREMENT,
            firstName datatype TEXT,
            lastName datatype TEXT,
            familySize datatype INTEGER,
            campID datatype INTEGER,
            medicalConditions datatype TEXT,
            unique(refugeeProfileId)
            )""")
        self.__connection.commit()

        # Create Emergency Plan table
        self.__connection.execute("""CREATE TABLE IF NOT EXISTS emergency_plan(
            ep_id INTEGER PRIMARY KEY AUTOINCREMENT,
            emergency_type TEXT,
            description TEXT,
            geog_area TEXT,
            camp_id TEXT,
            start_date TEXT,
            closing_date TEXT,
            is_closed INTEGER
            )""")
        self.__connection.commit()

        # Create Users table
        self.__connection.execute("""CREATE TABLE IF NOT EXISTS users(
                                username VARCHAR UNIQUE, 
                                password VARCHAR, 
                                is_admin INTEGER DEFAULT 0, 
                                first_name VARCHAR, 
                                last_name VARCHAR, 
                                is_active INTEGER DEFAULT 1, 
                                phone_number TEXT NOT NULL DEFAULT '', 
                                address TEXT NOT NULL DEFAULT '', 
                                camp_id INTEGER NOT NULL DEFAULT '', 
                                availability TEXT NOT NULL DEFAULT '')""")

        # Create notice board table
        self.__connection.execute("""CREATE TABLE IF NOT EXISTS notice_board(
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            camp_id INTEGER,
            priority_rating INTEGER,
            unique(message_id)
            )""")

        # Create campsAddress table
        self.__connection.execute("""CREATE TABLE IF NOT EXISTS campsAddress(
                camp_id INTEGER PRIMARY KEY,
                address TEXT,
                address_latitude FLOAT,
                address_longitude FLOAT,
                unique(camp_id)
                             )""")

        # Commit tables creation to db
        self.__connection.commit()

        print("Tables created")

    def add_data(self):
        c = self.__connection.cursor()

        # Add Volunteers
        password = 'passvolunteer'
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerjames','{self.user_controller.password_hash_function(password)}', 0, 'James','Scott',1, '05983835','Kent Avenue',1,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteertom','{self.user_controller.password_hash_function(password)}', 0, 'Tom','Deleaney',1, '05983835','Kent Avenue',2,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerjohn','{self.user_controller.password_hash_function(password)}', 0, 'John','Senpu',1, '05983835','Kent Avenue',3,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerjamie','{self.user_controller.password_hash_function(password)}', 0, 'Jamie','Pallance',1, '05983835','Kent Avenue',4,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerharry','{self.user_controller.password_hash_function(password)}', 0, 'Harry','Hungary',1, '05983835','Kent Avenue',5,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteeremma','{self.user_controller.password_hash_function(password)}', 0, 'Emma','Denderand',1, '05983835','Kent Avenue',1,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteeramy','{self.user_controller.password_hash_function(password)}', 0, 'Amy','Arshens',1, '05983835','Kent Avenue',2,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerlucy','{self.user_controller.password_hash_function(password)}', 0, 'Lucy','Kelt',0, '05983835','Kent Avenue',3,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerjon','{self.user_controller.password_hash_function(password)}', 0, 'Jon','Severu',0, '05983835','Kent Avenue',4,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteereric','{self.user_controller.password_hash_function(password)}', 0, 'Eric','Ionuscu',0, '05983835','Kent Avenue',5,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteermark','{self.user_controller.password_hash_function(password)}', 0, 'Mark','Fendaf',0, '05983835','Kent Avenue',1,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerjoe','{self.user_controller.password_hash_function(password)}', 0, 'Joe','Polder',0, '05983835','Kent Avenue',2,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerkonker','{self.user_controller.password_hash_function(password)}', 0, 'Konker','Derf',1, '05983835','Kent Avenue',1,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerpoal','{self.user_controller.password_hash_function(password)}', 0, 'Poal','Dadar',1, '05983835','Kent Avenue',2,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteereva','{self.user_controller.password_hash_function(password)}', 0, 'Eva','Ponderandu',1, '05983835','Kent Avenue',3,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerhellen','{self.user_controller.password_hash_function(password)}', 0, 'Hellen','Reds',1, '05983835','Kent Avenue',4,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerstud','{self.user_controller.password_hash_function(password)}', 0, 'Stud','Leeds',1, '05983835','Kent Avenue',5,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerrucy','{self.user_controller.password_hash_function(password)}', 0, 'Rucy','Koko',1, '05983835','Kent Avenue',1,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteersam','{self.user_controller.password_hash_function(password)}', 0, 'Sam','Feds',1, '05983835','Kent Avenue',2,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerdan','{self.user_controller.password_hash_function(password)}', 0, 'Dan','Dread',0, '05983835','Kent Avenue',3,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteeralan','{self.user_controller.password_hash_function(password)}', 0, 'Alan','Scott',0, '05983835','Kent Avenue',4,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteersue','{self.user_controller.password_hash_function(password)}', 0, 'Sue','Peters',0, '05983835','Kent Avenue',5,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteervivian','{self.user_controller.password_hash_function(password)}', 0, 'Vivian','Jeffers',0, '05983835','Kent Avenue',1,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteeralex','{self.user_controller.password_hash_function(password)}', 0, 'Alex','James',0, '05983835','Kent Avenue',2,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerjenny','{self.user_controller.password_hash_function(password)}', 0, 'Jenny','Scott',1, '05983835','Kent Avenue',1,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteeralexandra','{self.user_controller.password_hash_function(password)}', 0, 'Alexandra','Lodetta',1, '05983835','Kent Avenue',2,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerlynette','{self.user_controller.password_hash_function(password)}', 0, 'Lynette','Nursy',1, '05983835','Kent Avenue',3,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerpaulo','{self.user_controller.password_hash_function(password)}', 0, 'Paulo','Stevens',1, '05983835','Kent Avenue',4,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteersammy','{self.user_controller.password_hash_function(password)}', 0, 'Sammy','Scott',1, '05983835','Kent Avenue',5,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerkylie','{self.user_controller.password_hash_function(password)}', 0, 'Kylie','Jenner',1, '05983835','Kent Avenue',1,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerstacy','{self.user_controller.password_hash_function(password)}', 0, 'Stacy','Sends',1, '05983835','Kent Avenue',2,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerjabba','{self.user_controller.password_hash_function(password)}', 0, 'Jabba','Thehut',0, '05983835','Kent Avenue',3,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerluke','{self.user_controller.password_hash_function(password)}', 0, 'Luke','Skywalker',0, '05983835','Kent Avenue',4,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerrendetta','{self.user_controller.password_hash_function(password)}', 0, 'Rendetta','Peters',0, '05983835','Kent Avenue',5,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerbernie','{self.user_controller.password_hash_function(password)}', 0, 'Bernie','Sanders',0, '05983835','Kent Avenue',1,'TTTTTTT')")
        self.__connection.execute(
            f"INSERT into users VALUES('volunteerguetta','{self.user_controller.password_hash_function(password)}', 0, 'Guetta','Seles',0, '05983835','Kent Avenue',2,'TTTTTTT')")


        # Add camps
        self.__connection.execute("INSERT INTO camps VALUES ('Alpha','South Sudan',NULL, 102,40,96)")
        self.__connection.execute("INSERT INTO camps VALUES ('Bravo','Ghana',NULL, 99,86,105)")
        self.__connection.execute("INSERT INTO camps VALUES ('Charlie','Bangladesh',NULL,74,20,80)")
        self.__connection.execute("INSERT INTO camps VALUES ('Delta','Sri Lanka',NULL, 48,98,76)")
        self.__connection.execute("INSERT INTO camps VALUES ('Echo','Germany',NULL, 40,90,88)")

        # Add campsAddress
        self.__connection.execute("INSERT INTO campsAddress VALUES(1, 'South Sudan', 7.8699431, 29.6667897)")
        self.__connection.execute("INSERT INTO campsAddress VALUES(2, 'Ghana', 8.0300284, -1.0800271)")
        self.__connection.execute("INSERT INTO campsAddress VALUES(3, 'বাংলাদেশ', 24.4769288, 90.2934413)")
        self.__connection.execute("INSERT INTO campsAddress VALUES(4, 'ශ්‍රී ලංකාව இலங்கை', 7.5554942, 80.7137847)")
        self.__connection.execute("INSERT INTO campsAddress VALUES(5, 'Deutschland', 51.0834196, 10.4234469)")

        # Add refugeeProfiles
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Ken','Rogers',5,1,'Medical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Elon','Musk',6,1,'Psychiatric')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'James','Paul',8,2,'Medical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Celine','Artens',6,3,'Surgical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Greg','Wallace',6,4,'Surgical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'James','Peters',5,5,'None')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Susan','Logs',4,5,'Psychiatric')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Darren','Jeffs',2,4,'Medical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Ak','Selly',5,3,'Multiple')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Su','Li',5,1,'Multiple')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Soen','Pelly',8,1,'None')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Seffer','Pendred',3,2,'Medical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Warren','Buffet',7,1,'Psychiatric')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Tellen','Peltzer',5,1,'Medical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Kun','Gercy',8,2,'Medical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Bruce','Lee',8,1,'Surgical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Peter','Jones',2,2,'Surgical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Kond','Diker',7,4,'None')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Lok','Bard',6,5,'Psychiatric')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Sun','Po',4,5,'Medical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Kernel','Py',5,1,'Multiple')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Juju','Jones',5,4,'Multiple')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Korn','Pinder',4,3,'None')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Cem','Peters',6,2,'Medical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Ruddy','Bun',4,1,'Psychiatric')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Deder','Long',5,1,'Medical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Jenner','Paul',5,2,'Medical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Sander','Artens',8,1,'Surgical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Ponder','Fain',6,2,'Surgical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Fender','Janeer',7,4,'None')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Abdin','Sams',6,5,'Psychiatric')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Samad','Jeffs',8,5,'Medical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Pepper','Jones',5,2,'Multiple')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Crender','Lones',2,3,'Multiple')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Jake','Paul',4,2,'None')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Kenny','Rogers',8,5,'Medical')")
        self.__connection.execute("INSERT INTO refugeeProfile VALUES(NULL,'Wyclife','Jones',7,1,'Psychiatric')")

      # Add Admin
        password = 'passadmin'
        self.__connection.execute(
            f"INSERT into users VALUES('admin1', '{self.user_controller.password_hash_function(password)}', 1, 'admin','UCL', 1, '0783755845', 'London Street', 1, 'NONE')")

        # Add Emergency Plans
        self.__connection.execute(
            'INSERT INTO emergency_plan VALUES(NULL, "Flood", "Flooding of central Europe", "Germany", 1, "2021-12-17", "2021-12-31", 0)')
        self.__connection.execute(
            'INSERT INTO emergency_plan VALUES(NULL, "Tornado", "Midwest USA", "USA", 2, "2021-11-17", "2021-12-31", 0)')
        self.__connection.execute(
            'INSERT INTO emergency_plan VALUES(NULL, "Storm", "Storm Arwen", "UK", 3, "2021-12-01", "2021-12-31", 0)')

        # Add bulletins
        c.execute(
            "INSERT INTO notice_board VALUES (NULL,'We will soon have a large influx of refugees, so be prepared',1,1)")
        c.execute("INSERT INTO notice_board VALUES (NULL,'There is scheduled maintanance over the xmas holidays',1,2)")
        c.execute("INSERT INTO notice_board VALUES (NULL,'Rotas for next month will be released 3 days late',2,0)")
        c.execute(
            "INSERT INTO notice_board VALUES (NULL,'There is a storm on tuesday, so we will be placing sandbags in front of doors',2,1)")
        c.execute("INSERT INTO notice_board VALUES (NULL,'Merry Christmas',2,0)")
        
        self.__connection.commit()
        print("SQL committed")




