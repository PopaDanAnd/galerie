
from routes.common import *
from database import *


async def index_route():
    posts = dbsession.query(Post).all()
    return await render_page('index.html', posts=posts)
