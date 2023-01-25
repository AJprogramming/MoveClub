from movieclubs import app
from movieclubs.models.users_model import User
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


# render_templates

@app.route('/register')
def register():
    return render_template('/createaccount.html')

@app.route('/')
@app.route('/login')
def login():
    return render_template('/login.html')

@app.route('/genres')
def genres():
    if 'users_id' not in session:
        return redirect('/login')
    data = {
        'id' : session['users_id']
    }
    return render_template('/genres.html', user=User.get_one(data))

@app.route('/edit/genres')
def editgenres():
    if 'users_id' not in session:
        return redirect('/login')
    data = {
        'id' : session['users_id']
    }
    return render_template('/editgenres.html', user=User.get_one(data))

@app.route('/bio')
def bio():
    if 'users_id' not in session:
        return redirect('/login')
    data = {
        "id" : session['users_id']
    }
    return render_template('/bio.html', user=User.get_one(data))

@app.route('/editbio')
def editbio():
    if 'users_id' not in session:
        return redirect('/login')
    data = {
        "id" : session['users_id']
    }
    return render_template('/editbio.html', bio=User.get_one(data))


# -------------------------- redirect -----------------------------------

@app.route('/logging_in', methods=['POST'])
def logging_in():
    data = {
        "email": request.form['email']
    }
    user = User.get_email(data)
    if not user:
        flash("Invalid Creditentials","log")
        return redirect("/login")
    
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Invalid Creditentials","log")
        return redirect("/login")
    session['users_id'] = user.id
    id = session['users_id']
    return redirect(f"/home/{id}")

@app.route('/registering', methods=['POST'])
def registering():
    is_valid = User.validate_user(request.form)
    
    if not is_valid:
        return redirect('/register')
    password = bcrypt.generate_password_hash(request.form["password"])
    account = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "username" : request.form["username"],
        "password" : password,
    }
    id = User.new_user(account)
    session['users_id'] = id
    print(id)
    
    return redirect('/genres')

@app.route('/choosing_genres', methods=['POST'])
def choosing_genres():
    list = request.form.getlist("genres")
    print(list)
    is_valid = User.validate_genres(list)
    
    if not is_valid:
        return redirect('/genres')
    genre = {
        "id" : session['users_id'],
        "fav_genre1" : list[0],
        "fav_genre2" : list[1],
        "fav_genre3" : list[2],
    }
    User.new_user_genre(genre)
    id = session['users_id']
    print(id)
    
    return redirect(f'/bio')

@app.route('/edit_genres', methods=['POST'])
def edit_genres():
    list = request.form.getlist("genres")
    print(list)
    is_valid = User.validate_genres(list)
    
    if not is_valid:
        return redirect('/edit/genres')
    genre = {
        "id" : session['users_id'],
        "fav_genre1" : list[0],
        "fav_genre2" : list[1],
        "fav_genre3" : list[2],
    }
    User.new_user_genre(genre)
    id = session['users_id']
    return redirect(f'/home/{id}')

@app.route('/create_bio', methods=['POST'])
def create_bio():
    
    is_valid = User.validate_bio(request.form)
    if not is_valid:
        return redirect('/bio')
    
    bio = {
        "id" : session['users_id'],
        "bio" : request.form["bio"]
    }
    User.new_user_bio(bio)
    id = session['users_id']
    return redirect(f"/home/{id}")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')