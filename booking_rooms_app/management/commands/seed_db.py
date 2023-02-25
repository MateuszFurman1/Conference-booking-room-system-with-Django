from django.core.management.base import BaseCommand
from booking_rooms_app.factories import ReservationFactory, CommentFactory
from django.db import transaction

class Command(BaseCommand):
    help = 'Seeds the database with dummy data'

    def handle(self, *args, **options):
        with transaction.atomic():
            reservation = ReservationFactory.create_batch(5)
            comment = CommentFactory.create_batch(5)
