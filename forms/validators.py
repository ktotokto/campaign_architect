from flask import flash

from const import INVALID_URL_CHARS
from data.db_session import create_session


def no_invalid_url_chars(message="Недопустимые символы в названии"):
    def _no_invalid_url_chars(form, field):
        value = field.data
        if any(char in INVALID_URL_CHARS for char in value):
            flash(message, 'error')
            field.errors.append(message)
            return False

    return _no_invalid_url_chars


def validate_unique_name(model):
    def _validator(form, field):
        session = create_session()
        try:
            existing = session.query(model).filter(
                model.name == field.data,
                model.campaign_id == form.campaign_id
            ).first()

            if form.obj and existing:
                if (not hasattr(form, 'obj') or existing.id != form.obj.id):
                    flash(f"{model.__name__} с таким именем уже существует в кампании", "error")
                    field.errors.append(f"{model.__name__} с таким именем уже существует в кампании")
                    return False
            elif existing:
                flash(f"{model.__name__} с таким именем уже существует в кампании", "error")
                field.errors.append(f"{model.__name__} с таким именем уже существует в кампании")
                return False
        finally:
            session.close()

    return _validator
