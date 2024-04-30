from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class OTPForm(FlaskForm):
    otp1 = StringField('OTP 1', validators=[DataRequired(), Length(min=1, max=1)])
    otp2 = StringField('OTP 2', validators=[DataRequired(), Length(min=1, max=1)])
    otp3 = StringField('OTP 3', validators=[DataRequired(), Length(min=1, max=1)])
    otp4 = StringField('OTP 4', validators=[DataRequired(), Length(min=1, max=1)])
    otp5 = StringField('OTP 5', validators=[DataRequired(), Length(min=1, max=1)])
    otp6 = StringField('OTP 6', validators=[DataRequired(), Length(min=1, max=1)])
    submit = SubmitField('Verificar')
