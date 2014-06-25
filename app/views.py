from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, s3connection #,oid
from forms import LoginForm
from models import User, ROLE_SPECIALIST, ROLE_ADMIN, EyeImage, Exam
#from sqlalchemy.util import buffer
from s3 import uploadToS3, createBucket, getBucket, doesBucketExist, deleteAllBuckets
from datetime import datetime
import string, random
import traceback, sys


global exams_list
exams_list=[] 

@app.route('/')
@app.route('/select')
def select_study():
    study_list = ['Glaucoma','Trachoma','Diabetic Retinopathy']
    return render_template('study_select.html',study_list=study_list)

@app.route('/deleteAll')
def purge():
    deleteAll()
    study_list = ['Glaucoma','Trachoma','Diabetic Retinopathy']
    return render_template('study_select.html',study_list=study_list)

@app.route('/select/<study_name>')
def fetch_exams(study_name):
    #Return all Exams for which STUDY_NAME == study_name

    exams = Exam.query.all()
    
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

@app.route('/select/<study_name>/<exam_uuid>')
def fetch_single_exam(study_name,exam_uuid):
    #fetch the patient based on the UUID passed in the URL
    exam = Exam.query.filter(Exam.uuid == exam_uuid).first()
    #return render_template('patient.html',patient = {"firstName": "Willem", "lastName": "Dafoe", "mrn":"150", "date": "December 22th 1947","uuid":6843636})

    return render_template('patient.html',exam=exam)

@app.route('/select/<study_name>/<exam_uuid>/<image_uuid>')
def fetch_Single_image(study_name,exam_uuid,image_uuid):
    eyeImage = EyeImage.query.filter(EyeImage.uuid == image_uuid).first()
    #print eyeImage
    exam = eyeImage.exam
    print exam
    return render_template('image.html',eyeImage=eyeImage,exam=exam)

def deleteAll():
  exams = Exam.query.all()
  for exam in exams:
    db.session.delete(exam)
  eyeImages = EyeImage.query.all()
  for eyeImage in eyeImages:
    db.session.delete(eyeImage)
  db.session.commit()
  deleteAllBuckets(s3connection)

@app.route('/exam', methods=['GET','POST'])
#Every Time an Exam is uploaded, an exam object is created
def exam():

  if(request.method == 'GET'):
    exams=Exam.query.all()
    exams_dict={}
    i = 0
    for e in exams:
      exams_dict[str(i)] = str(e)
      i=i+1
    print exams
    return jsonify(exams = exams_dict)
    #return "exams GET"

  else:
    if("firstName" in request.form and request.form["firstName"]):
      fn = request.form["firstName"]
      print fn
    else:
      fn = "Place"
    if("lastName" in request.form and request.form["lastName"]):
      ln = request.form["lastName"]
    else:
      ln = "Holder"
    if("exam_uuid" in request.form):
      exam_uuid = request.form["exam_uuid"]
    else:
      print "PROBLEM WITH EXAM UUID"
      exam_uuid = "666"
    if("date" in request.form):      
      date = request.form["date"]
      print date
    else:
      date = "2000-01-01 11:11:11"

    d = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    print d
    yyyymmddHHMM = d.strftime("%Y-%m-%d-%H-%M")
    print yyyymmddHHMM
    bucketName = (yyyymmddHHMM+"-"+exam_uuid).lower()
    print "BucketName " + bucketName

    val = doesBucketExist(s3connection,bucketName)
    if val is False:
      print "about to create bucket"
      createBucket(s3connection,bucketName)
      #include bucketName in Exam model
      exam = Exam.query.filter(Exam.uuid== exam_uuid).first()  
      if not exam:
        exam = Exam(firstName=fn,lastName=ln,uuid=exam_uuid,bucket=bucketName)#, date=d)
        db.session.add(exam)
        db.session.commit()
        return jsonify(status="Exam Created")
      else:
        return jsonify(status="Exam was a duplicate and was not saved")
    else:
      return jsonify(status="Exam Bucket Already Created")  

    #else:
      #return jsonify(status="Exam was a duplicate and was not saved")

@app.route('/eyeImages', methods=['GET'])
def eyeImage():
  if(request.method == 'GET'):
    eyeImages=EyeImage.query.all()
    eyeImages_dict={}
    i = 0
    for ei in eyeImages:
      eyeImages_dict[str(i)] = str(ei)
      i=i+1
    print eyeImages
    return jsonify(eyeImages = eyeImages_dict)

