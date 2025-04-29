from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class CampaignForm(FlaskForm):
    title = StringField('Название преключения', validators=[
        DataRequired('Поле обязательно для заполнения'),
        Length(max=100)
    ], render_kw={"placeholder": "Введите название"})
    system = StringField('Система', render_kw={"placeholder": "Введите систему"})
    description = StringField('Краткое описание', render_kw={"placeholder": "Введите описание"})

    submit = SubmitField('Создать')
