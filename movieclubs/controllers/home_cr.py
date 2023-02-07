from movieclubs import app
from movieclubs.models.users_model import User
from movieclubs.models.clubs_model import Club
from flask import render_template, redirect, session

# route

@app.route('/home/<int:id>')
def home(id):
    if 'users_id' not in session:
        return redirect('/login')
    data = {
        "id" : id
    }
    return render_template('/home.html', user=User.get_one(data), joined=User.get_joined_clubs(data), created=Club.get_users_club_list(data))

