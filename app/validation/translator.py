"""Translates validation error messages for the response"""


messages = {
    'accepted': 'The :field: must be accepted',
    'after': 'The date :field: must be after :other:',
    'alpha': 'The :field: must be alphabetic',
    'alpha_num': 'The :field: must be alphanumeric',
    'array': 'The :field: must be an array',
    'before': 'The date :field: must be before :other:',
    'between': 'The :field: must be between :least: and :most:',
    'boolean': 'The :field: must be boolean',
    'confirmed': 'The :field: must be confirmed',
    'date': 'The :field: must be a valid date format',
    'different': 'The :field: must be different from :other:',
    'digits': 'The :field: must be numeric and of length :length:',
    'email': 'The :field: must be a valid email',
    'exists': 'The :field: must exist on :model:',
    'found_in': 'The :field: must be found in: :in:',
    'integer': 'The :field: must be an integer',
    'json': 'The :field: must be valid json format',
    'most': 'The :field: must be less than :other:',
    'least': 'The :field: must be more than :other:',
    'numeric': 'The :field: must be numeric',
    'not_in': 'The :field: must not be in: :not_in:',
    'regex': 'The :field: must match the specified pattern',
    'required': 'The :field: must be provided',
    'required_with': 'The :field: must be provided with :other:',
    'required_without': 'The :field: must be provided without :other:',
    'same': 'The :field: must be the same as :other:',
    'size': 'The :field: must be of the size :size:',
    'string': 'The :field: must be a string',
    'unique': 'The :field: must be unique for :model:',
    'url': 'The :field: must be a valid url',
}


def trans(rule, fields):
    message = messages[rule] 
    for k, v in fields:
        message.replace(k, v)
    return message

