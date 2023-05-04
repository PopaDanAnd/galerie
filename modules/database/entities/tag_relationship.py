
from database.common import *

tag_relationships = Table(
    'tag_relationships', Base.metadata,
    Column('post_id', String, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', String, ForeignKey('tags.id'), primary_key=True)
)
