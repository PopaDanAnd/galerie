
from routes.common import *
from auth import *
from forms import Form, Field
import forms.validators as validators
from PIL import Image
import secrets


class EditProfileForm(Form):

    id = 'editprofile_form'

    username = Field(
        name='username',
        label='New username:'
    )

    profile_name = Field(
        name='profile_name',
        label='New profile name:'
    )

    avatar = Field(
        name='avatar',
        label='New avatar:',
        type='file',
        validators=[validators.HasExtension(extensions=['png', 'jpg', 'jpeg'])]
    )

    new_password = Field(
        name='new_password',
        label='New password:',
        type='password'
    )

    new_password_confirm = Field(
        name='new_password_confirm',
        label='New password confirmation:',
        type='password'
    )
    
    password = Field(
        name='password',
        label='Current password:',
        type='password',
        validators = [validators.NotEmpty(message="Password required.")]
    )

    submit_text = 'Edit profile'

    def update_account(self, account:Account) -> None:
       
        new_pass_hash: str = None
         
        if self.username.data:
            if dbsession.query(Account).filter(Account.username == self.username.data).first():
                self.username.errors.append(f'{ self.username.data } is already used')
            else:
                account.username = self.username.data
        
        if self.profile_name.data:
            if dbsession.query(Account).filter(Account.profile_name == self.profile_name.data).first():
                self.profile_name.errors.append(f'{ self.profile_name.data } is already used.')
            else:
                account.profile_name = self.profile_name.data
            
        if self.new_password.data: 
            if self.new_password.data != self.new_password_confirm.data:
                self.new_password_confirm.errors.append('Passwords dont match.')

            if len(self.new_password.data) < 5:
                self.new_password.errors.append('Password must be 5 characters in length.')
            
            new_pass_hash = ag2.hash(self.new_password.data)


        if self.avatar.data: 
            try:
                with Image.open(self.avatar.data.stream) as img:

                    img_token = secrets.token_urlsafe(10)

                    avatar = MediaItem(
                        filename=f'{img_token}_avatar.jpg',
                        mediatype='avatar'
                    )

                    img.thumbnail((200, 200))
                    img.save(avatar.local_path)

                    if account.avatar:
                        dbsession.delete(account.avatar)

                    account.avatar = avatar

            except Exception as e:
                self.avatar.errors.append(f'Error loading image. {e}')

        try:
            ag2.verify(account.auth_digest, self.password.data)
        except:
            self.password.errors.append('Invalid password.')
 
        if new_pass_hash:
            account.auth_digest = new_pass_hash

@enforce_login
async def editprofile_route():

    form = EditProfileForm()

    if request.method == 'GET':
        return await render_page('editprofile.html', form=form)
    else:
        if await form.load(request):
            form.update_account(g.current_account)
            if form.errors:
                dbsession.rollback()
                return jsonify({'errors': form.errors}), 400
            dbsession.commit()
            dbsession.refresh(g.current_account)
            return jsonify({'username':g.current_account.username})
        else:
            return jsonify({'errors': form.errors}), 400
