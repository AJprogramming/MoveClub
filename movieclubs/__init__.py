from flask import Flask
app = Flask(__name__)

app.secret_key = "This is my key, please don't share it. It's the only one I have :("