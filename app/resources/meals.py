from flask import request
from flask_restful import Resource
from app.models import Meal
from app.requests.meals import PostRequest, PutRequest
from app.validation import validate
from app.middlewares.auth import user_auth, admin_auth


class MealResource(Resource):

    @user_auth
    def get(self, meal_id):
        # exists? ...
        meal = Meal.query.get(meal_id)
        if not meal:
            return {
                'success': False,
                'message': 'Meal not found',
            }, 404

        return {
            'success': True,
            'message': 'Meal successfully retrieved',
            'data': {
                'meal': meal.to_dict()
            }
        }

    @admin_auth
    @validate(PutRequest)
    def put(self, meal_id):

        # check if another meal exists with new name...
        name = request.json['name']
        meal = Meal.query.filter_by(name=name).first()
        if meal and meal.name.lower() == name.lower() and meal.id != meal_id:
            return {
                'success': False,
                'message': 'Validation error',
                'errors': {
                    'name': ['Meal name must be unique']
                }
            }, 400

        # check exists? ...
        meal = Meal.query.get(meal_id)
        if not meal:
            return {
                'success': False,
                'message': 'Meal not found',
            }, 404

        # now update...
        meal.update(request.json)
        return {
            'success': True,
            'message': 'Meal successfully updated',
            'data': {
                'meal': meal.to_dict()
            }
        }

    @user_auth
    def delete(self, meal_id):
        # exists? ...
        meal = Meal.query.get(meal_id)
        if not meal:
            return {
                'success': False,
                'message': 'Meal not found',
            }, 404

        meal.delete()
        return {
            'success': True,
            'message': 'Meal successfully deleted',
        }


class MealListResource(Resource):
    @user_auth
    def get(self):
        print(Meal.paginate())
        return {}

    @admin_auth
    @validate(PostRequest)
    def post(self):
        meal = Meal.create(request.json)
        return {
            'success': True,
            'message': 'Successfully saved meal.',
            'data': {
                'meal': meal.to_dict()
            }
        }, 201

