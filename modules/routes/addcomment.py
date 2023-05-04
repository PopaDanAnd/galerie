from routes.common import *
from auth import *
from forms import Form, Field
import forms.validators as validators


class CommentForm(Form):

    id = 'comment_form'

    parent_id = Field(
        name='parent_id'
    )

    text_body = Field(
        name='text_body',
        validators=[validators.NotEmpty()]
    )


async def addcomment_route(post_id: int):

    form = CommentForm()

    if not g.current_account:
        return jsonify({'errors': 'Not logged in.'}), 400

    post = dbsession.query(Post).filter(Post.id == post_id).first()

    if await form.load(request):
        for f in form.fields:
            print(f.data)
        parent_comment = dbsession.query(Comment).filter(Comment.id == form.parent_id.data).first()

        comment = Comment(
            content=form.text_body.data
        )

        if parent_comment:
            if parent_comment.post_id != post_id:
                return jsonify({'errors': {'parent_id': "Comment doesnt exist."}}), 400
            parent_comment.replies.append(comment)

        post.replies.append(comment)

        comment.uploader = g.current_account

        dbsession.add(comment)
        dbsession.commit()
        dbsession.refresh(comment)

        return jsonify({'comment_id': comment.id})

    else:
        return jsonify({'errors': form.errors}), 400
