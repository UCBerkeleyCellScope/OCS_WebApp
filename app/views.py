from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, s3connection #,oid
from forms import LoginForm
from models import User, ROLE_SPECIALIST, ROLE_ADMIN, EyeImage, Exam

global exams_list
exams_list=[] 

@app.before_request
def before_request():
    g.user = current_user #current_user is a global variable set by Flask-Login
    #print g.user.username

@app.route('/index')
@login_required
def index():
    user = g.user
    b = s3.get_bucket("cesllscope13")
    for x in b.list:
      print x.key()

    exams = [ # fake array of posts
        { 
            'assigned_specialist': { 'username': 'John' }, 
            'diagnosis': 'Beautiful day in Portland!' 
        },
        { 
            'assigned_specialist': { 'username': 'Susan' }, 
            'diagnosis': 'The Avengers movie was so cool!' 
        },
    ]
    return render_template("index.html",
        title = 'Home',
        user = user,
        exams = exams)
    #Get a list of all the buckets (exams) from S3 then display them
    #If a user clicks on an exam, we'll retrieve that exam

    #Has the user clicked a particular exam? If so, they need to let 
    #everyone else know how much space they need 

'''
@app.route('/login', methods = ['GET', 'POST']) #only GET by default
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
      return redirect(url_for('index')) #if already logged in don't need to re login
      # is used to store and save data during a request
      #url_for(<method_name>) is a clean way to grab the URL for a view function

    form = LoginForm()
    if form.validate_on_submit():
        #this is the flask session
        session['remember_me'] = form.remember_me.data
        #session remains for future requests made by the same client

        #The part handles the redirect to "allow the user to log in"
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
        
        #oid object user authentication
        #'ask for' is a list of data items that we want from the OpenID provider
        #we'll get back from yahoo a username and email hopefully

    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])
      
#This is a callback for OpenID      
@oid.after_login
def after_login(resp):
  #resp has info returned by openID
  if resp.email is None or resp.email == "":
      flash('Invalid login. Please try again.')
      return redirect(url_for('login')) #resp needs to have an email in it
  user = User.query.filter_by(email = resp.email).first() #check the DB for the user
  if user is None:
      nickname = resp.nickname
      if nickname is None or nickname == "":
          nickname = resp.email.split('@')[0]
      user = User(username = nickname, email = resp.email, role = ROLE_SPECIALIST)
      db.session.add(user)
      db.session.commit()
  remember_me = False
  if 'remember_me' in session:
      remember_me = session['remember_me']
      session.pop('remember_me', None)

  login_user(user, remember = remember_me) #This is a Flask-Login function

  return redirect(request.args.get('next') or url_for('index'))
  #if the user tries to access a page without logging in, they are sent over to log-in
  #once successfully logged in, the user will be brought back to this page
'''
@app.route('/')
@app.route('/select')
def select_study():

    study_list = ['Glaucoma','Trachoma','Diabetic Retinopathy']
    return render_template('study_select.html',study_list=study_list)

@app.route('/select/<study_name>')
def fetch_exams(study_name):
    #Return all Exams for which STUDY_NAME == study_name

    '''
    e = Exam(firstName="John", lastName="Smith", uuid="1234")
    ei1 = EyeImage(imageURL="http://cdn.memegenerator.net/instances/500x/50708036.jpg")
    ei2 = EyeImage(imageURL="http://cdn.memegenerator.net/images/240x240/3459374.jpg")
    e.eyeImages.append(ei1)
    e.eyeImages.append(ei2)

    db.session.add(e)
    db.session.add(ei1)
    db.session.add(ei2)
    db.session.commit()
    '''

    exams = Exam.query.all()
    
    if exams is not None:
      for ex in exams:    
        print str(ex.eyeImages)

    if(study_name == "trachoma"):
      patient1= {"firstName": "John", "lastName": "Smith", "mrn":"123", "date": "May 23rd 1990","uuid":8549085094235}
      patient2= {"firstName": "Sally", "lastName": "Johannsen", "mrn":"321", "date": "August 19th 2008","uuid":3209445}
      patient3= {"firstName": "Bruce", "lastName": "Williams", "mrn":"007", "date": "June 20th 1987","uuid":8543758943}

    else:
      patient1= {"firstName": "Martin", "lastName": "Scorcese", "mrn":"678", "date": "May 99rd 1997","uuid":804525211}
      patient2= {"firstName": "Scarlet", "lastName": "Jenkins", "mrn":"1337", "date": "July 19th 2108","uuid":96592662}
      patient3= {"firstName": "Willem", "lastName": "Dafoe", "mrn":"150", "date": "December 22th 1947","uuid":6843636}
    
    global exams_list
    exams_list=[patient1,patient2,patient3]
    return render_template('exams.html', exams_list=exams_list, exams = exams)


