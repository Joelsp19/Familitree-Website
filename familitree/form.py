from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField, SubmitField, BooleanField,SelectField,SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from familitree.models import User,People
from sqlalchemy.sql import text

class RegistrationForm(FlaskForm):
    username=StringField('Username',
            validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',
            validators=[DataRequired(),Email()])
    password=PasswordField('Password',
            validators = [DataRequired(),Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
            validators = [DataRequired(),EqualTo('password')])
            
    submit = SubmitField('Sign Up')
    
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username has already been taken. Please choose another one. ')
        
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('There is already an account with this email.')

   
    
class LoginForm(FlaskForm):
    email = StringField('Email',
            validators=[DataRequired(),Email()])
    password=PasswordField('Password',
            validators = [DataRequired(),Length(min=8)])
    remember = BooleanField('Remember Me')      
    
    submit = SubmitField('Login')
    
    
class UpdateAccountForm(FlaskForm):
    username=StringField('Username',
            validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',
            validators=[DataRequired(),Email()])
    
    picture = FileField('Update Profile Picture', 
                        validators =[FileAllowed(['jpg','png','PNG'])])
    
    submit = SubmitField('Update')
    
    def validate_username(self,username):
        if username.data != current_user.username:            
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username has already been taken. Please choose another one. ')
            
    def validate_email(self,email):
        if email.data != current_user.email:            
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('There is already an account with this email.')



class FamilyForm(FlaskForm):
    
    name_first=StringField('First Name',
            validators=[DataRequired()])
    name_last=StringField(' Last Name',
                validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class KidForm(FlaskForm):
    name_first=StringField('First Name')
    name_last=StringField(' Last Name')
    addKid = BooleanField('Add another Kid')
    deleteKid = BooleanField('Delete this Kid')
    noKid = BooleanField('I have no Kids')
    submit = SubmitField('Submit')

class IsThisYouForm(FlaskForm):
    checkbox = BooleanField('Yes')
    submit = SubmitField('Submit')
    
class AddPersonForm(FlaskForm):
    name_first=StringField('First Name')
    name_last=StringField(' Last Name')
    submit = SubmitField('Submit')
    
class AddRelationshipForm(FlaskForm):
    user_one_id=IntegerField('User 1 ID')
    user_two_id=IntegerField(' User 2 ID')
    relationship_type = SelectField('Your relationship', choices=[('father','father'),('mother',"mother"),('kid','kid'),('brother','brother'),('sister','sister')])
    submit = SubmitField('Submit')
   
    def validate_user_one_id(self,user_one_id):
        myPeopleID=[]
        myPeople = People.query.filter_by(people=current_user).all()
        for p in myPeople:
            myPeopleID.append(p.id)
        user = user_one_id.data in myPeopleID
        ##People.query.filter(People.user_id==user_one_id.data).first()
        if not user:
            raise ValidationError('There is not a person with this id')
    
    def validate_user_two_id(self,user_two_id):
        myPeopleID=[]
        myPeople = People.query.filter_by(people=current_user).all()
        for p in myPeople:
            myPeopleID.append(p.id)
        user = user_two_id.data in myPeopleID
        if not user:
            raise ValidationError('There is not a person with this id')
  
   