from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from booking_rooms_app.form import RoomForm
from booking_rooms_app.models import Room


@pytest.mark.django_db
def test_create_room_get_view(user):
    client = Client()
    url = reverse('create-room')
    client.force_login(user)
    response = client.get(url)
    assert 200 == response.status_code
    assert isinstance(response.context['form'], RoomForm)


@pytest.mark.django_db
def test_create_room_post_view_with_log(user):
    client = Client()
    url = reverse('create-room')
    client.force_login(user)
    data = {
        'name': 'room',
        'seats': 100,
        'projector': False
        }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Room.objects.get(name='room', seats=100, projector=False)


@pytest.mark.django_db
def test_Allrooms_view(rooms):
    client = Client()  # otwieramt przeglądarkę
    url = reverse('all-rooms')  # mówimy na jaki url chcemy wejsc
    response = client.get(url)  # wchodzimu na url
    persons_context = response.context['rooms']
    assert persons_context.count() == len(rooms)
    for p in rooms:
        assert p in persons_context


@pytest.mark.django_db
def test_edit_room_get_view(user, rooms):
    client = Client()
    url = reverse('edit-room')
    client.force_login(user)
    data = {
        'name': 'room',
        'seats': 100,
        'projector': False
    }
    response = client.get(url, data)
    # assert 200 == response.status_code
    assert isinstance(response.context['form'], RoomForm)


@pytest.mark.django_db
def test_edit_room_post_view_with_perm(user):
    client = Client()
    url = reverse('edit-room')
    client.force_login(user)
    data = {
        'name': 'room',
        'seats': 100,
        'projector': False
        }
    response = client.post(url, data)
    assert response.status_code == 302
    assert Room.objects.get(name='room', seats=100, projector=False)
