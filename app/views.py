from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, s3connection #,oid
from forms import LoginForm
from models import User, ROLE_SPECIALIST, ROLE_ADMIN, EyeImage, Exam
#from sqlalchemy.util import buffer
from s3 import uploadToS3, createBucket, getBucket, doesBucketExist, deleteAllBuckets
from send import examUploadConfirmation
import calendar
from datetime import datetime, timedelta
import string, random, re
import traceback, sys

@app.route('/')
@app.route('/select/')
def select_study():
    study_list = ['Glaucoma','Trachoma','Diabetic Retinopathy']
    return render_template('study_select.html',study_list=study_list)

@app.route('/deleteAll')
def purge():
    deleteAll()
    study_list = ['Glaucoma','Trachoma','Diabetic Retinopathy']
    return render_template('study_select.html',study_list=study_list)

@app.route('/select/<study_name>/')
def fetch_exams(study_name):
    #Return all Exams for which STUDY_NAME == study_name

    exams = Exam.query.order_by(Exam.exam_date.desc())
    
    '''
    for e in exams:
      e.exam_date = utc_to_local(e.exam_date)
      print e.exam_date
    '''

    return render_template('exams.html', exams = exams)

def utc_to_local(utc_dt):
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)

'''
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                               'favicon.ico', mimetype='image/png')
'''

@app.route('/select/<study_name>/<exam_uuid>/',methods=['POST','GET'])
def fetch_single_exam(study_name,exam_uuid):
    
    if(request.method == 'POST'): 
      exam = Exam.query.filter(Exam.uuid == exam_uuid).first()
      if "diagnosis" in request.form:
        print "diagnosis Found"
        print  request.form["diagnosis"] 
        exam.diagnosis = request.form["diagnosis"]
        db.session.commit()
      else:
        print "NO DIAGNOSIS FOUND"

    exam = Exam.query.filter(Exam.uuid == exam_uuid).first()

    return render_template('patient.html',exam=exam)

    #fetch the patient based on the UUID passed in the URL
    #exam = Exam.query.filter(Exam.uuid == exam_uuid).first()
    #return render_template('patient.html',patient = {"firstName": "Willem", "lastName": "Dafoe", "mrn":"150", "date": "December 22th 1947","uuid":6843636})
    
@app.route('/select/<study_name>/<exam_uuid>/<image_uuid>/')
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
    
    try:
      if("phoneNumber" in request.form and request.form["phoneNumber"]):      
        phoneNumber = request.form["phoneNumber"]
        print phoneNumber
        phoneNumber = re.sub(r'[^\w]','',phoneNumber)
        #phoneNumber = phoneNumber.translate(None,'()-')
        print phoneNumber
      else:
        phoneNumber = "4085291354"
        print phoneNumber
    except:
      print "Exception in PHONE NUMBER"
      print '-'*60
      #print traceback.print_exc(file=sys.stdout)
      print traceback.print_exc()
      print '-'*60

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
        exam = Exam(firstName=fn,lastName=ln,uuid=exam_uuid,bucket=bucketName, exam_date=d, phoneNumber = phoneNumber)
        db.session.add(exam)
        db.session.commit()
        try:
          examUploadConfirmation(exam_uuid,phoneNumber)
        except:
          print '-'*60
          print "SOMETHING WRONG WITH TWILIO"
          print traceback.print_exc()
          print '-'*60
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

  #bucketName derived from "lastName-firstName-DD-MM-YY-AWS_ACCESS_KEY"
  #print "form"+str(request.form)
  #print "files"+str(request.files)
  
  url = "http://cdn.memegenerator.net/instances/500x/50708036.jpg"

  if "eye" in request.form:
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
    if fixationLight == 1:
        fixationText = "Center"
    elif fixationLight == 2:
        fixationText = "Top"
    elif fixationLight == 3:
        fixationText = "Bottom"
    elif fixationLight == 4:
        fixationText = "Left"
    elif fixationLight == 5:
        fixationText = "Right"
    elif fixationLight == 6:
        fixationText = "None"
    else: fixationText = "None Specified"

    #if eye is not "right" or eye is not "left":
      #throw error

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
    eyeImage = EyeImage(imageURL=url, uuid=eyeImage_uuid, eyeString=eye,fixationText=fixationText,image_date=d)
    print eyeImage
    exam.eyeImages.append(eyeImage)
    db.session.add(eyeImage)
    db.session.commit()
    return jsonify(status="EyeImage Created")

  except:
    print "Exception thrown in S3 upload sequence"
    print '-'*60
    #print traceback.print_exc(file=sys.stdout)
    print traceback.print_exc()
    print '-'*60
    return jsonify(status="Image Upload Failed")

  #else:
  #  return jsonify(status="Something Wrong with Exam")
#else:
  #return jsonify(status="EyeImage was a duplicate and was not saved")
  
  #return jsonify(status="An Image Upload was completed")
