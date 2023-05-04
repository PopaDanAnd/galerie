
from database.common import *


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('posts.id'))

    title = Column(String(256), nullable=False)
    description = Column(Text)
    uploader_id = Column(Integer, ForeignKey('accounts.id'))
    views = Column(Integer, default=0)

    upload_ts = Column(Integer, nullable=False)
    edit_ts = Column(Integer)
    visibility = Column(Integer, nullable=False, default=1)
    # 0 = public, 1 = unlisted, 2 = requires_login, 3 = hidden

    parent_post = relationship(
        'Post',
        remote_side=[id],
        back_populates='child_posts',
        uselist=False
    )

    child_posts = relationship(
        'Post',
        back_populates='parent_post'
    )

    tags = relationship(
        'Tag',
        secondary='tag_relationships',
        back_populates='posts'
    )

    mediaitems = relationship(
        'MediaItem',
        cascade='all, delete'
    )

    uploader = relationship(
        'Account',
        uselist=False
    )

    replies = relationship(
        'Comment',
        cascade='all, delete'
    )
