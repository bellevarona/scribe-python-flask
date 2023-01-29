from flask import Blueprint, jsonify, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():

    if request.method=='POST':
        note = request.form.get('note')
        weather = request.form.get('weather')
        emotion = request.form.get('emotion')
        person = request.form.get('person')
        activity = request.form.get('activity')
        scene = request.form.get('scene')
        food = request.form.get('food')
        food_rate = request.form.get('food-rate')
        day_title = request.form.get('day_title')
        
        
        if len(note)<1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(
                data=note,
                user_id=current_user.id,
                day_title=day_title,
                weather=weather,
                emotion=emotion,
                person=person,
                activity=activity,
                scene=scene,
                food=food,
                food_rate=food_rate
                )
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!',category='success')

    return render_template("home.html", user=current_user)

    
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return render_template("mynotes.html",user=current_user)
    # return jsonify({})

@views.route('/mynotes')
def mynotes():
    return render_template('mynotes.html',user=current_user)


