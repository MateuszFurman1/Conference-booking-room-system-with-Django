from booking_rooms_app.models import Comment
import factory
from factory.faker import Faker
from factory.django import DjangoModelFactory
from django.contrib.auth.models import User
from factory import Sequence, PostGenerationMethodCall
from booking_rooms_app.models import Room

class RoomFactory(DjangoModelFactory):
    class Meta:
        model = Room

    name = 'test'
    seats = 'test'
    projector = True

# class UserFactory(DjangoModelFactory):
#
#     class Meta:
#         model = 'booking_rooms.User'
#
#     first_name = 'test'
#     last_name = 'test'
#     username = 'test'
#     password = PostGenerationMethodCall('set_password', 'secret')
#
# u = UserFactory()
# print(u)

# class CommentFactory(DjangoModelFactory):
#     class Meta:
#         model = Comment
#         text = models.TextField()
#         author = factory.SubFactory(UserFactory)
#         date =