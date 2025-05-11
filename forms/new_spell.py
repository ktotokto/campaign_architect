from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

from data.spell import Spell
from forms.validators import no_invalid_url_chars, validate_unique_name


class SpellForm(FlaskForm):
    name = StringField("Название заклинания", validators=[DataRequired(), no_invalid_url_chars(), validate_unique_name(Spell)])
    level = IntegerField("Уровень заклинания", validators=[
        DataRequired(),
        NumberRange(min=0, max=9, message="Уровень от 0 до 9")
    ])
    components = StringField("Компоненты", validators=[Optional()])
    school = StringField("Школа заклинания", validators=[DataRequired()])
    range = IntegerField("Дистанция", validators=[DataRequired(), NumberRange(min=1, max=999, message="Максимум 999")])
    duration = StringField("Длительность", validators=[DataRequired()])
    casting_time = StringField("Время накладывания", validators=[DataRequired()])
    description = TextAreaField("Описание", validators=[DataRequired()])

    submit = SubmitField("💾 Сохранить")

    def __init__(self, *args, obj=None, campaign_id=None, **kwargs):
        super(SpellForm, self).__init__(*args, **kwargs)
        self.campaign_id = campaign_id
        self.obj = obj
