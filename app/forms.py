from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,TextAreaField
from wtforms.validators import Required,EqualTo,email,ValidationError,DataRequired,Email,Length
from app.models import User
from flask import request
# 定义表单类
class LoginForm(FlaskForm):
    username = StringField('What is your name',validators = [DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',validators=[DataRequired(),EqualTo('password')])
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Register')

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None :
            raise ValidationError('Please user a different name')
    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email')
class EditProfileForm(FlaskForm):
    username = StringField('username',validators= [DataRequired()])
    about_me = TextAreaField('about_me',validators=[Length(min=0,max=140)])
    submit = SubmitField('submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class PostForm(FlaskForm):
    posts = TextAreaField('Say something',validators=[DataRequired(),Length(min=1,max=150)])

    submit = SubmitField('Submit')

# 重置密码请求表单
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('email',validators=[DataRequired(),Email()])
    submit = SubmitField('Submit')
#     重置密码表单
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    password1 = PasswordField('Repeat password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Request Password Reset')



# class SearchForm(FlaskForm):
#     q = StringField(_l('search'),validatirs = [DataRequired()])
#     def __init__(self,*args,**kwargs):
#         if 'formdata' not in kwargs:
#             kwargs['formdata'] = request.args
#         if 'csrf_enabled' not in kwargs:
#             kwargs['csrf_enabled'] = False
#         super(SearchForm,self).__init__(*args,**kwargs)

