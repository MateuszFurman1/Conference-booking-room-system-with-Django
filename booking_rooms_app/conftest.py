import pytest
from django.contrib.auth.models import User, Permission

from booking_rooms_app.models import Room


@pytest.fixture
def rooms():
    lst = []
    for n in range(10):
        p = Room.objects.create(name=n, seats=n, projector=False, created='2022-11-07 20:20:46.816306+01',
                                updated='2022-11-07 20:20:46.816306+01')
        lst.append(p)
    return lst

# @pytest.fixture
# def oneMovie(persons):
#     p = Movie.objects.create(title='Owoc który się nie kula', year=2022, director=persons[0])
#     return p
#
@pytest.fixture
def user():
    return User.objects.create(username='tadeusz')


# @pytest.fixture
# def user():
#     u = User.objects.create(username='amadeusz')
#     return u