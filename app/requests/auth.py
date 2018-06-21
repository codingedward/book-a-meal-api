from .base import JsonRequest 

class RegisterRequest(JsonRequest):
    def rules(self):
        return {
            'email': 'required|email|unique:User',
            'password': 'required|string|confirmed|min:6',
            'username': 'required|string',
        }

class LoginRequest(JsonRequest):
    def rules(self):
        return {
            'email': 'required|email',
            'password': 'required|string'
        }
