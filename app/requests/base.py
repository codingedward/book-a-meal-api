from flask import request
from app.validation.validator import Validator
from app.exceptions import ValidationException
from app.middlewares.clean_request import clean_json_request


class JsonRequest:

    @clean_json_request
    def __init__(self):
        self.validator = Validator(
            rules=self.rules(),
            request=request.json
        )

    def validate(self):
        if self.validator.fails():
            raise ValidationException(self.validator.errors())

    def rules(self):
        return {}
