
from routes.common import *


async def profile_route():
    if not g.current_account:
        return redirect(url_for('login_route'))
    return str(g.current_account.username)
