import hashlib

class UserController:

    def __init__(self, connection):
        self.connection = connection

    # if user object password and username is correct, it returns dict of username and is_admin
    def login_function(self, user_name, password):
        existing_user = self.get_user(user_name)
        if not existing_user:
            raise Exception("Account does not exist")
        
        pwhash = self.get_password(user_name)
        
        if not self.hashed_password_match(password, pwhash):
            raise Exception("Incorrect Password")
        
        status = self.get_status(user_name)
        
        if status == 0:
            raise Exception(
                "Your account has been deactivated. Please contact admin")
        return {'user_name': user_name, 'is_admin': existing_user[2]}

    # returns status of user
    def get_status(self, username):
        cursor = self.connection.cursor()
        query = "SELECT is_active FROM users WHERE username = ?"
        cursor.execute(query, [username])
        result = cursor.fetchone()
        self.connection.commit()
        return result[0]

    # returns None if user does not exist in the database
    def get_user(self, username):
        cursor = self.connection.cursor()
        query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(query, [username])
        result = cursor.fetchone()
        self.connection.commit()
        return result

    def password_hash_function(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def get_password(self, username):
        cursor = self.connection.cursor()
        query = "SELECT password FROM users WHERE username = ?"
        cursor.execute(query, [username])
        result = cursor.fetchone()[0]
        self.connection.commit()
        return result

    def hashed_password_match(self, password, hashed_password):
        if hashlib.sha256(password.encode()).hexdigest() != hashed_password:
            return False
        return True
