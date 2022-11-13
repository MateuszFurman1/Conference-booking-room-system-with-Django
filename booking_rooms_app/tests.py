import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_Allpersons_view(persons):
    client = Client()  # otwieramt przeglądarkę
    url = reverse('all-persons')  # mówimy na jaki url chcemy wejsc
    response = client.get(url)  # wchodzimu na url
    persons_context = response.context['persons']
    assert persons_context.count() == len(persons)
    for p in persons:
        assert p in persons_context
