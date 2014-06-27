from twilio.rest import TwilioRestClient 
 
# put your own credentials here 
ACCOUNT_SID = "AC67afcaf825dddb2791878c24bc5883ec" 
AUTH_TOKEN = "91fd2fc525d70eadd02aa82fc2b9083e" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 

message = client.messages.create(body="Jenny please?! I love you <3",
    to="+14085291354",
    from_="+15104661333")
    #,media_url="http://www.example.com/hearts.png")
print message.sid

def examUploadConfirmation(exam_uuid,phoneNumber):
  client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
  print "INSIDE TWILIO METHOD"
  text= "Thank you for using the Ocular CellScope. Your exam has been uploaded and is being\
  reviewed by a clinician. You may view your exam at www.OCSWebApp.HerokuApp.com/select/glaucoma/"
  +exam_uuid
  message = client.messages.create(body=text,to=phoneNumber,from_="+15104661333")
  print message.sid