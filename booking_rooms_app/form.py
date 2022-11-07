from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget

from .models import Room, Reservation, Comment


def validate_seats(value):
    if value < 1:
        raise ValidationError("Please set correct seats number")


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name', 'seats', 'projector')
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'seats': forms.NumberInput(attrs={'class': "form-control"}),
        }
    def clean(self):
        cleaned_data = super().clean()
        seats = cleaned_data['seats']
        if seats < 1:
            raise forms.ValidationError("This is not valid seats number")


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('comment', 'date')
        widgets = {
            'comment': forms.Textarea(attrs={'class': "form-control"}),
            'date': SelectDateWidget,
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': "form-control"}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    re_password = forms.CharField(max_length=128, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.Textarea(attrs={'class': "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['re_password']:
            raise ValidationError('Passwords are not the same!')