@app.route('/select/<study_name>/<uuid>')
def fetch_single_exam(study_name,uuid):
    #fetch the patient based on the UUID passed in the URL
    exam = Exam.query.filter(Exam.uuid == uuid).first()

    #return render_template('patient.html',patient = {"firstName": "Willem", "lastName": "Dafoe", "mrn":"150", "date": "December 22th 1947","uuid":6843636})
    return render_template('patient.html',exam=exam)

@app.route('/select/<study_name>/<exam_uuid>/<image_uuid>')
def fetch_Single_image(study_name,exam_uuid,image_uuid):
    eyeImage = EyeImage.quer.filter(EyeImage.uuid == image_uuid).first()
    return render_template('image.html',eyeImage=eyeImage)

def deleteAll():
  exams = Exam.query.all()
  for exam in exams:
    db.session.delete(exam)
  eyeImages = EyeImage.query.all()
  for eyeImage in eyeImages:
    db.session.delete(eyeImage)
  db.session.commit()

@app.route('/test', methods=['GET','POST'])
def test():
  if(request.method=="POST"):
    print "args"+str(request.args)
    print "form"+str(request.form)

    print "values"+str(request.values)
    print "data"+str(request.data)

    return request.form["firstName"]

    #return str(request.values["firstName"])
    #return "OMG POST\n"
  else:
    return "HOLY MOLY\n"

@app.route('/exam', methods=['GET','POST'])
#Every Time an Exam is uploaded, an exam object is created
def exam():

  if request.method == 'GET':
    print "OMG GET REQUEST"

  else:

    if("firstName" in request.form):
      fn = request.form["firstName"]
      print fn
    if("lastName" in request.form):
      ln = request.form["lastName"]
    if("exam_uuid" in request.form):
      exam_uuid = request.form["exam_uuid"]
    if("date" in request.form):      
      date = request.form["date"]

    #should avoid using boto as much as possible for speed!!!!!!!!!!!!

    #???should 
    #BUCKET = exam
    #bucket has many keys.. which are images

    #study_name = request.form["study_name"]

    #Create string uuid+
    #bucketName = app.config['AWS_ACCESS_KEY_ID']
    
    if(fn is None or ln is None):
      bucketName = date+"-"+exam_uuid
      fn = "Place"
      ln = "Holder"
    else:
      bucketName = date+"-"+ln+"-"+fn+"-"+exam_uuid

    '''
    b = s3connection.lookup(bucketName) 

    if(b is None):
      b = s3connection.create_bucket(bucket_Name = bucketName)
    '''

    exam = Exam.query.filter(Exam.uuid == exam_uuid).first()
    if not exam:
      exam = Exam(firstName=fn,lastName=ln,uuid=exam_uuid)
      db.session.add(exam)
      db.session.commit()
      return jsonify(status="Exam Created")
    else:
      return jsonify(status="Exam was a duplicate and was not saved")
    #NEED TO RETURN REFERENCE TO B SOMEHOW!   

  #2002-01-31-LAST-FIRST-UUID

@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
  if request.method =='POST':
    #bucketName derived from "lastName-firstName-DD-MM-YY-AWS_ACCESS_KEY"
    #create bucket(bucketName) #Can try to create, even if already created

    #create an exam element

    #note that exam_uuid also has firstName, lastName
    mrn = request.form["mrn"]

    eye = request.form["eye"]
    fixationLight = request.form["fixationLight"]
    exam_uuid = request.form["exam_uuid"]
    exam = Exam.query.filter(uuid== exam_uuid).first()
   
    eyeImage_uuid = request.form["eyeImage_uuid"] 
    url = "http://cdn.memegenerator.net/instances/500x/50708036.jpg"
    eyeImage = EyeImage(imageURL=url, uuid=eyeImage_uuid, eye=eye,
      fixationLight=fixationLight, thumbnail=request.files["thumbnail"])
    print eyeImage

    exam.eyeImages.append(eyeImage)

    db.session.add(eyeImage)
    db.session.commit()

  return jsonify(status="Upload Completed")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@lm.user_loader
def load_user(id):
  return User.query.get(int(id))
  #User IDs in Flask-Login are always unicode strings, so
  #convert the string into an integer every time eyou come o Python with data

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first()
    if user == None:
        flash('User ' + username + ' not found.') #note don't have to pass flash messages
        return redirect(url_for('index'))
    exams = [
        { 'assigned_specialist': user, 'diagnosis': 'Test post #1' },
        { 'assigned_specialist': user, 'diagnosis': 'Test post #2' }
    ]
    return render_template('user.html',
        user = user,
        exams = exams)