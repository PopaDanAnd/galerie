
import time
from pathlib import Path
from functools import wraps
from quart import Quart, g, render_template, session, redirect, url_for, request, flash, jsonify


def enforce_login(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        if not g.current_account:
            return redirect(url_for('login_route', redirect=url_for(request.endpoint)))
        return await f(*args, **kwargs)
    return decorated_function


def render_page(arg, **kwargs):
    kwargs.update({'current_account': g.current_account})
    return render_template(arg, **kwargs)
