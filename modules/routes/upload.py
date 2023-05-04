
from routes.common import *
from auth import *
from forms import Form, Field
import forms.validators as validators
from PIL import Image
import secrets


class UploadForm(Form):

    id = 'upload_form'

    title = Field(
        name='title',
        label='Post title:',
        validators=[validators.NotEmpty()]
    )

    description = Field(
        name='description',
        label='Post description:',
        validators=[]
    )

    tags = Field(
        name='tags',
        label='Post tags:',
        validators=[validators.NotEmpty()]
    )

    file = Field(
        name='file',
        label='Media file:',
        type='file',
        validators=[validators.NotEmpty(), validators.HasExtension(extensions=['png', 'jpg', 'jpeg', 'gif'])]
    )

    submit_text = 'Upload'

    def get_post(self) -> Post:
        tags = string_to_tags(self.tags.data)
        if not tags:
            self.tags.errors.append('Invalid tags.')
            return None

        post = Post(
            title=self.title.data,
            description=self.description.data,
            upload_ts=int(time.time()),
            edit_ts=int(time.time())
        )

        post.tags = tags

        try:
            with Image.open(self.file.data.stream) as img:

                img_token = secrets.token_urlsafe(10)

                media_img = MediaItem(
                    filename=f'{img_token}_{self.title.data}.jpg',
                    mediatype='image'
                )

                media_thumb = MediaItem(
                    filename=f'{img_token}_{self.title.data}.jpg',
                    mediatype='thumb'
                )

                img.save(f'data/img_orig/{img_token}_{self.file.data.filename}')

                img.save(media_img.local_path)
                img.thumbnail((200, 200))
                img.save(media_thumb.local_path)
                post.mediaitems = [media_img, media_thumb]
        except Exception as e:
            self.file.errors.append(f'Error loading image. {e}')
            return None

        return post


def string_to_tags(s: str) -> list:

    res: list = []
    for tag_name in s.split():
        tag = dbsession.query(Tag).filter(Tag.name == tag_name).first()
        if tag:
            res.append(tag)
    return res


@enforce_login
async def upload_route():

    form = UploadForm()
    tags = dbsession.query(Tag).all()

    if request.method == 'GET':
        return await render_page('upload.html', form=form, tags=tags)
    else:
        if await form.load(request):
            post = form.get_post()
            if not post:
                return jsonify({'errors': form.errors}), 400
            post.uploader = g.current_account
            dbsession.add(post)
            dbsession.commit()
            dbsession.refresh(post)
            return jsonify({'post': post.id})
        else:
            return jsonify({'errors': form.errors}), 400
