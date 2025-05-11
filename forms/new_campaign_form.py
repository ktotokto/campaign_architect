from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from forms.validators import no_invalid_url_chars


class CampaignForm(FlaskForm):
    title = StringField('Название преключения', validators=[
        DataRequired('Поле обязательно для заполнения'),
        Length(max=100), no_invalid_url_chars()
    ], render_kw={"placeholder": "Введите название"})
    system = StringField('Система', render_kw={"placeholder": "Введите систему"})
    description = StringField('Краткое описание', render_kw={"placeholder": "Введите описание"})

    submit = SubmitField('Создать')
