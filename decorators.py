from functools import wraps

from flask import flash, redirect, url_for

from const import INVALID_URL_CHARS


def sanitize_title(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        title = kwargs.get("title")
        if title and any(c in title for c in INVALID_URL_CHARS):
            flash("Недопустимые символы", "error")
            return redirect(url_for("campaigns"))
        return f(*args, **kwargs)

    return decorated_function