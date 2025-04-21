from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired('Поле обязательно для заполнения'),
        Length(min=3, max=25)
    ], render_kw={"placeholder": "Введите ваш логин"})

    password = PasswordField('Пароль', validators=[
        DataRequired('Поле обязательно для заполнения'),
        Length(min=6)
    ], render_kw={"placeholder": "Введите ваш пароль"})

    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')