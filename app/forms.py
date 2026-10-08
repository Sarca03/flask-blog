from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Korisničko ime', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email adresa', validators=[DataRequired(), Email()])
    password = PasswordField('Lozinka', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Potvrdi lozinku', validators=[DataRequired(), EqualTo('password', message='Lozinke se moraju poklapati.')])
    submit = SubmitField('Registruj se')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ovo korisničko ime je već zauzeto. Izaberi drugo.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Nalog sa ovim email-om već postoji.')


class LoginForm(FlaskForm):
    email = StringField('Email adresa', validators=[DataRequired(), Email()])
    password = PasswordField('Lozinka', validators=[DataRequired()])
    remember = BooleanField('Zapamti me')
    submit = SubmitField('Prijavi se')


class PostForm(FlaskForm):
    title = StringField('Naslov članka', validators=[DataRequired(), Length(max=150)])
    subtitle = StringField('Podnaslov (opciono)', validators=[Length(max=200)])
    content = TextAreaField('Sadržaj članka', validators=[DataRequired()])
    submit = SubmitField('Objavi članak')


class CommentForm(FlaskForm):
    content = TextAreaField('Komentar', validators=[DataRequired(), Length(min=1, max=500)])
    submit = SubmitField('Pošalji komentar')