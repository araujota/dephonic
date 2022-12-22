import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask

my_id = os.getenv("ID")
FLASK_SECRET=os.getenv('FLASK_SECRET_KEY')

app = Flask(__name__)

app.secret_key = FLASK_SECRET

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

UPLOAD_FOLDER = "flask_app/static/files"
ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'aac', 'flac', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
