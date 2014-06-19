import os
basedir = os.path.abspath(os.path.dirname(__file__)) #directory of config.py

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')#join is like +

AWS_ACCESS_KEY_ID='AKIAIZJCDD43UTMHGLXQ'
AWS_SECRET_ACCESS_KEY='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'

CSRF_ENABLED = True #prevent corss-site request forgery
SECRET_KEY = 'you-will-never-guess' #only needed when CSRF is CSRF_ENABLED
#the Key is used to create a cryptographic token that is used to validate a form

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

