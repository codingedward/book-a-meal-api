from .base import JsonRequest


class PostRequest(JsonRequest):
    def rules(self):
        return {
            'quantity': 'required|integer|positive',
            'meal_id': 'required|integer|positive|exists:Meal,id',
            'menu_id': 'required|integer|positive|exists:Menu,id',
        }


class PutRequest(JsonRequest):
    def rules(self):
        return {
            'quantity': 'integer|positive',
            'meal_id': 'integer|positive|exists:Meal,id',
            'menu_id': 'integer|positive|exists:Menu,id',
        }
