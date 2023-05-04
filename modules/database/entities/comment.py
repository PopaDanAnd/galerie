
from database.common import *


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    parent_id = Column(Integer, ForeignKey('comments.id'))
    uploader_id = Column(Integer, ForeignKey('accounts.id'))

    content = Column(Text, nullable=False)

    upload_ts = Column(Integer, nullable=False)
    edit_ts = Column(Integer)

    parent_post = relationship(
        'Post',
        uselist=False
    )

    parent_reply = relationship(
        'Comment',
        remote_side=[id],
        back_populates='replies',
        uselist=False
    )

    replies = relationship(
        'Comment',
        back_populates='parent_reply',
        cascade='all, delete'
    )

    uploader = relationship(
        'Account',
        uselist=False
    )
