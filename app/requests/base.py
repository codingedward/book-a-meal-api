from flask import request
from app.validation.validator import Validator, ValidationException


class JsonRequest:
    def __init__(self):
        if not request.is_json:
            raise ValidationException(['Request must be valid JSON'])
        self.validator = Validator(
            rules=self.rules(),
            request=request.json
        )

    def validate(self):
        if self.validator.fails():
            raise ValidationException(self.validator.errors())

    def rules(self):
        return {}
