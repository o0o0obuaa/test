from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import Required, Length, Email

class LoginForm(Form):
	username = StringField('username', validators=[Required(), Length(1, 64)])
	password = PasswordField('password', validators=[Required()])
	#remember_me = BooleanField('Keep me logged in')
	submit = SubmitField('Log In')

class UploadForm(Form):
	script_file = FileField('upload file',validators=[Required()])
	submit_upload = SubmitField('Upload')

class RunForm(Form):
	submit_run = SubmitField('Run')
	

	



