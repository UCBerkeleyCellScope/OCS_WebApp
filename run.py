#!/usr/local/bin/python
from app import app #from the app folder import the app object (from init) 
app.run('0.0.0.0', debug=True, threaded=True)
#this is the path to the interpreter
#./run.py: flask/bin/python: bad interpreter: No such file or directory