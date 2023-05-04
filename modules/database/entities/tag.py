
from database.common import *
from database.entities.tag_relationship import tag_relationships


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), unique=True)
    description = Column(Text, nullable=False)

    posts = relationship(
        'Post',
        secondary=tag_relationships,
        back_populates='tags',
        cascade='all,delete'
    )
