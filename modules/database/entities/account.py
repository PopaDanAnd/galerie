
from database.common import *


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    profile_name = Column(String(128), unique=True)
    description = Column(Text)

    auth_digest = Column(String(256), nullable=False)
    registration_ts = Column(Integer, nullable=False)

    power_level = Column(Integer, default=0, nullable=False)

    posts = relationship(
        'Post',
        cascade='all, delete'
    )

    replies = relationship(
        'Comment',
        cascade='all, delete'
    )

    session_tokens = relationship(
        'SessionToken',
        cascade='all, delete'
    )

    avatars = relationship(
        'MediaItem',
        cascade='all, delete'
    )
