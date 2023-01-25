from movieclubs import app
from movieclubs.models.clubs_model import Club
from movieclubs.models.users_model import User
from flask import render_template, redirect, request, session

#route

@app.route('/create_club')
def create_club():
    if 'users_id' not in session:
        return redirect('/login')
    data = {
        'id' : session['users_id']
    }
    return render_template('/createclub.html', user=User.get_one(data))

@app.route('/editclub/<int:id>')
def editclub(id):
    if 'users_id' not in session:
        return redirect('/login')
    data = {
        'id' : id
    }
    return render_template('/editclub.html', club=Club.get_created_club(data), user=User.get_one(data))

#redirect

@app.route('/creating_club', methods=['POST'])
def creating_club():
    
    is_valid = Club.validate_club(request.form)
    if not is_valid:
        return redirect('/create_club')
    
    list = request.form.getlist("genres")
    
    is_valid_genre = Club.validate_club_genre(list)
    
    if not is_valid_genre:
        return redirect('/create_club')
    
    data = {
        "name" : request.form['name'],
        "genre" : list,
        "description" : request.form['description'],
        "users_id" : session['users_id']
    }
    Club.createclub(data)
    return redirect('/findclubs')

@app.route('/editingclub', methods=["POST"])
def editingclub():
    is_valid = Club.validate_club(request.form)
    if not is_valid:
        return redirect('/create_club')
    
    list = request.form.getlist("genres")
    
    is_valid_genre = Club.validate_club_genre(list)
    
    if not is_valid_genre:
        return redirect('/create_club')
    
    data = {
        "id" : request.form['id'],
        "name" : request.form['name'],
        "genre" : list,
        "description" : request.form['description']
    }
    Club.updateclub(data)
    id = request.form['id']
    return redirect(f'/clubpage/{id}')
