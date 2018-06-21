from .base import JsonRequest 

class RegisterRequest(JsonRequest):
    def rules(self):
        return {
            'email': 'required|email|unique:User,email',
            'password': 'required|string|confirmed|least_string:6',
            'username': 'required|string',
        }

class LoginRequest(JsonRequest):
    def rules(self):
        return {
            'email': 'required|email',
            'password': 'required|string'
        }
