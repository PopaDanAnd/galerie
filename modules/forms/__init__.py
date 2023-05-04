
class Field:

    def __init__(self, **kwargs):
        self.errors: list = []
        self.data = None
        self.type = kwargs.get('type', 'text')
        self.name = kwargs.get('name', '')
        self.label = kwargs.get('label', self.name)
        self.placeholder = kwargs.get('placeholder', '')
        self.validators = kwargs.get('validators', [])

    def validate(self) -> bool:
        for validator in self.validators:
            if not validator.validate(self):
                raise ValueError(validator.message)
                return False
        return True

    def load(self, data):
        self.errors = []
        if self.type == 'checkbox':
            self.data = (data == 'on')
        elif self.type == 'file':
            self.data = data
        else:
            self.data = data

    @property
    def attributes(self) -> str:
        for validator in self.validators:
            yield validator.constraint


class Validator:

    def __init__(self, **kwargs):
        pass

    def validate(self, field: Field) -> bool:
        pass

    @property
    def constraint(self) -> str:
        return ''


class Form():

    submit_text: str = 'submit'

    async def load(self, request):
        valid: bool = True
        data: dict = await request.form if request.method == 'POST' else request.args
        files: dict = await request.files

        for field_name, field in vars(self.__class__).items():
            if isinstance(field, Field):
                if field.type == 'file':
                    field.load(files.get(field_name))
                else:
                    field.load(data.get(field_name))
                try:
                    field.validate()
                except ValueError as err:
                    field.errors.append(err.args[0])
                    valid = False
        return valid

    @property
    def fields(self):
        for field_name, field in vars(self.__class__).items():
            if isinstance(field, Field):
                yield field

    @property
    def data(self) -> dict:
        data: dict = {}
        for field_name, field in vars(self.__class__).items():
            if isinstance(field, Field):
                data[field_name] = field.data
        return data

    @property
    def errors(self) -> dict:
        errors: dict = {}
        for field_name, field in vars(self.__class__).items():
            if isinstance(field, Field):
                if field.errors:
                    errors[field_name] = field.errors
        return errors
