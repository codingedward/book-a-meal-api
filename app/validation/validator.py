import re
import json
from datetime import date
from .translator import trans

class ValidationException(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)

class Validator:
    def __init__(self, request={}, rules={}):
        """Initialize rules and models"""
        self._rules = rules
        self._request = request

    def passes(self):
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
                 trans('accepted', {':field:': field})
             )
        return (True, '')

    def _after(self, field=None, params=None, **kwargs):
        field_date = self.__to_date(self._request[field])
        if not field_date:
            return (
                False,
                trans('date', {':field:': field})
            )
        after_date = self.__to_date(params)
        if not after_date:
            raise Exception('Validator: after date must match YYYY-MM-DD')

        if field_date < after_date:
            return (
                False,
                trans('after', {':field:': field, ':after': params})
            )
        return (True, '')

    def _alpha(self, field=None, **kwargs):
        if not str(self._request[field]).isalpha():
            return (
                False,
                trans('alpha', {':field:': field})
            )
        return (True, '')

    def _alpha_dash(self, field=None, **kwargs):
        value = self._request[field].replace('-','')
        if not str(self._request[field]).isalpha():
            return (
                False,
                trans('alpha_dash', {':field:': field})
            )
        return (True, '')

    def _alpha_num(self, field=None, **kwargs):
        if not str(self._request[field]).isalnum():
            return (
                False,
                trans('alpha_num', {':field:': field})
            )
        return True, ''

    def _before(self, field=None, params=None, **kwargs):
        field_date = self.__to_date(self._request[field])
        if not field_date:
            return (
                False,
                trans('date', {':field:': field})
            )
        before_date = self.__to_date(params)
        if not after_date:
            raise Exception('Validator: before date must match YYYY-MM-DD')

        if field_date > before_date:
            return (
                False,
                trans('before', {':field:': field, ':after:': params})
            )
        return (True, '')

    def _between(self, field=None, params=None, **kwargs):
        least, most = params.split(',')
        if least > self.request[field] > most:
            return (
                False, 
                trans('between', {
                    ':field:': field, 
                    ':least:': least, 
                    ':most:': most
                })
            )
        return (True, '')

    def _boolean(self, field=None, **kwargs):
        valid = [1, '1', True, 'true', 0, '0', False, 'false' ]
        if self._request[field] not in valid:
            return (
                False,
                trans('boolean', {':field:': field})
            )
        return (True, '')

    def _confirmed(self, field=None, **kwargs):
        confirm_field = field + '_confirmation'
        if self._request.get(confirm_field) is None or  \
                self._request[field] != self.request[confirm_field]:
            return (
                False,
                trans('confirmed', {':field:': field})
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
                trans('date', {':field:': field})
            )
        return (True, '')

    def _different(self, field=None, params=None, **kwargs):
        if self._request[field] == self._request[params]:
            return (
                False,
                trans('different', {':field:': field, ':other:': params})
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
                trans('digits', {':field:': field, ':length:': length})
            )
        return (True, '')

    def _email(self, field=None, **kwargs):
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$",
                        self._request[field]):
            return (
                False,
                trans('email', {':field:': field})
            )
        return (True, '')

    def _exists(self, field=None, params=None, **kwargs):
        modelName, endName = params.split(',')
        model = eval(modelName)
        if not model.query.filter_by(**{field: self._request[field]}).first():
            return (
                False,
                trans('exists', {':field:': field, ':model:': endName})
            )
        return (True, '')

    def _found_in(self, field=None, params=None, **kwargs):
        valid = params.split(',')
        if not self._request[field] in valid:
            return (
                False,
                trans('found_in', {':field:': field, ':in:': valid})
            )

        return (True, '')

    def _integer(self, field=None, **kwargs):
        try:
            int(self._request[field])
        except:
            return (
                False, 
                trans('integer', {':field:': field})
            )
        return (True, '')

    def _json(self, field, **kwargs):
        try:
            json.loads(self._request[field])
        except ValueError:
            return (
                False,
                trans('json', {':field:': field})
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
                trans('most', {':field:': field, ':most:': size})
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
                trans('least', {':field:': field, ':least:': size})
            )
        return (True, '')

    def _numeric(self, field=None, **kwargs):
        try:
            float(self._request[field])
        except:
            return (
                False, 
                trans('numeric', {':field:': field})
            )
        return (True, '')

    def _not_in(self, field=None, params=None, **kwargs):
        not_in = !self._found_in(field, params)
        if not not_in:
            return (
                False,
                trans('not_in', {':field:': field, ':not_in:': params})
            )
        return (True, '')

    def _regex(self, field=None, params=None, **kwargs):
        if not re.match(params, self._request[field]):
            return (
                False,
                trans('regex', {':field:': field})
            )
        return (True, '')

    def _required(self, field=None, params=None, **kwargs):
        if self._request.get(field) is None:
            return  (
                False,
                trans('required', {':field:': field})
            )

    def _required_with(self, field=None, params=None, **kwargs):
        if self._request.get(params) and self._request.get(field) is None:
            return (
                False,
                trans('required_with', {':field:': field, ':other:': params})
            )
        return (True, '')

    def _required_without(self, field=None, params=None, **kwargs):
        if self._request.get(params) and self._request.get(field) is None:
            return (
                False,
                trans('required_without', {':field:': field, ':other:': params})
            )
        return (True, '')

    def _same(self, field=None, params=None, **kwargs):
        if self._request[field] != self._request[params]:
            return (
                False,
                trans('same', {':field:': field, ':other:': params})
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
                trans('size', {':field:': field, ':size:': size})
            )
        return (True, '')

    def _string(self, field=None, params=None, **kwargs):
        if not isinstance(self._request[field], str):
            return (
                False,
                trans('string', {':field:': field})
            )
        return (True, '')

    def _unique(self, field=None, params=None, **kwargs):
        modelName, unique, endName = params.split(',')
        model = eval(modelName)
        if not model.query.filter_by(**{unique: self._request[field]}).first():
            return (
                False,
                trans('unique', {':field:': field, ':model:': endName})
            )

    def _url(self, field=None, params=None, **kwargs):
        pattern = 
        if not re.match(
                '^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$',
                self._request[field]
        ):
            return (
                False,
                trans('url', {':field:': field})
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
