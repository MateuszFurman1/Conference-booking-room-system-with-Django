from django import forms
from django.forms import SelectDateWidget

from .models import Room, Reservation
import datetime

class RoomForm(forms.ModelForm):
     class Meta:
        model = Room
        fields = ('name', 'seats', 'projector')
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'seats': forms.NumberInput(attrs={'class': "form-control"}),
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('comment', 'date')
        widgets = {
            'comment': forms.Textarea(attrs={'class': "form-control"}),
            'date': SelectDateWidget,
        }
