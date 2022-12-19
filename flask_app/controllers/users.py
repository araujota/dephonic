from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.track import Track
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return "DePhonic"

@app.route('/tracks')
def user_tracks():
    user_data = {
        'id' : session['user_id']
    }
    user = User.user_by_id(user_data)
    tracks = Track.select_all()
    return render_template('', user = user, tracks = tracks)

@app.route('/login', methods=['POST'])
def login():
    if not User.val_login(request.form):
        return redirect('/')
    user = User.user_by_email(request.form)
    if user:
        if not bcrypt.check_password_hash(user.password, request.form["password"]):
            flash("Email/Password combination is incorrect")
            return redirect('/')

        session['user_id'] = user.id
        flash("Success! Welcome!")
        return redirect('/tracks')

    flash("No email for this account.")
    return redirect("/")

@app.route('/register', methods=["POST"])
def reg():
    if not User.val_register(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    reg_data = {
        'first_name': request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }

    user_id = User.reg_user(reg_data)
    session["user_id"] = user_id
    flash("Registration was successful")
    return redirect("/tracks")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')