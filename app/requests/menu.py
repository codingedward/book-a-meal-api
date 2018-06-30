from .base import JsonRequest


class PostRequest(JsonRequest):
    def rules(self):
        return {
            'name': 'required|alpha|unique:Menu,name',
        }


class PutRequest(JsonRequest):
    def rules(self):
        return {
            'name': 'required|alpha',
        }
