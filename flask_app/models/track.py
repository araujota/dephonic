from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models.user import User

class Track:
    db = "dephonics_schema"
    def __init__ ( self, data ):
        self.id = data['id']
        self.title = data['title']
        self.audio_file = data['audio_file']
        self.qr_code = data['qr_code']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        
    
    @classmethod
    def add_track(cls, data):
        query = """INSERT INTO tracks (title, audio_file, qr_code, user_id)
        VALUES (%(title)s, %(audio_file)s, %(qr_code)s, %(user_id)s);"""
        result = connectToMySQL(cls.db).query_db(query,data)
        return result


    @classmethod
    def get_one_track(cls, data):
        query = """
        SELECT * FROM tracks 
        WHERE id = %(id)s;
        """
        results = connectToMySQL('dephonics_schema').query_db(query, data)
        return cls(results[0])

    
    @classmethod
    def update_track(cls,data):
        query = """UPDATE tracks SET title=%(title)s, audio_file=%(audio_file)s,
        qr_code=%(qr_code)s
        WHERE id = %(id)s;"""
        result = connectToMySQL('dephonics_schema').query_db(query, data)
        return result

    
    @classmethod
    def select_all(cls):
        query = """SELECT * FROM tracks;
        """
        results = connectToMySQL('dephonics_schema').query_db(query)
        all_tracks = []
        for one_track in results:
            all_tracks.append(cls(one_track))
        return all_tracks

    @classmethod
    def select_all_by_user(cls, data):
        query = """SELECT * FROM tracks WHERE user_id = %(id)s;
        """
        results = connectToMySQL('dephonics_schema').query_db(query)
        all_tracks = []
        for one_track in results:
            all_tracks.append(cls(one_track))
        return all_tracks


    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM tracks WHERE id= %(id)s;"
        return connectToMySQL('dephonics_schema').query_db(query,data)
