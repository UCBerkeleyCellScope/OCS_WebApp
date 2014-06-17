import boto
from boto.s3.key import Key
import string, random

def connect(access_id,secret):
  s3connection = boto.connect_s3(access_id,secret)
  return s3connection

def uploadImage(s3connection,mrn,date,imageData):
  patientBucket = s3connection.get_bucket(mrn)
  #For now, pretend
  bucketName = mrn + '_' + date
  b = s3connection.create_bucket(bucketName)
  k = Key(b)
  bucketName = bucketName+ ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
  k.key = bucketName
  k.set_contents_from_file(object, replace = True) # THIS SHOULD NEVER REPLACE
  print "Uploading to " + bucketName + " with key: " + k.key
  k.set_acl('public-read')
  url = k.generate_url(expires_in=0, query_auth=False)
  t = k.key, url
  return t

def createBucket(s3connection,bucketName):
  b = s3connection.create_bucket(bucketName)
  #check if bucket exists
  #if not, create the bucket
  #return the confirmation

def getBucket(s3connection,bucketName):
  return s3connection.get_bucket(bucketName)

def uploadToS3(bucket,imageName,image):
  k = Key(bucket)
  k.key = imageName
  k.set_contents_from_file(image, replace = True)
  k.set_acl('public-read')
  url = k.generate_url(expires_in=0, query_auth=False)
  return url

def getExam(s3connection,mrn,date):
  bucketName = mrn + '_' + date
  s3connection.get_bucket(bucketName)


  #Go to the bucket
    #Get the sub-bucket
    #list the contents of the sub-bucket


def listKeys(b):
  for x in b.list():
    print x.key()

def gee():
  print "geegeegeegeeBabyBabyBaby"