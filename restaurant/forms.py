from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, Regexp


class RegisterForm(FlaskForm):
    username = StringField(label = 'username', validators = [Length(min = 2, max = 30), DataRequired()])
    fullname = StringField(label = 'fullname', validators = [Length(min=3, max = 30), DataRequired()])
    email = StringField(label = 'email', validators = [Length(min=3, max = 30),Email(), DataRequired()])
    address = StringField(label = 'address', validators = [Length(min=7, max = 50), DataRequired()])
    phone_number = StringField(label = 'phone_number', validators = [DataRequired(),Regexp(r'^\d{10}$', message="Enter a valid 10-digit phone number")]) #try to find phone
    password1 = PasswordField(label = 'password1', validators = [Length(min = 6), DataRequired()])
    password2 = PasswordField(label = 'password2', validators = [EqualTo('password1'), DataRequired()])
    submit = SubmitField(label = 'Sign Up')

class LoginForm(FlaskForm):
    username = StringField(label = 'username', validators = [DataRequired()])
    password = PasswordField(label = 'password', validators = [DataRequired()])
    submit = SubmitField(label = 'Sign In')

class OrderIDForm(FlaskForm):
    orderid = StringField(label ='order-id', validators = [Length(min = 1), DataRequired()])      
    submit = SubmitField(label = 'Track')

class ReserveForm(FlaskForm):
    submit = SubmitField(label = 'Reserve')

class AddForm(FlaskForm):
    submit = SubmitField(label = 'Add')
    
class OrderForm(FlaskForm):
    submit = SubmitField(label = 'Order Now')

class PaymentForm(FlaskForm):
    submit = SubmitField(label = 'Pay Now')