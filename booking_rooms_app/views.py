import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from booking_rooms_app.form import RoomForm, ReservationForm
from booking_rooms_app.models import Room, Reservation
from django.urls import reverse

class RoomView(View):
    def get(self, request):
        rooms = Room.objects.all()
        date = datetime.date.today()
        if len(rooms) == 0:
            return HttpResponse('Nothing here :(')
        else:
            for room in rooms:
                reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
                room.reserved = datetime.date.today() in reservation_dates
            context = {
                'rooms': rooms,
                'date': date
            }
        return render(request, 'booking_rooms_app/Base_extend.html', context)

class CreateRoomView(View):
    def get(self, request):
        form = RoomForm()
        context = {
            'form': form
        }
        return render(request, 'booking_rooms_app/create.html', context)

    def post(self, request):
        rooms = Room.objects.all()
        name = request.POST.get('name')
        seats = request.POST.get('seats')
        for i in rooms:
            if i.name == name:
                return HttpResponse('Room with this name already exist')
        if int(seats) < 0:
            return HttpResponse('Please set correct number of seats')
        else:
            form = RoomForm(request.POST)
            if form.is_valid():
                form.save()
        return redirect(reverse('home'))

class AllRoomsView(View):
    def get(self, request):
        rooms = Room.objects.all()
        date = datetime.date.today()
        if len(rooms) == 0:
            return HttpResponse('Nothing here :(')
        else:
            for room in rooms:
                reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
                room.reserved = datetime.date.today() in reservation_dates
            context = {
                'rooms': rooms,
                'date': date
                }
            return render(request, 'booking_rooms_app/All_rooms.html', context)

class EditRoomView(View):
    def get(self, request):
        id = request.GET.get('id')
        room = get_object_or_404(Room, pk=id)
        form = RoomForm(instance=room)
        context = {
            'room': room,
            'form': form
        }
        return render(request, 'booking_rooms_app/Edit_view.html', context)

    def post(self, request):
        id = request.POST.get('id')
        rooms = Room.objects.all()
        room = get_object_or_404(Room, pk=id)
        name = request.POST.get('name')
        seats = request.POST.get('seats')
        for i in rooms:
            if i.name == name:
                return HttpResponse('Room with this name already exist')
        if int(seats) < 0:
            return HttpResponse('Please set correct number of seats')
        else:
            form = RoomForm(request.POST or None, instance=room)
            if form.is_valid():
                room.save()
            return redirect(reverse('all-rooms'))

class DeleteRoomView(View):
    def get(self, request):
        id = request.GET.get('id')
        room = get_object_or_404(Room, pk=id)
        room.delete()
        return redirect(reverse('all-rooms'))

class ReservationView(View):
    def get(self, request):
        id = request.GET.get('id')
        room = get_object_or_404(Room, pk=id)
        form = ReservationForm(request.GET or None)
        reservations = room.reservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        date = datetime.date.today()
        context = {
            'room': room,
            'form': form,
            'reservations': reservations,
            'date': date
        }
        return render(request, 'booking_rooms_app/Reservation.html', context)

    def post(self, request):
        id = request.POST.get('id')
        room = get_object_or_404(Room, pk=id)

        form = ReservationForm(request.POST or None)
        form.instance.room = room
        print(form.instance.date)

        if form.is_valid():
            if Reservation.objects.filter(room=room, date=form.instance.date):
                return HttpResponse('Reservation exist')
            elif form.instance.date < datetime.date.today():
                return HttpResponse('Date is from the past')
            form.save()
        return redirect(reverse('all-rooms'))

class DetailView(View):
    def get(self, request):
        id = request.GET.get('id')
        room = get_object_or_404(Room, pk=id)

        reservations = room.reservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        context = {
            'room': room,
            'reservations': reservations
        }
        return render(request, 'booking_rooms_app/Detail_view.html', context)

class SearchView(View):
    def get(self, request):
        date = datetime.date.today()
        rooms = Room.objects.all()
        name = request.GET.get('room-name')
        seats = request.GET.get('seats')

        if 'projector' in request.GET:
            rooms = rooms.filter(projector=True)
        if seats:
            rooms = rooms.filter(seats__gte=int(seats))
        if name:
            rooms = rooms.filter(name__contains=name)
        if 'Cancel Search' in request.GET:
            rooms = Room.objects.all()

        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = date in reservation_dates
        context = {
            "rooms": rooms,
            "date": date
        }
        return render(request, "booking_rooms_app/Search.html", context)