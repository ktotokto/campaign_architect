from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.fields import EmailField
from wtforms.validators import Email
from wtforms import ValidationError

from data.db_session import create_session
from data.user import User


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(),
        Length(min=3, max=25)
    ], render_kw={"placeholder": "Придумайте логин"})

    email = EmailField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=50)
    ], render_kw={"placeholder": "example@example.com"})

    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=6),
    ], render_kw={"placeholder": "Не менее 6 символов"})

    confirm_password = PasswordField('Подтверждение пароля', validators=[
        DataRequired(),
        EqualTo('password', message='Пароли должны совпадать')
    ], render_kw={"placeholder": "Повторите пароль"})

    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, field):
        session = create_session()
        if session.query(User).filter_by(username=field.data).first():
            raise ValidationError('Это имя пользователя уже занято')
        session.commit()

    def validate_email(self, field):
        session = create_session()
        if session.query(User).filter_by(email=field.data).first():
            raise ValidationError('Этот email уже используется')
        session.commit()