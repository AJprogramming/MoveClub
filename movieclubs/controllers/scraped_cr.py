from movieclubs import app
from movieclubs.models.scraped_model import Scraped
from flask import render_template, redirect, session

@app.route('/movielist')
def movielist():
    if 'users_id' not in session:
        return redirect('/login')
    return render_template('/movielist.html', allmovies=Scraped.get_movies())