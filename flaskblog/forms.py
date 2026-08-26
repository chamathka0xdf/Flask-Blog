from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField , BooleanField , TextAreaField
from flask_wtf.file import FileAllowed , FileField
from wtforms.validators import DataRequired , Length  , Email  , EqualTo , ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegisterForm(FlaskForm):
    username=StringField(
        "Username",
        validators=[DataRequired(),
                    Length(min=3,max=20)
                    ]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(),
                    Email()
                    ]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(),
                    Length(min=8)
                    ]
    )
    confirm_password=PasswordField(
        "Confirm Password",
        validators=[DataRequired(),
                    Length(min=8),
                    EqualTo("password")
                    ]
    )
    submit =  SubmitField("Sign Up")

    def validate_username(self,username):
        if User.query.filter(User.username == username.data).first():
            raise ValidationError("Username is already taken.")

    def validate_email(self,email):
        if User.query.filter(User.email == email.data).first():
            raise ValidationError("This email is already registered")
class LoginForm(FlaskForm):
    email=StringField(
        "Email",
        validators=[DataRequired(),
                    Email()
                    ]
    )
    password=PasswordField(
        "Password",
        validators=[DataRequired(),
                    Length(min=8)
        ]
    )
    remember= BooleanField("Remember me")
    submit=SubmitField("Login")
class updateForm(FlaskForm):
    profilepic=FileField(
        "Update Profile Picture",
        validators=[FileAllowed(['jpg','png','webp'])]
    )
    username=StringField(
        "Username",
        validators=[DataRequired(),
                    Length(min=3,max=20)
                    ]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(),
                    Email()
                    ]
    )

    submit =  SubmitField("Update")

    def validate_username(self,username):
        if username.data != current_user.username:
            if User.query.filter(User.username == username.data).first():
                raise ValidationError("Username is already taken.")

    def validate_email(self,email):
        if email.data != current_user.email:
            if User.query.filter(User.email == email.data).first():
                raise ValidationError("This email is already registered")



class NewPost(FlaskForm):
    title=StringField("Title",
                      validators=[DataRequired()])
    content=TextAreaField("Content",
                     validators=[DataRequired(),
                                 Length(max=2500)
                                 ]
                          )
    submit=SubmitField("Post")





# TODO : check this validaters using burp