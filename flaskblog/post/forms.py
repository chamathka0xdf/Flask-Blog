from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired , Length

class NewPost(FlaskForm):
    title=StringField("Title",
                      validators=[DataRequired()])
    content=TextAreaField("Content",
                     validators=[DataRequired(),
                                 Length(max=2500)
                                 ]
                          )
    submit=SubmitField("Post")