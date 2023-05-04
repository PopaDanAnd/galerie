
from routes.common import *
from database import *


async def deltag_route(tag_id: int):
    tag = dbsession.query(Tag).filter(Tag.id == tag_id).first()
    if not tag or not g.current_account.power_level == 99:
        return redirect(url_for('admin_route'))

    dbsession.delete(tag)
    dbsession.commit()
    return redirect(url_for('admin_route'))
