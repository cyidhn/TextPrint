from flask import Flask

UPLOAD_FOLDER = '/static/textes'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.secret_key = 'dhbjnbhz68Gbzbzbhu'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from routes import *

if __name__ == "__main__":
    app.run()
