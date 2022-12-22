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
    return render_template("showtracks.html", user=user, all_tracks = Track.select_all())


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
            filename = secure_filename(track.filename)
            track.save(os.path.join(app.config['UPLOAD_FOLDER'], track.filename))

    data = {
        'title': request.form['title'],
        'audio_file': request.files['audio_file'],
        'users_id': session['user_id']
    }
    Track.add_track(data)
    return redirect('/showtracks')

@app.route('/play/<int:id>')
def playtrack(id):
    data = {
        "id":id,
        }
    track = Track.get_one_track(data)
    track_file = track.audio_file.split("'")
    track_filename = track_file[1]
    return render_template("view_track.html", track=track, track_filename=track_filename)


# Show One Track
@app.route('/show/<int:id>')
def show_one_track(id):
    data = {
        "id":id,
        }
    track = Track.get_one_track(data)
    track_file = track.audio_file.split()
    track_filename = track_file[1]
    return render_template("edit_track.html", track=track, user=User.show(data), track_filename=track_filename)

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
    data = {
        'id':request.form['id'],
        'title': request.form['title'],
        'audio_file': request.form['audio_file'],
        'users_id': session['user_id']
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
