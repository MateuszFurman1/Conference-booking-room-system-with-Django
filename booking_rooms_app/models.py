from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    seats = models.PositiveIntegerField(null=False)
    projector = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


class Reservation(models.Model):
    date = models.DateField()
    comment = models.CharField(max_length=128, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('date', 'room')

    def __str__(self):
        return f'{self.comment}: {self.room}'


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.first_name} {self.date}'
