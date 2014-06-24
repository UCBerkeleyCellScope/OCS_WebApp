from hashlib import md5
from app import db
ROLE_SPECIALIST = 0
ROLE_ADMIN = 1
ROLE_TECHNICIAN = 2

UNVIEWED= 0

#Cool SQL-Alchemy commands
# user = models.User.query.get(1)
# users = models.User.query.all)
# exams = user.posts.all()
# for e in exams: 
#   print e.exam_date
# models.User.query.order_by('username desc').all()

print "!!!!!!!!!!!!!!! MODELS.PY !!!!!!!!!"

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index = True, unique = True)
  email = db.Column(db.String(120), index = True, unique = True)
  role = db.Column(db.SmallInteger, default = ROLE_SPECIALIST)
  exams = db.relationship('Exam', backref = 'assigned_specialist', lazy = 'dynamic')

  def is_authenticated(self):
      return True #not allowed to authenticate at all

  def is_active(self):
      return True #True unless has been banned

  def is_anonymous(self):
      return False #only True for fake users not supposed to log-in

  def get_id(self):
      return unicode(self.id)  

  def avatar(self,size):
    return 'http://www.gravatar.com/avatar/' + \
    md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

  def __repr__(self):
      return '<User %r>' % (self.username) #how to print objects if you need to print

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    exam_date = db.Column(db.DateTime) #use to be time
    firstName = db.Column(db.String(20))
    lastName = db.Column(db.String(20))
    status = db.Column(db.SmallInteger, default = UNVIEWED)
    diagnosis = db.Column(db.String(300))
    patientID = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #demonstrates the linking
    eyeImages = db.relationship('EyeImage', backref = 'exam', lazy = 'dynamic')
    bucket = db.Column(db.String(80),unique=True)
    uuid = db.Column(db.String(80),unique=True)
    crazy = db.Column(db.String(80))
    #date = db.Column(db.String(40))

    def __init__(self, firstName, lastName, uuid, bucket):
      self.firstName = firstName
      self.lastName = lastName
      self.uuid= uuid
      self.bucket=bucket
      #self.date=date

    def __repr__(self):
        #return '<Exam %r>' % (self.id)
        return '<Exam First Name:{!s} Last Name:{!s} UUID:{!s} # Images:{!s} Bucket:{!s}'\
        .format(self.firstName,self.lastName,self.uuid,self.eyeImages,self.bucket)
        #.format(self.firstName,self.lastName,self.uuid,str(len(self.eyeImages)))
        #return "TESTING"

class EyeImage(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    image_date = db.Column(db.DateTime) #use to be time
    technician = db.Column(db.String(40))
    eye = db.Column(db.Boolean)
    imageURL = db.Column(db.String(200))
    fixationLight = db.Column(db.SmallInteger)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id')) #demonstrates the linking
    #thumbnail = db.Column(db.LargeBinary)
    imageKey = db.Column(db.String(80))
    uuid = db.Column(db.String(80),unique=True)

    def __init__(self, imageURL, uuid, eye, fixationLight):
      self.imageURL = imageURL
      self.uuid = uuid
      self.eye = eye
      self.fixationLight = fixationLight
    

    '''
    def __init__(self, imageURL=None, uuid=None, eye=None, fixationLight=None, thumbnail=None):
      self.imageURL = imageURL
      self.uuid = uuid
      self.eye = eye
      self.fixationLight = fixationLight
      self.thumbnail = thumbnail
    '''

    '''
    def __init__(self, thumbnail):
      self.thumbnail = thumbnail
    '''

    def __repr__(self):
        return '<EyeImage UUID:{!s} Eye:{!s} Fixation:{!s} ImageURL:{!s}>'.format(self.uuid,self.eye,self.fixationLight,self.imageURL)
        #return "test"