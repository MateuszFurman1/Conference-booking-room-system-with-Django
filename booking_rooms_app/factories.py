# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "booking_rooms.settings")
# import django
# django.setup()
# from django.core.management import call_command
from booking_rooms_app.models import User, Comment
import factory
from factory.django import DjangoModelFactory
from faker import Faker

faker = Faker()

from django.contrib.auth.models import User

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('username')
    password = '123'
    is_staff = True
    is_active = True

u = UserFactory()
print(u)

# class CommentFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Comment
#         text = models.TextField()
#         author = models.ForeignKey(User, on_delete=models.CASCADE)
#         date