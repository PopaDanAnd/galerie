
from routes.common import *
from database import *


async def delcomment_route(comment_id: int):
    comment = dbsession.query(Comment).filter(Comment.id == comment_id).first()
    if not comment or not g.current_account:
        return redirect(url_for('index_route'))

    if g.current_account != comment.uploader and g.current_account.power_level != 99:
        return redirect(url_for('post_route', post_id=comment.parent_post))

    post_id = comment.parent_id

    dbsession.delete(comment)
    dbsession.commit()
    return redirect(url_for('post_route', post_id=comment.post_id))
