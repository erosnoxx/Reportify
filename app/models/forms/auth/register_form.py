from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField, DateField
from wtforms.validators import Email, DataRequired, Length


class RegisterForm(FlaskForm):
    first_name = StringField('Nome', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Sobrenome', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Length(min=5, max=100), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=8, max=50)])
    date_of_birth = DateField('Data de Nascimento', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')
