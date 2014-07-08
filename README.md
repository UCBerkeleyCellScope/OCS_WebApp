OCS_WebApp
==========
2013-2014 Capstone Web App
ocswebapp.herokuapp.com

A Flask-based Web Application used to receive exam and image uploads 
from the Ocular CellScope iOS application via a RESTful API

Requirements: Mac OS X 10.7 or later

SETUP

1. Install Pip 
$ sudo  easy_install pip

2. Install virtualenv
$ pip install virtualenv

3. From inside the Git Repo, Create and Activate virtualenv
$ virtualenv venv
$ source venv/bin/activate

4. Set up PostgreSQL for local development and add to $PATH
This web app uses the psycopg2 package in order to work with a PostGres database. In order to install psycopg2 in 
virtualenv, PostGres must be installed on your local machine. The easiest way to do this is to download the 
"PostGres App" at http://postgresapp.com/
After installation, add the Postgres.app resources to your $PATH in order to install psycopg2 in step 5. In accordance with the
PostGres App online documentation (http://postgresapp.com/documentation/cli-tools.html), the command would look 
something like this:
$ export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.3/bin
Test that this worked by running $ psql

5. Install Dependencies in your new virtualenv (dependencies won't be installed system-wide). Note that 
if dependencies are only installed within virtualenv, the environment must be activated
in order for the code to run. 
$ pip install -r requirements.txt
Now use $ pip freeze 
to list all currently installed packages within virtualenv and verify that they match ones listed in requirements.txt 
If psycopg2 throws an error during installation, remove it from requirements.txt and run $pip install -r requirements.txt again
Note: requirements.txt must be included in git on Heroku. Heroku reads the requirements.txt and installs dependencies accordingly

6. Download the Heroku Toolbelt .pkg and install the Toolbelt on your system
https://toolbelt.heroku.com/

7. From the command line, connect to heroku 
$ heroku login
Enter in the CellScope email and Password to connect 

NOTE: git should be established if the repo was cloned, but if you can't cd into
.git then use $git init 

If the heroku remote isn't listed in ./.git/config, use $heroku create
(but this might have redundant side effects because we've already created a heroku git remote)

8. You can now 
$git add <filename>
$git commit -m "add a message here"
$git push heroku master

9. To test that the environment is working, use $python run.py to launch the code locally
If no exceptions are thrown, the app should be available in a browser at localhost:5000

Resouces:
Heroku and Flask: https://devcenter.heroku.com/articles/getting-started-with-python
AWS S3 and Python: http://boto.readthedocs.org/en/latest/ref/s3.html

$foreman start also runs the code

to Exit virtualenv type
$ deactivate

$ Why using gunicorn

jinja is for templating
$ error
$ foreman 

db_migrate.py used when the data model is updated
$ heroku run python db_migrate.py

$ boto AWS commands

Gunicorn dependency

About Heroku
runp-heroku.py, Procfile, and requirements.txt are special files used by Heroku and should not be deleted

Heroku uses git to launch a publicly available version of the Web App. Here are a couple of useful git
$heroku login // this allows you to login and enable git for a specific heroku account
$heroku logs // once logged in, access the logs of the web server
$heroku run python XXX // used to run command line arguments (in this case python XXX) on the heroku side
  // ie $heroku run python db_migrate.py
