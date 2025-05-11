from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired

from data.location import Location
from forms.validators import validate_unique_name, no_invalid_url_chars


class LocationForm(FlaskForm):
    name = StringField("Название локации", validators=[
        DataRequired(message="Введите название"),
        validate_unique_name(Location), no_invalid_url_chars()
    ])
    type = StringField("Тип локации")
    description = TextAreaField("Описание")
    submit = SubmitField("💾 Сохранить локацию")

    def __init__(self, *args, campaign_id=None, obj=None, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.campaign_id = campaign_id
        self.obj = obj