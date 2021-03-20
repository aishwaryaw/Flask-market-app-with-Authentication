from wtforms import StringField, PasswordField, SubmitField, HiddenField
from flask_wtf import FlaskForm
from wtforms.validators import Email, Length, EqualTo, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')
    
    def validate_email_address(self, email_address_to_check):
        user = User.query.filter_by(email_address=email_address_to_check.data).first()
        if user:
            raise ValidationError('Email address already exists! Please try a different email address')



    username = StringField(label='Username:', validators=[Length(min=2, max=30,message='Username must be between 2 and 30 characters long'), DataRequired(message='Username is required')])
    password1 = PasswordField(label='Password:', validators=[Length(min=6,message='Password must be at least 6 characters long'), DataRequired(message='Password is required')])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1', message='Password should match'),DataRequired(message='Confirm password is required')])
    email_address = StringField(label='Email Address:', validators=[Email(message='Email must be valid'), DataRequired(message='Email address is required')])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired(message='Username is required')])
    password = PasswordField(label='Password:', validators=[DataRequired(message='Password is required')])
    submit = SubmitField(label='Login')


class PurchaseForm(FlaskForm):
    submit = SubmitField(label='Purchase Item !')

class SellingForm(FlaskForm):
    submit=SubmitField(label='Sell Item !')