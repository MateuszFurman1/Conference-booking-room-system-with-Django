from django.contrib import admin

from booking_rooms_app.models import Room, Reservation, Comment

# Register your models here.
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Comment)