import re
import json
from datetime import date

"""A request validator inspired by Laravel validation rules. 

The rules supported include:
1. accepted - this field must be yes, on, 1 or true
2. after:date - must be after date specified in the format YYYY-MM-DD
3. alpha - must be all alphabetic characters
4. alpha_dash - alphas and dash allowed
5. alpha_num - alpha numeric allowed
6. array - must be an array
7. before:date - must be before date specified in the format YYYY-MM-DD
8. between:min,max - 
9. boolean - true, false, 0 or 1 as well as "0" and "1"
10. confirmed - must have foo_confirmation for a field foo
11. date - must be in the format YYYY-MM-DD
12. different:field - must be different from the specified field
13. digits:value - must be numeric and must have exact length of value
14. digits_between:min,max - must be numeric and have an exact length of 
    value
15. email - must be a valid email
16. exists:table,column,... - the field under validation must exist on a 
    table
17. in:foo,bar,... - must be in the list given
18. integer - the field must be an integer
20. json - the field must be a JSON string
21. max:value -  maximum value evaluated same as the size rule
22. min:value - minimum value evaluated same as size rule
23. numeric - must be a numeric value
24. not_in:foo,bar... - field must not equal any of the values in the list
25. regex:pattern
26. required -  this field must be present
27. required_if:another_field,value,...
29. required_with:foo,bar,... - required if any of the other fields is 
    present
31. required_without:foo,bar,... - required without any of the other fields
33. same:field - the two fields must match
34. size:value - for a string, this is the length, for numeric data, value
    is the integer value. 
35. string - must be a string, empty strings are not allowed.
36. unique:table,column,except,columnId - must be unique in the given 
    table's column except the given columnId
37. url - field under validation must be a url
"""

