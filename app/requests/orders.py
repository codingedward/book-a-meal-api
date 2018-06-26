from .base import JsonRequest


class PostRequest(JsonRequest):
    def rules(self):
        return {
            'quantity': 'required|integer|positive',
            'user_id': 'required|integer|positive|exists:User,id',
            'menu_item_id': 'required|integer|positive|exists:MenuItem,id',
        }


class PutRequest(JsonRequest):
    def rules(self):
        return {
            'quantity': 'integer|positive',
            'menu_item_id': 'integer|positive|exists:MenuItem,id',
        }
