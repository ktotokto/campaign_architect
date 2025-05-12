from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

from data.event import Event
from forms.validators import no_invalid_url_chars, validate_unique_name


class EventForm(FlaskForm):
    name = StringField("Название события", validators=[DataRequired(), no_invalid_url_chars(), validate_unique_name(Event)])
    description = TextAreaField("Описание события", validators=[DataRequired()])

    submit = SubmitField("Сохранить")

    def __init__(self, *args, campaign_id=None, obj=None, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.campaign_id = campaign_id
        self.obj = obj
