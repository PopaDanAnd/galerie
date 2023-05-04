
from forms import Validator, Field


class Length(Validator):

    def __init__(self, **kwargs):
        self.max = kwargs.get('max', None)
        self.min = kwargs.get('min', None)
        self.message = kwargs.get('message', 'Invalid length.')

    def validate(self, field: Field):
        data_len = len(field.data)
        if self.max is not None and data_len > self.max:
            return False
        if self.min is not None and data_len < self.min:
            return False
        return True

    @property
    def constraint(self) -> str:
        if self.min is not None and self.max is not None:
            return f'minlength="{self.min}" maxlength="{self.max}"'
        elif self.min is not None:
            return f'minlength="{self.min}"'
        elif self.max is not None:
            return f'maxlength="{self.max}"'
        else:
            return ''


class NotEmpty(Validator):

    def __init__(self, **kwargs):
        self.message = kwargs.get('message', 'Field is empty.')

    def validate(self, field: Field):
        return bool(field.data)

    @property
    def constraint(self) -> str:
        return 'required'


class HasExtension(Validator):

    def __init__(self, **kwargs):
        self.extensions = kwargs.get('extensions')
        self.message = kwargs.get('message', 'Extension not allowed.')

    def validate(self, field: Field):
        if not field.data:
            return True
        filename = field.data.filename.lower()
        return '.' in filename and filename.rsplit('.', 1)[1] in self.extensions
