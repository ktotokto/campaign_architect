from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

from data.monster import Monster
from forms.validators import validate_unique_name, no_invalid_url_chars


class MonsterForm(FlaskForm):
    name = StringField("Имя монстра", validators=[
        DataRequired(message="Введите имя монстра"),
        validate_unique_name(Monster), no_invalid_url_chars()
    ])
    monster_type = StringField("Тип монстра", default="Зверь / Нежить / Дракон")
    cr = StringField("CR", default="1/4")
    description = TextAreaField("Описание")
    submit = SubmitField("💾 Сохранить")

    def __init__(self, *args, campaign_id=None, obj=None, **kwargs):
        super(MonsterForm, self).__init__(*args, **kwargs)
        self.campaign_id = campaign_id
        self.obj = obj
