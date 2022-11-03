from django.contrib import admin

from booking_rooms_app.models import Room, Reservation

# Register your models here.
admin.site.register(Room)
admin.site.register(Reservation)