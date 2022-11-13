import pytest
from django.contrib.auth.models import User, Permission

from shelf.models import Person, Studio, Movie


@pytest.fixture
def oneMovie(persons):
    p = Movie.objects.create(title='Owoc który się nie kula', year=2022, director=persons[0])
    return p

@pytest.fixture
def user_with_permission():
    u = User.objects.create(username='tadeusz')
    permission = Permission.objects.get(codename='add_comment')
    u.user_permissions.add(permission)
    return u

@pytest.fixture
def user():
    u = User.objects.create(username='amadeusz')
    return u