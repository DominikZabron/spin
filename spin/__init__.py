from flask import Flask
from settings import DB_URI

app = Flask(__name__)

import views

app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.debug = True

if '__name__' == "__main__":
    app.run()
