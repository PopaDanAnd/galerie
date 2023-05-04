
from routes.common import *
from auth import *


async def logout_route():
    clear_session()
    return redirect(url_for('index_route'))
