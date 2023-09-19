from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager
from mongoengine import DoesNotExist, DateTimeField

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except DoesNotExist:
        return None


class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True, min_length=1, max_length=40)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()
    reviews = db.ListField(db.ReferenceField('Review'))

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min_length=5, max_length=500)
    date = DateTimeField(default=datetime.utcnow, required=True)
    imdb_id = db.StringField(required=True, min_length=9, max_length=9)
    movie_title = db.StringField(required=True, min_length=1, max_length=100)
