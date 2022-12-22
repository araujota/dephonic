from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.user import User
from flask_app.models.track import Track
from flask import flash
import os
from werkzeug.utils import secure_filename

@app.route('/showtracks')
def all():
    if "user_id" not in session:
        return redirect('/logout')
    user = User.user_by_id({"id":session["user_id"]})
    print(session['user_id'])
    return render_template("showtracks.html", user=user, all_tracks = Track.select_all_by_user({"id":session["user_id"]}))


# Add a new track HTML
@app.route('/new')
def new_track():
    return render_template("add_track.html")

# Add a new track form POST method
@app.route('/add', methods = ['POST'])
def add_track():
    if request.method == 'POST':
        if request.files:
            track = request.files['audio_file']
            track.save(os.path.join(app.config['UPLOAD_FOLDER'], track.filename))
            return "File uploaded successfully."
    data = {
        'title': request.form['title'],
        'audio_file': request.files['audio_file'],
        'user_id': session['user_id']
    }
    Track.add_track(data)
    return redirect('/showtracks')


# Show One Track
@app.route('/show/<int:id>')
def show_one_track(id):
    data = {
        "id":id,
        }
    track = Track.get_one_track(data)
    return render_template("view_track.html", track=track, user=User.show(data))

# Edit a Track
@app.route('/track/edit')
def edit_track():
    data = {
        'id': session['user_id']
    }
    user = User.show(data)
    track = Track.get_one_track(data)
    return render_template("edit_track.html", track = track, user=user)

# Edit a Track POST
@app.route('/track/edit/update', methods=["POST"])
def update():
    if request.method == 'POST':
        if request.files:
            uploaded_file = request.files['audio_file']
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename))
            session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    data = {
        'id':request.form['id'],
        'title': request.form['title'],
        'audio_file': request.files['audio_file'],
        'user_id': session['user_id']
    }
    Track.update_track(data)
    return redirect('/showtracks')


# Delete a Track
@app.route('/destroy/<int:id>')
def delete(id):
    data = {
        "id":id
    }
    Track.destroy(data)
    return redirect('/showtracks')
