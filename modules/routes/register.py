from routes.common import *
from auth import *
from forms import Form, Field
import forms.validators as validators


class RegisterForm(Form):

    id = 'register_form'

    username = Field(
        name='username',
        label='Username:',
        validators=[validators.NotEmpty()]
    )

    profile_name = Field(
        name='profile_name',
        label='Profile name:',
        validators=[]
    )

    password = Field(
        name='password',
        label='Password:',
        type='password',
        validators=[validators.NotEmpty()]
    )

    password_confirm = Field(
        name='password_confirm',
        label='Password confirmation:',
        type='password',
        validators=[validators.NotEmpty()]
    )

    def get_account(self) -> Account:
        if dbsession.query(Account).filter(Account.username == self.username.data).first():
            self.username.errors.append(
                f'{ self.username.data } is already used')
        if dbsession.query(Account).filter(Account.profile_name == self.profile_name.data).first():
            self.profile_name.errors.append(
                f'{ self.username.data } is already used.')

        if self.password.data != self.password_confirm.data:
            self.password_confirm.errors.append('Passwords dont match.')

        if len(self.password.data) < 5:
            self.password.errors.append('Password must be 5 characters in length.')

        if not self.profile_name:
            self.profile_name = self.username

        if self.errors:
            return None

        account = Account(
            username=self.username.data,
            profile_name=self.profile_name.data,
            auth_digest=ag2.hash(self.password.data),
            registration_ts=int(time.time()),
            power_level=1 if dbsession.query(Account).all() else 99
        )

        return account


async def register_route():

    if g.current_account:
        return redirect(url_for('index_route'))

    form = RegisterForm()

    if request.method == 'GET':
        return await render_page('register.html', form=form)

    else:
        if await form.load(request):
            account = form.get_account()
            if not account:
                return jsonify({'errors': form.errors}), 400
            dbsession.add(account)
            dbsession.commit()
            return jsonify({'username': account.username})
        else:
            return jsonify({'errors': form.errors}), 400
