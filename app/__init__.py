from flask import Flask
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
import s3

#before code is run, special variables are defined
#if source file is the main program, it sets a special 
#__name__ variable to be __main__
#if the file is a module that's imported into main, then
#from within the module, __name__ = <name of the module>

#Do the __name__ = __main__ so that the main method
#is only executed when the script is run directly instead
#of being imported

#with is like try..finally (finally being clean-up code)

app = Flask(__name__) #application object of class Flask 
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)

#oid = OpenID(app, os.path.join(basedir, 'tmp'))
lm.login_view = 'login'

s3connection = s3.connect(app.config['AWS_ACCESS_KEY_ID'], app.config['AWS_SECRET_ACCESS_KEY'])

from app import views, models

#classes are database models
#ORM maps objects in classes into rows in a databse table