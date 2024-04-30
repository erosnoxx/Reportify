from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.fields import PasswordField
from wtforms.validators import Email, DataRequired, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=100), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=8, max=50)])
    submit = SubmitField('Entrar')
