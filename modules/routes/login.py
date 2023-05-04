from routes.common import *
from auth import *
from forms import Form, Field
import forms.validators as validators


class LoginForm(Form):

    id = 'login_form'

    username = Field(
        name='username',
        label='Username:',
        validators=[validators.NotEmpty()]
    )

    password = Field(
        name='password',
        label='Password:',
        type='password',
        validators=[validators.NotEmpty()]
    )

    remember = Field(
        name='remember',
        label='Remember login',
        type='checkbox',
        validators=[]
    )

    submit_text: str = 'Log in'

    def get_account(self) -> Account:

        account = dbsession.query(Account).filter(
            Account.username == self.username.data).first()

        if not account:
            self.username.errors.append('Invalid username.')
            return None

        try:
            ag2.verify(account.auth_digest, self.password.data)
        except:
            self.password.errors.append('Invalid password.')
            return None
        else:
            return account


async def login_route():

    if g.current_account:
        return redirect(url_for('index_route'))

    form = LoginForm()

    if request.method == 'GET':
        return await render_page('login.html', form=form)

    else:
        if await form.load(request):
            account = form.get_account()
            if not account:
                return jsonify({'errors': form.errors}), 400
            generate_token_for_account(account)
            return jsonify({'username': account.username})
        else:
            return jsonify({'errors': form.errors}), 400