@app.route('/postImage', methods=['POST','PUT'])
def postImage():

  print "form"+str(request.form)
  print "files"+str(request.files)
    
  exam = Exam.query.filter(Exam.uuid== "008").first()
  if exam:
    print "PASSED THE FIRST PART"
    if("file" in request.files):
      print "FOUND AN IMAGE!!!!!!!"
      bucket = getBucket(s3connection,exam.bucket)
      print bucket
      image = request.files['file']

      imageName = image.filename
      print imageName
      url = uploadToS3(bucket,imageName,image)
      print url
    
    eyeImage = EyeImage(imageURL=url, uuid="111",
      eye=None, fixationLight=None)
    exam.eyeImages.append(eyeImage)
    db.session.add(eyeImage)
    db.session.commit()
    return jsonify(status="EyeImage Created")
  else:
    return jsonify(status="Something Wrong with Exam")

#return jsonify(status="An Image Upload was completed")

@app.route('/uploader', methods=['POST','PUT'])
def uploader():

  print "i am not crazy"
  #bucketName derived from "lastName-firstName-DD-MM-YY-AWS_ACCESS_KEY"
  #print "form"+str(request.form)
  #print "files"+str(request.files)
  
  url = "http://cdn.memegenerator.net/instances/500x/50708036.jpg"
  print "make sure heroku works"

  if "eye" in request.form:
    print "eye was in params"
    eye = request.form["eye"]
  else:
    print "eye wasnt there"
    eye = 'leftEye'
  if "fixationLight" in request.form:
    print "fixationLight was in params"
    print request.form["fixationLight"]
    fixationLight = int(request.form["fixationLight"]) 
  else:
    fixationLight = int(5)
    print "fixationLight wasnt there"

  try:
    if "date" in request.form:
      print "Found a date"
      date = request.form["date"]
    else:
      print "No date found"
      date = "2000-01-01 11:11:11"

    d = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    #print d
    
    if eye == 'OD': #was LEFT
      eyeBool = False
    elif eye == 'OS':  # was RIGHT
      eyeBool = True
    print eyeBool

    print "Before fixationLight"
    if fixationLight == 0:
        fixationText = "Center"
    elif fixationLight == 1:
        fixationText = "Top"
    elif fixationLight == 2:
        fixationText = "Bottom"
    elif fixationLight == 3:
        fixationText = "Left"
    elif fixationLight == 4:
        fixationText = "Right"
    elif fixationLight == 5:
        fixationText = "None"
    else: fixationText = "None Specified"

    #if eye is not "right" or eye is not "left":
      #throw error

    print "Before eyeImage_uuid"  

    if "eyeImage_uuid" in request.form:
      print "eyeImage uuid in form"
      eyeImage_uuid = request.form["eyeImage_uuid"] 
    else:
      print "eyeImage uuid NOT in form"
      eyeImage_uuid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

    #eyeImage_uuid = eyeImage_uuid + + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    #Just removed this 1:17 Wed Am to see if Not a duplicate will print for me 
    #eyeImage = EyeImage.query.filter(EyeImage.uuid == eyeImage_uuid).first()
    #print eyeImage
    #if not eyeImage: #This was indented
    print "NOT A DUPLICATE IMAGE"
    if "exam_uuid" in request.form:
      print "exam_uuid was in form"
      exam_uuid = request.form["exam_uuid"]
    else:
      print "EXAM_UUID INFO IS BROKEN"
      exam_uuid = Exam.query.limit(1).all()[0].uuid
  except:
    print "Exception thrown PRIOR TO S3 CALL"
    print '-'*60
    #print traceback.print_exc(file=sys.stdout)
    print traceback.print_exc()
    print '-'*60


  try: 
    exam = Exam.query.filter(Exam.uuid== exam_uuid).first()
    if not exam:
      return jsonify(status="Exam UUID corrupted, Exam does not exist")
    if("file" in request.files):
      print "FOUND AN IMAGE!!!!!!!"
      bucket = getBucket(s3connection,exam.bucket)
      image = request.files['file']
      imageName = image.filename
      url = uploadToS3(bucket,imageName,image)
      print "S3 URL:" + url   
    eyeImage = EyeImage(imageURL=url, uuid=eyeImage_uuid, eye=eyeBool,fixationLight=fixationLight,image_date=d)
    print eyeImage
    exam.eyeImages.append(eyeImage)
    print "appended eyeImage"
    db.session.add(eyeImage)
    print "added eyeImage to session"
    db.session.commit()
    print "commited the session"
    return jsonify(status="EyeImage Created")

  except:
    print "Exception thrown in S3 upload sequence"
    print '-'*60
    #print traceback.print_exc(file=sys.stdout)
    print traceback.print_exc()
    print '-'*60
    return jsonify(status="Upload Failed")

  
  #else:
  #  return jsonify(status="Something Wrong with Exam")
#else:
  #return jsonify(status="EyeImage was a duplicate and was not saved")
  
  #return jsonify(status="An Image Upload was completed")

'''
@app.route('/psql')
def psql():
'''

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