from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import track
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0_9.+_-]+@[a-zA-Z0_9.+_-]+\.[a-zA-z]+$')

class User:
    db = "dephonics_schema"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.tracks =[]
        
    @classmethod
    def reg_user(cls, data):
        query = "INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results =  connectToMySQL(cls.db).query_db(query, data)
        
        if len(results) < 1:
            return False
        row = results[0]
        user = cls(row)
        return user

    @classmethod
    def user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results =  connectToMySQL(cls.db).query_db(query, data)
        
        if len(results) < 1:
            return False
        row = results[0]
        user = cls(row)
        return user
    
    @staticmethod
    def val_register(user):
        is_valid = True
        user_db = User.user_by_email(user)
        if user_db:
            flash('Email already used.')
            is_valid = False
        if len(user['first_name']) <2:
            flash ('First name must be at least 2 characters.')
            is_valid = False
        if len(user['last_name']) <2:
            flash ('Last name must be at least 2 characters.')
            is_valid = False
        if len(user['password']) <8:
            flash ('Password must be at least 8 characters.')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Your passwords must match.')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email.')
            is_valid = False
        return is_valid

    @staticmethod
    def val_update(user):
        is_valid = True
        #the_user_filtered_by_id = User.user_by_id(user)
        #print(the_user_filtered_by_id)
        user_db = User.user_by_email(user)
        #if the_user_filtered_by_id.email != user['email']:
        #    print("Not same email.")
        if user_db:
            print("Email exists in database")
            flash("Can not change email.")
            is_valid = False
        if len(user['first_name']) <3:
            flash ('First name must be at least 3 characters.')
            is_valid = False
        if len(user['last_name']) <3:
            flash ('Last name must be at least 3 characters.')
            is_valid = False
        if len(user['password']) <8:
            flash ('Password must be at least 8 characters.')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email.')
            is_valid = False

        return is_valid

    @staticmethod
    def val_login(user):
        is_valid = True
        user_db = User.user_by_email(user)
        if not user_db:
            flash('There is no account with this email.')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email.')
            is_valid = False
        if len(user['password']) <8:
            flash ('Password must be at least 8 characters.')
            is_valid = False
        return is_valid
    
    @classmethod
    def update_user(cls, data):
        query ="UPDATE users SET firstName = %(firstName)s, lastName = %(lastName)s, email = %(email)s, password = %(password)s WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def show(cls, data):
        query="""
        SELECT * FROM tracks LEFT JOIN users ON tracks.user_id = users.id WHERE tracks.id = %(id)s;
        """
        results = connectToMySQL('dephonics_schema').query_db(query, data)
        print(results)
        return results

    #if needed. replace *whatever* with whatever is needed. Many to Many relationship
    # @classmethod
    # def get_users_with_paint( cls , data ):
    #     query = "SELECT * FROM users LEFT JOIN *whatever* ON *whatever*.user_id = users.id LEFT JOIN tracks ON *whatever*.track_id = tracks.id WHERE users.id = %(id)s;"
    #     results = connectToMySQL('users').query_db( query , data )
    #     user = cls( results[0] )
    #     for db_row in results:
    #         track_data = {
    #             "id" : db_row["id"],
    #             "title" : db_row["title"],
    #             "description" : db_row["description"],
    #             "created_at" : db_row["tracks.created_at"],
    #             "updated_at" : db_row["tracks.updated_at"]
    #         }
    #         user.tracks.append( track.Track( track_data ) )
    #     return user

