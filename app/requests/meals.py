from .base import JsonRequest


class PostRequest(JsonRequest):
    def rules(self):
        return {
            'name': 'required|string|unique:Meal,name',
            'cost': 'required|positive',
            'img_url': 'url',
        }


class PutRequest(JsonRequest):
    def rules(self):
        return {
            'name': 'string',
            'cost': 'positive',
            'img_url': 'url',
        }
