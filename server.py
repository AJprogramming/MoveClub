from movieclubs.controllers import login_cr, home_cr, showclubs_cr, createclub_cr, scraped_cr
from movieclubs import app

if __name__ == "__main__":
    app.run(debug=True)