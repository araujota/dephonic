import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask

FLASK_SECRET=os.getenv('FLASK_SECRET_KEY')

app = Flask(__name__)

app.secret_key = FLASK_SECRET

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)