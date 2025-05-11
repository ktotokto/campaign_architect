from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from const import SKILL_CHOICES
from data.player import Player
from forms.validators import no_invalid_url_chars, validate_unique_name


class PlayerForm(FlaskForm):
    name = StringField('Имя персонажа', validators=[DataRequired(), no_invalid_url_chars(), validate_unique_name(Player)])
    race = StringField('Раса', validators=[DataRequired()])
    char_class = StringField('Класс', validators=[DataRequired()])
    level = IntegerField('Уровень', validators=[
        DataRequired(),
        NumberRange(min=1, max=20)
    ])
    background = TextAreaField('Предыстория')

    strength = IntegerField('Сила', validators=[NumberRange(min=1, max=30)])
    dexterity = IntegerField('Ловкость', validators=[NumberRange(min=1, max=30)])
    constitution = IntegerField('Телосложение', validators=[NumberRange(min=1, max=30)])
    intelligence = IntegerField('Интеллект', validators=[NumberRange(min=1, max=30)])
    wisdom = IntegerField('Мудрость', validators=[NumberRange(min=1, max=30)])
    charisma = IntegerField('Харизма', validators=[NumberRange(min=1, max=30)])

    skills = SelectMultipleField('Выберите навыки', choices=SKILL_CHOICES)

    submit = SubmitField('Сохранить персонажа')

    def __init__(self, *args, obj=None, campaign_id=None, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        self.campaign_id = campaign_id
        self.obj = obj
