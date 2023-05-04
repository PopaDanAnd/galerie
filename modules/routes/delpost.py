
from routes.common import *
from database import *


async def delpost_route(post_id: int):
    post = dbsession.query(Post).filter(Post.id == post_id).first()
    if not post or not g.current_account:
        return redirect(url_for('index_route'))

    if g.current_account != post.uploader and g.current_account.power_level != 99:
        return redirect(url_for('index_route'))

    dbsession.delete(post)
    dbsession.commit()
    return redirect(url_for('profile_route', username=g.current_account.username))
