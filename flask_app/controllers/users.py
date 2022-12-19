from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.user import User
from flask_app.models.track import Track
from flask_app import bcrypt
from flask import flash

@app.route('/')
def index():
    return "Let's do this!"