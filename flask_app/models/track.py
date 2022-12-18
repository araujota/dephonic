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
        self.user = None