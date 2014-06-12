import boto

def connect(access_id,secret):
  s3connection = boto.connect_s3(access_id,secret)
  return s3connection

def uploadImage(s3connection,mrn,date,imageData):
  patientBucket = s3connection.get_bucket(mrn)
  #For now, pretend
  bucketName = mrn + '_' + date
  b = s3connection.create_bucket(bucketName)
  k = Key(b)
  k.key = bucketName
  k.set_contents_from_file(object, replace = True) # THIS SHOULD NEVER REPLACE
  print "Uploading to " + bucketName + " with key: " + k.key
  k.set_acl('public-read')
  url = k.generate_url(expires_in=999999, query_auth=False)
  t = k.key, url
  return t

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