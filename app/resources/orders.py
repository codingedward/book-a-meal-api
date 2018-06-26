from flask import request
from flask_restful import Resource
from app.validation import validate
from app.models import Order, MenuItem
from app.requests.orders import PostRequest, PutRequest
from app.middlewares.auth import user_auth, admin_auth
from app.utils import current_user


class OrderResource(Resource):

    @user_auth
    def get(self, order_id):
        # exists? ...
        order = Order.query.get(order_id)
        if not order:
            return {
                'success': False,
                'message': 'Order not found.',
            }, 404

        return {
            'success': True,
            'message': 'Order successfully retrieved.',
            'order': order.to_dict()
        }

    @user_auth
    @validate(PutRequest)
    def put(self, order_id):

        # exists? ...
        order = Order.query.get(order_id)
        if not order:
            return {
                'success': False,
                'message': 'Order not found.',
            }, 404

        # check user is authorized to update order
        user = current_user()
        if not user.is_caterer() and user.id != order.user_id:
            return {
                'success': False,
                'message': 'Unauthorized access to this order.'
            }, 401

        # check that we have enough quantity...
        menu_item = MenuItem.query.get(request.json['menu_item_id'])
        available = order.quantity + menu_item.quantity
        if available < request.json['quantity']:
            message = None
            if menu_item.quantity > 0:
                message = 'Only {} more meals are available.'.format(
                    menu_item.quantity
                )
            else:
                message = 'No more orders can be made on this meal.'

            return {
                'success': False,
                'message': 'Validation error.',
                'errors': {
                    'quantity': [message]
                }
            }, 400

        # set the new quantity...
        menu_item.quantity = (menu_item.quantity 
                              - request.json['quantity'] 
                              + order.quantity)
        menu_item.save()

        # update...
        order.update(request.json)
        return {
            'success': True,
            'message': 'Order successfully updated.',
            'order': order.to_dict()
        }

    @user_auth
    def delete(self, order_id):
        # exists? ...
        order = Order.query.get(order_id)
        if not order:
            return {
                'success': False,
                'message': 'Order not found.',
            }, 404

        # check user can delete this order...
        user = current_user()
        if not user.is_caterer() and user.id != order.user_id:
            return {
                'success': False,
                'message': 'Unauthorized access to this order.'
            }, 401

        # restore quantity...
        menu_item = MenuItem.query.get(order.menu_item_id)
        menu_item.quantity += order.quantity
        menu_item.save()

        # now delete...
        order.delete()
        return {
            'success': True,
            'message': 'Order successfully deleted.',
        }


class OrderListResource(Resource):
    @user_auth
    def get(self):
        resp = Order.paginate()
        resp['orders'] = resp['data']
        resp['message'] = 'Successfully retrieved orders.'
        resp['success'] = True
        return resp

    @user_auth
    @validate(PostRequest)
    def post(self):

        # check we have enough quantity...
        menu_item = MenuItem.query.get(request.json['menu_item_id'])
        if menu_item.quantity < request.json['quantity']:
            message = None
            if menu_item.quantity > 0:
                message = 'Only {} meals are available.'.format(
                    menu_item.quantity
                )
            else:
                message = 'No more orders can be made on this meal.'

            return {
                'success': False,
                'message': 'Validation error.',
                'errors': {
                    'quantity': [message]
                }
            }, 400

        # update quantity...
        menu_item.quantity -= request.json['quantity']
        menu_item.save()

        # create order...
        order = Order.create(request.json)
        return {
            'success': True,
            'message': 'Successfully saved order.',
            'order': order.to_dict()
        }, 201
