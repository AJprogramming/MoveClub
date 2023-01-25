from movieclubs import app
from movieclubs.models.posts_model import Post
from movieclubs.models.clubs_model import Club
from movieclubs.models.users_model import User
from movieclubs.models.joinedclubs_model import Joined
from flask import render_template, redirect, request, session

# render_templates

@app.route('/findclubs')
def findclubs():
    if 'users_id' not in session:
        return redirect('/login')
    data = {
        'id' : session['users_id']
    }
    return render_template('/findclubs.html', allclubs = Club.get_all_clubs(), user=User.get_one(data))

@app.route('/clubpage/<int:id>')
def clubpage(id):
    if 'users_id' not in session:
        return redirect('/login')
    
    data = {
        'id' : id
    }
    
    
    return render_template('/clubpage.html', user=User.get_one, posts=Post.get_posts(data),
                           club = Club.get_created_club(data),
                           usersclubs=Club.get_users_club(data), notjoined=Joined.get_all(data))


# redirect

@app.route('/posting', methods=['POST'])
def posting():
    print(request.form['clubs_id'])
    data = {
        "clubs_id" : request.form['clubs_id'],
        "content" : request.form['content'],
        "users_id" : session['users_id']
    }
    Post.save(data)
    id = request.form['clubs_id']
    return redirect(f'/clubpage/{id}')

@app.route('/deletepost/<int:id>/<int:club>')
def deletepost(id, club):
    data = {
        "id" : id
    }
    Post.delete(data)
    id = club
    return redirect(f'/clubpage/{id}')

@app.route('/deleteclub/<int:id>/')
def deleteclub(id):
    data = {
        "id" : id
    }
    Post.deletepostsfromclub(data)
    Club.delete(data)
    return redirect('/findclubs')

@app.route('/join/<int:id>')
def join(id):
    data = {
        'users_id' : session['users_id'],
        'clubs_id' : id
    }
    User.join_club(data)
    return redirect(f"/home/{session['users_id']}")

@app.route('/unjoin/<int:id>')
def unjoin(id):
    data = {
        'id' : id
    }
    Club.leave_club(data)
    return redirect(f'/clubpage/{id}')