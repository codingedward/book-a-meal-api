import re
from flask import request
from app.validation.validator import Validator, ValidationException


class JsonRequest:
    def __init__(self):
        if not request.is_json:
            raise ValidationException(['Request must be valid JSON'])
        for field, value in request.json.items():
            
            if isinstance(value, str):
                request.json[field] = re.sub('\s+', ' ', value).strip()
        self.validator = Validator(
            rules=self.rules(),
            request=request.json
        )

    def validate(self):
        str(self.validator.errors())
        if self.validator.fails():
            raise ValidationException(self.validator.errors())

    def rules(self):
        return {}
