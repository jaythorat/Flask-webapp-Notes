# Importing Modules
from flask import Blueprint,render_template ,request ,flash
from flask_login import login_user, login_required, logout_user, current_user,LoginManager
from .models import  Note
from . import db
import json
from .models import User

#Registering Blueprints for views
views = Blueprint('views',__name__)

#Home page and will show only if user is logged in
@views.route('/',methods=['GET',"POST" ])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        # validating conditions for note.
        if len(note) < 1:
            flash('Note is too short..!',category='error')
        else:
            # Adding new note to database with corresponding user id
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("NOTE ADDED...",category='success')
    #Will return home page if GET req. is received
    return render_template('home.html',user = current_user,name = current_user.first_name)


# Delete note function
@views.route('/delete-note', methods=['POST'])
def delete_note():
    #Load req. data in json 
    note = json.loads(request.data)
    #Extracting 'noteId' from requested data.
    noteId = note['noteId']
    #checking if note with 'noteid' is availabale and is corresponds to logged in user or not.
    note = Note.query.get(noteId)
    if note:
        #If True then note will get deleted
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    # returning NULL jsonify statement. Because of FLASK's requirements.
    return jsonify({})