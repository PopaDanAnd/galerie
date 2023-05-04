
from routes.common import *
from database import *


async def profile_route(username: str):
    account = dbsession.query(Account).filter(Account.username == username).first()
    if not account:
        return '404', 404
    return await render_page('profile.html', account=account)

