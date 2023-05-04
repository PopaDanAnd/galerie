
from routes.common import *
from database import *
from forms import Form, Field
import forms.validators as validators


class AddTagForm(Form):

    tag_name = Field(
        name='tag_name',
        label='Name',
        validators=[validators.NotEmpty()]
    )

    tag_description = Field(
        name='tag_description',
        label='Description',
        validators=[validators.NotEmpty()]
    )

    def get_tag(self) -> Tag:

        if dbsession.query(Tag).filter(Tag.name == self.tag_name.data).all():
            self.tag_name.errors.append(f'Tag {self.tag_name.data} already exists.')
            return None

        return Tag(
            name=self.tag_name.data,
            description=self.tag_description.data,
        )


@enforce_login
async def admin_route():

    if g.current_account.power_level < 99:
        return redirect(url_for('index_route'))

    accounts = dbsession.query(Account).all()
    tags = dbsession.query(Tag).all()
    return await render_page('admin.html', tags=tags, accounts=accounts)


@enforce_login
async def addtag_route():

    if g.current_account.power_level < 99:
        return jsonify({'errors': 'User is not an admin'})

    form = AddTagForm()
    if await form.load(request):
        tag = form.get_tag()
        if not tag:
            return jsonify({'errors': form.errors})
        dbsession.add(tag)
        dbsession.commit()
        dbsession.refresh(tag)
        return jsonify({'tag': tag.id})
    else:
        return jsonify({'errors': form.errors})


async def remove_tag():
    pass
