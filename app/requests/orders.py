from .base import JsonRequest


class PostRequest(JsonRequest):
    @staticmethod
    def rules():
        return {
            'quantity': 'required|integer|positive',
            'user_id': 'required|integer|positive|exists:User,id',
            'menu_item_id': 'required|integer|positive|exists:MenuItem,id',
        }


class PutRequest(JsonRequest):
    @staticmethod
    def rules():
        return {
            'quantity': 'integer|positive',
            'menu_item_id': 'integer|positive|exists:MenuItem,id',
        }