class Validator:
    def __init__(self, request={}, rules={}):
        """Initialize rules and models"""
        self._rules = rules
        self._request = request
        self._errors = {
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

    def valid(self):
        # for every field and its rules...
        for field, rules in self._rules:

            # for each of current field's rule...
            for rule in rules.split('|'):
                # split rule name and its parameters...
                rule_name = rule_params = None
                if ':' in rule:
                    rule_name, rule_params = rule.split(':')
                else:
                    rule_name = rule
                func_name = '_' + rule_name # rule function name

                # field exists? ...only when not executing required rule
                if rule_name != 'required' and self._request[field]:

                    # check if we have a function for this rule..
                    if not hasattr(self, func_name):
                        raise Exception('Validator: no rule named '+rule_name)

                    # now get that function and call it with the arguments
                    func = getattr(self, func_name)
                    is_valid, message = func(field=field, params=rule_params)

                    # if rule does not pass save the error and bail
                    if not is_valid:
                        if not self.errors.get(field):
                            self.errors[field] = []
                        self.errors[field].append(message)
                        return False
        return True

    def fails(self):
        return not self.passes()

    def first(self, field=field):
        pass

    def errors(self):
        return self.errors

    def set_rules(rules={}):
        self._rules = rules

    def _accepted(self, field=None, **kwargs):
        valid = [1, '1', True, 'true', 'yes']
        if self._request[field] not in valid: 
             return (
                 False, 
                 self._errors['accepted'].replace(':field:', field)
             )
        return (True, '')

    def _after(self, field=None, params=None, **kwargs):
        field_date = self.__to_date(self._request[field])
        if not field_date:
            return (
                False,
                self._errors['date']
                .replace(':field:', field)
            )
        after_date = self.__to_date(params)
        if not after_date:
            raise Exception('Validator: after date must match YYYY-MM-DD')

        if field_date < after_date:
            return (
                False,
                self.errors['after']
                .replace(':field:', field)
                .repalce(':after:', params)
            )
        return (True, '')

    def _alpha(self, field=None, **kwargs):
        if not str(self._request[field]).isalpha():
            return (
                False,
                self._errors['alpha'].replace(':field:', field)
            )
        return (True, '')

    def _alpha_dash(self, field=None, **kwargs):
        value = self._request[field].replace('-','')
        if not str(self._request[field]).isalpha():
            return (
                False,
                self._errors['alpha_dash'].replace(':field:', field)
            )
        return (True, '')

    def _alpha_num(self, field=None, **kwargs):
        if not str(self._request[field]).isalnum():
            return (
                False,
                self._errors['alpha_num'].replace(':field:', field)
            )
        return True, ''

    def _before(self, field=None, params=None, **kwargs):
        field_date = self.__to_date(self._request[field])
        if not field_date:
            return (
                False,
                self._errors['date']
                .replace(':field:', field)
            )
        before_date = self.__to_date(params)
        if not after_date:
            raise Exception('Validator: before date must match YYYY-MM-DD')

        if field_date > before_date:
            return (
                False,
                self.errors['before']
                .replace(':field:', field)
                .repalce(':after:', params)
            )
        return (True, '')

    def _between(self, field=None, params=None, **kwargs):
        least, most = params.split(',')
        if least > self.request[field] > most:
            return (
                False, 
                self._errors['between']
                .replace(':field:', field)
                .replace(':least:', least)
                .replace(':most:', most)
            )
        return (True, '')

    def _boolean(self, field=None, **kwargs):
        valid = [1, '1', True, 'true', 0, '0', False, 'false' ]
        if self._request[field] not in valid:
            return (
                False,
                self._errors['boolean'].replace(':field:', field)
            )
        return (True, '')

    def _confirmed(self, field=None, **kwargs):
        confirm_field = field + '_confirmation'
        if self._request.get(confirm_field) is None or  \
                self._request[field] != self.request[confirm_field]:
            return (
                False,
                self._errors['confirmed']
                .replace(':field:', field)
            )
        return (True, '')

    def _date(self, field, **kwargs):
        ok = True
        date_lst = [int(x) for x in self._requests[field].split('-')]
        ok = len(date_lst) == 3
        if ok:
            try:
                year, month, day = date_lst
                date(year, month, day)
            except ValueError:
                ok = False
        if not ok:
            return (
                False,
                self._errors['date']
                .replace(':field:', field)
            )
        return (True, '')

    def _different(self, field=None, params=None, **kwargs):
        if self._request[field] == self._request[params]:
            return (
                False,
                self._errors['different']
                .replace(':field:', field)
                .replace(':other:', params)
            )
        return (True, '')

    def _digits(self, field=None, params=None, **kwargs):
        length = int(params)
        is_numeric, msg = self._isnumeric(field)
        if not is_numeric:
            return (False, msg)
        str_repr = str(self._request[field])

        if '.' in str_repr: length += 1 
        if len(str_repr) != length:
            return (
                False,
                self._errors['digits']
                .replace(':field:', field)
                .replace(':length:', length)
            )
        return (True, '')

    def _email(self, field=None, **kwargs):
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                        self._request[field]):
            return (
                False,
                self._errors['email'].replace(':field:', field)
            )
        return (True, '')

    def _exists(self, field=None, params=None, **kwargs):
        modelName, endName = params.split(',')
        model = eval(modelName)
        if not model.query.filter_by(**{field: self._request[field]}).first():
            return (
                False,
                self._errors['exists']
                .replace(':field:', field)
                .replace(':model:', endName)
            )
        return (True, '')

    def _found_in(self, field=None, params=None, **kwargs):
        valid = params.split(',')
        if not self._request[field] in valid:
            return (
                False,
                self._errors['found_in']
                .replace(':field:', field)
                .replace(':in:', valid.join(', '))
            )

        return (True, '')

    def _integer(self, field=None, **kwargs):
        try:
            int(self._request[field])
        except:
            return (
                False, 
                self._errors['integer'].replace(':field:', field)
            )
        return (True, '')

    def _json(self, field, **kwargs):
        try:
            json.loads(self._request[field])
        except ValueError:
            return (
                False,
                self._errors['json'].replace(':field:', field)
            )
        return (True, '')

    def _most(self, field=None, params=None, **kwargs):
        ok = True
        size = int(params)
        value = self._requests[field]
        if isinstance(value, str):
            if len(value) < size:
                ok = False
        else:
            value = float(value)
            if value < size:
                ok = False
        if not ok:
            return (
                False,
                self._errors['most']
                .replace(':field:', field)
                .replace(':most:', size)
            )
        return (True, '')

    def _least(self, field=None, params=None, **kwargs):
        ok = True
        size = int(params)
        value = self._requests[field]
        if isinstance(value, str):
            if len(value) > size:
                ok = False
        else:
            value = float(value)
            if value > size:
                ok = False
        if not ok:
            return (
                False,
                self._errors['least']
                .replace(':field:', field)
                .replace(':least:', size)
            )
        return (True, '')

    def _numeric(self, field=None, **kwargs):
        try:
            float(self._request[field])
        except:
            return (
                False, 
                self._errors['numeric'].replace(':field:', field)
            )
        return (True, '')

    def _not_in(self, field=None, params=None, **kwargs):
        not_in = !self._found_in(field, params)
        if not not_in:
            return (
                False,
                self._errors['not_in']
                .replace(':field:', field)
                .replace(':not_in:', params.replace(',', ', ')))
            )
        return (True, '')

    def _regex(self, field=None, params=None, **kwargs):
        if not re.match(params, self._request[field]):
            return (
                False,
                self._errors['regex'].replace(':field:', field)
            )
        return (True, '')

    def _required(self, field=None, params=None, **kwargs):
        if self._request.get(field) is None:
            return  (
                False,
                self._errors['required'].replace(':field:', field)
            )

    def _required_with(self, field=None, params=None, **kwargs):
        if self._request.get(params) and self._request.get(field) is None:
            return (
                False,
                self._errors['required_with']
                .replace(':field:', field)
                .replace(':other:', params)
            )
        return (True, '')

    def _required_without(self, field=None, params=None, **kwargs):
        if self._request.get(params) and self._request.get(field) is None:
            return (
                False,
                self._errors['required_without']
                .replace(':field:', field)
                .replace(':other:', params)
            )
        return (True, '')

    def _same(self, field=None, params=None, **kwargs):
        if self._request[field] != self._request[params]:
            return (
                False,
                self._errors['same']
                .replace(':field:', field)
                .replace(':other:', params)
            )
        return (True, '')

    def _size(self, field=None, params=None, **kwargs):
        ok = True
        size = int(params)
        value = self._requests[field]
        if isinstance(value, str):
            if len(value) != size:
                ok = False
        else:
            value = float(value)
            if value != size:
                ok = False
        if not ok:
            return (
                False,
                self._errors['size']
                .replace(':field:', field)
                .replace(':size:', size)
            )
        return (True, '')

    def _string(self, field=None, params=None, **kwargs):
        if not isinstance(self._request[field], str):
            return (
                False,
                self._errors['string'].replace(':field:', field)
            )
        return (True, '')

    def _unique(self, field=None, params=None, **kwargs):
        modelName, unique, endName = params.split(',')
        model = eval(modelName)
        if not model.query.filter_by(**{unique: self._request[field]}).first():
            return (
                False,
                self._errors['unique']
                .replace(':field:', field)
                .replace(':model:', endName)
            )

    def _url(self, field=None, params=None, **kwargs):
        pattern = 
        if not re.match(
                '^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$',
                self._request[field]
        ):
            return (
                False,
                self._errors['url']
                .replace(':field:')
            )
        return (True, '')

    def __to_date(self, date_str):
        date_lst = [int(x) for x in date_str.split('-')]
        if len(date_lst) == 3:
            try:
                year, month, day = date_lst
                return date(year, month, day)
            except ValueError:
                return None
        return None
