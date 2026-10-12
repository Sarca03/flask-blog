from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Korisničko ime', validators=[DataRequired(message='Ovo polje je obavezno.'), Length(min=2, max=50, message='Korisničko ime mora imati od 2 do 50 znakova.')])
    email = StringField('Email adresa', validators=[DataRequired(message='Ovo polje je obavezno.'), Email(message='Unesi ispravnu email adresu.')])
    password = PasswordField('Lozinka', validators=[DataRequired(message='Ovo polje je obavezno.'), Length(min=6, message='Lozinka mora imati bar 6 znakova.')])
    confirm_password = PasswordField('Potvrdi lozinku', validators=[DataRequired(message='Ovo polje je obavezno.'), EqualTo('password', message='Lozinke se moraju poklapati.')])
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
    email = StringField('Email adresa', validators=[DataRequired(message='Ovo polje je obavezno.'), Email(message='Unesi ispravnu email adresu.')])
    password = PasswordField('Lozinka', validators=[DataRequired(message='Ovo polje je obavezno.')])
    remember = BooleanField('Zapamti me')
    submit = SubmitField('Prijavi se')


class PostForm(FlaskForm):
    title = StringField('Naslov članka', validators=[DataRequired(message='Ovo polje je obavezno.'), Length(max=150, message='Naslov može imati najviše 150 znakova.')])
    subtitle = StringField('Podnaslov (opciono)', validators=[Length(max=200, message='Podnaslov može imati najviše 200 znakova.')])
    content = TextAreaField('Sadržaj članka', validators=[DataRequired(message='Ovo polje je obavezno.')])
    submit = SubmitField('Objavi članak')


class CommentForm(FlaskForm):
    content = TextAreaField('Komentar', validators=[DataRequired(message='Ovo polje je obavezno.'), Length(max=500, message='Komentar može imati najviše 500 znakova.')])
    submit = SubmitField('Pošalji komentar')