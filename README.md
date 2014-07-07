OCS_WebApp
==========

2013-2014 Capstone Web App

A Flask-based Web Application used to receive exam and image uploads 
from the Ocular CellScope iOS application via a RESTful API

SETUP

1. In a "bash" window on Terminal, install HomeBrew. 
http://brew.sh/ Scroll down to "Install Homebrew" and enter the Ruby command 
into the terminal

1. Install Pip 
$ sudo  easy_install pip

2. Install virtualenv
$ pip install virtualenv

3. From inside the Git Repo, Create and Activate virtualenv
$ virtualenv venv
$ source venv/bin/activate

4. Install Dependencies in your new virtualenv (dependencies won't be installed system-wide). Note that if dependencies are only installed within virtualenv, the environment must be activated
in order for the code to run.
$ pip install -r requirements.txt

5. Download the Heroku Toolbelt .pkg and install the Toolbelt on your system
https://toolbelt.heroku.com/

6. From the command line, connect to heroku 
$ heroku login

7. Enter in the CellScope email and Password to connect 

8. Can now 
$git add <filename>
$git commit -m "add a message here"
$git push heroku master

$python run.py runs the code locally

$foreman start also runs the code

to Exit virtualenv type
$ deactivate



app/

/static