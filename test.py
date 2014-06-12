import os
from flask import flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def direct():
  return "Hello World"