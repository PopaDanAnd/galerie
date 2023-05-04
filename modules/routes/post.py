
from routes.common import *
from database import *


async def post_route(post_id: int):
    post = dbsession.query(Post).filter(Post.id == post_id).first()
    if not post:
        return '404', 404
    post.views = post.views + 1
    replies = dbsession.query(Comment).filter(and_(Comment.parent_id == None, Comment.post_id == post.id)).all()
    dbsession.commit()
    return await render_page('post.html', post=post, replies=replies)
