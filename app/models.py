"""Contains the application's database models"""


import json
from app import db
from passlib.hash import bcrypt
from datetime import datetime


class UserType:
    """Users roles"""
    ADMIN = 1
    USER = 2


class MenuType:
    """Menu categories"""
    BREAKFAST = 1
    LUNCH = 2
    SUPPER = 3


class BaseModel:
    """This will handle saving and deletion of models"""

    _fields = []
    _hidden = []
    _timestamps = True

    @classmethod
    def make(cls, data):
        instance = cls()
        instance.from_dict(data)
        return instance

    @classmethod
    def create(cls, data):
        instance = cls()
        instance.from_dict(data)
        instance.save()
        return instance

    def update(self, data):
        self.from_dict(data)
        self.save()
        return self

    @classmethod
    def paginate(cls):
        pg = cls.query.paginate(error_out=False)
        return {
            'meta': {
                'pages': pg.pages,
                'total': pg.total,
                'has_next': pg.has_next,
                'has_prev': pg.has_prev,
                'per_page': pg.per_page,
                'next_page': pg.next_num,
                'prev_page': pg.prev_num,
            },
            'data':[ inst.to_dict() for inst in pg.items ]
        }

    def from_dict(self, data):
        for field in self._fields:
            if field in data:
                setattr(self, field, data[field])
        return self

    def save(self):
        """Save current model"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete current model"""
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        dict_repr = {}

        # check if has id
        if getattr(self, 'id'):
            dict_repr['id'] = self.id

        # check if timestamps enabled and feed the dict
        if self._timestamps:
            created = getattr(self, 'created_at')
            if created:
                dict_repr['created_at'] = str(created)
            updated = getattr(self, 'updated_at')
            if updated: 
                dict_repr['updated_at'] = str(updated)

        # for every field declared...
        for field in self._fields:
            # as long as it is not hidden feed it...
            if field not in self._hidden:
                value = getattr(self, field)
                if isinstance(value, datetime):
                    dict_repr[field] =  str(value)
                else:
                    dict_repr[field] = value
        return dict_repr

    def to_json(self):
        return json.dumps(self.to_dict())


class Blacklist(db.Model, BaseModel):
    """Holds JWT tokens revoked through user signing out"""

    __tablename__ = 'blacklist'
    _fields = ['token']

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, token=None):
        """Initialiaze the blacklist record"""
        self.token = token


class User(db.Model, BaseModel):
    """This will have application's users details"""

    __tablename__ = 'users'
    _hidden = ['password']
    _fields = ['username', 'email', 'password', 'role']

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(1024), unique=True)
    password = db.Column(db.String(300))
    role = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, username=None, email=None,\
                 password=None, role=UserType.USER):
        """Initialize the user"""
        self.email = email
        self.role = role
        self.username = username
        if password:
            self.password = bcrypt.encrypt(password)

    def from_dict(self, data):
        for field in self._fields:
            if field in data:
                if field == 'password':
                    self.password = bcrypt.encrypt(data[field])
                else:
                    setattr(self, field, data[field])

    def validate_password(self, password):
        """Checks the password is correct against the password hash"""
        return bcrypt.verify(password, self.password)

    def is_caterer(self):
        """Checks if current user is a caterer"""
        return self.role == UserType.ADMIN


class Menu(db.Model, BaseModel):
    """Holds the menus"""

    __tablename__ = 'menus'
    _fields = ['category']

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, category=None):
        """Initialize the menu"""
        self.category = category


class MenuItem(db.Model, BaseModel):
    """Holds the menu item of the application"""

    __tablename__ = 'menu_items'
    _fields = ['day', 'menu_id', 'meal_id', 'quantity']

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Date, default=db.func.current_timestamp())
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))
    quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    # relationship with the menu
    menu = db.relationship(
        'Menu',
        backref=db.backref('menu_items', lazy='dynamic')
    )

    # relationship with the meal
    meal = db.relationship(
        'Meal',
        backref=db.backref('menu_items', lazy='dynamic')
    )

    def __init__(self, menu_id=None, meal_id=None, quantity=1):
        """Initialize a meal item"""
        self.menu_id = menu_id
        self.meal_id = meal_id
        self.quantity = quantity


class Meal(db.Model, BaseModel):
    """Holds a meal in the application"""

    __tablename__ = 'meals'
    _fields = ['name', 'cost', 'img_url']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    cost = db.Column(db.Float(2))
    img_url = db.Column(db.String(2048))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    def __init__(self, name=None, cost=None, img_url=None):
        """Initialize a meal"""
        self.name = name
        self.cost = cost
        self.img_url = img_url


class Order(db.Model, BaseModel):
    """Holds an order of the application"""

    __tablename__ = 'orders'
    _fields = ['quantity', 'menu_item_id', 'user_id']

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    menu_item_id = db.Column(
        db.Integer,
        db.ForeignKey('menu_items.id', ondelete='CASCADE')
    )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    # relationship with the menu items
    menu_item = db.relationship(
        'MenuItem',
        backref=db.backref('orders', lazy='dynamic')
    )

    def __init__(self, menu_item_id=None, user_id=None, quantity=None):
        """Initialize the order"""
        self.user_id = user_id
        self.quantity = quantity
        self.menu_item_id = menu_item_id


class Notification(db.Model, BaseModel):
    """Notification model"""

    __tablename__ = 'notifications'
    _fields = ['title', 'message', 'user_id']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    message = db.Column(db.String(1024))
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

    # relationship with a user
    user = db.relationship(
        'User',
        backref=db.backref('notifications', lazy='dynamic')
    )

    def __init__(self, title=None, message=None, user_id=None):
        """Initialize the notification"""
        self.title = title
        self.message = message
        self.user_id = user_id
