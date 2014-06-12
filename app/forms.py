from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required


#LoginForm object is subclassed from class Form
class LoginForm(Form):
    #LoginForm class knows how to produce HTML forms
    #TextField and BooleanField are Field types within WTF-Forms
    #You can have many types of validators, the Required one 
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

    #Where do we define the form method?