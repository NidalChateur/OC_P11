from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(view_func):
    @wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Permission refusée !", "error")
            return redirect(url_for("authentication_app.login"))
        return view_func(*args, **kwargs)

    return decorated_view
