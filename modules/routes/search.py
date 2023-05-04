
from routes.common import *
from database import *
from forms import Form, Field, validators


def get_posts_by_tags(tags: list):
    return dbsession.query(Post).join(Post.tags).filter(Tag.id.in_([tag.id for tag in tags])).group_by(Post.id).having(func.count(Tag.id) == len(tags))


class SearchForm(Form):

    tag_list = Field(
        name='tag_list',
        placeholders='Search for multiple tags',
    )

    def get_posts(self):
        tags: list = []
        for tag_name in self.tag_list.data.split():
            tag = dbsession.query(Tag).filter(Tag.name == tag_name).first()
            if tag:
                tags.append(tag)

        if not tags:
            return None, None
        return get_posts_by_tags(tags), tags


async def search_route():
    form = SearchForm()
    if await form.load(request):
        posts, tags = form.get_posts()
        return await render_page('index.html', posts=posts, tags=tags)
    else:
        return jsonify({'errors': form.errors})
