import factory
from django.utils import timezone

from .models import Room, Reservation, Comment


class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room

    name = factory.Faker('word')
    seats = factory.Faker('pyint', min_value=1, max_value=50)
    projector = factory.Faker('pybool')
    updated = factory.Faker('date_time_this_month', tzinfo=timezone.utc)
    created = factory.Faker('date_time_this_month', tzinfo=timezone.utc)


class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reservation

    date = factory.Faker('date_between', start_date='+1d', end_date='+7d')
    comment = factory.Faker('sentence')
    room = factory.SubFactory(RoomFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    text = factory.Faker('text')
    author = factory.SubFactory('users.factories.UserFactory')
    date = factory.Faker('date_time_this_month', tzinfo=timezone.utc)
