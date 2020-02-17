from flask import Flask
from flask_cors import CORS, cross_origin

UPLOAD_FOLDER = '/static/textes'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.secret_key = 'dhbjnbhz68Gbzbzbhu'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app, support_credentials=True, resources={r"/*": {"origins": "*"}})



from routes import *

if __name__ == "__main__":
    app.run()
