from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

from data.item import Item
from forms.validators import no_invalid_url_chars, validate_unique_name


class ItemForm(FlaskForm):
    name = StringField("Название предмета", validators=[DataRequired(), no_invalid_url_chars(), validate_unique_name(Item)])
    item_type = StringField("Тип")
    rarity = StringField("Редкость")
    description = TextAreaField("Описание")
    weight = FloatField("Вес", default=0.0, validators=[NumberRange(min=0, message="Вес не может быть отрицательным")])
    value = StringField("Стоимость")

    submit = SubmitField("💾 Сохранить предмет")

    def __init__(self, *args, campaign_id=None, obj=None, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.campaign_id = campaign_id
        self.obj = obj
