import datetime
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse

from booking_rooms_app.form import RoomForm, ReservationForm, CommentForm, LoginForm, RegistrationForm
from booking_rooms_app.models import Room, Reservation, Comment
from django.urls import reverse, reverse_lazy


def activateEmail(request, user, to_email):
    messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
        received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')


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


@method_decorator(login_required(login_url='login'), name='dispatch')
class CreateRoomView(View):
    def get(self, request):
        form = RoomForm()
        context = {
            'form': form
        }
        return render(request, 'booking_rooms_app/form.html', context)

    def post(self, request):
        form = RoomForm(request.POST)
        context = {
            'form': form
        }
        if form.is_valid():
            t = form.save()
            messages.success(request, f"{t.name} has been added")
            return redirect(reverse('home'))
        return render(request, 'booking_rooms_app/create.html', context)


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


@method_decorator(login_required(login_url='login'), name='dispatch')
class EditRoomView(LoginRequiredMixin, View):
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
        room = get_object_or_404(Room, pk=id)
        form = RoomForm(request.POST or None, instance=room)
        ctx = {
            'form': form
        }
        if form.is_valid():
            room.save()
            messages.success(request, f"{room} has been updated")
            return redirect(reverse('all-rooms'))
        return render(request, 'booking_rooms_app/Edit_view.html', ctx)


@method_decorator(login_required(login_url='login'), name='dispatch')
class DeleteRoomView(View):
    def get(self, request):
        id = request.GET.get('id')
        room = get_object_or_404(Room, pk=id)
        room.delete()
        messages.success(request, f"{room} has been deleted")
        return redirect(reverse('all-rooms'))


@method_decorator(login_required(login_url='login'), name='dispatch')
class ReservationView(View):
    def get(self, request):
        id = request.GET.get('id')
        room = get_object_or_404(Room, pk=id)
        form = ReservationForm()
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
                return messages.error('Reservation exist')
            elif form.instance.date < datetime.date.today():
                return messages.error('Date is from the past')
            form.save()
            messages.success(request, f"Reservation has been made")
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


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        page = 'login'
        ctx = {
            "form": form,
            'page': page
        }
        return render(request, 'booking_rooms_app/form.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        ctx = {
            "form": form,
        }
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "Login successfully")
                return redirect('home')
            messages.error(request, "Wrong name or password!")
            ctx = {
                "form": form
            }
        return render(request, 'booking_rooms_app/form.html', ctx)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Logout successfully")
        return redirect('login')


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        page = 'registration'
        ctx = {
            "form": form,
            'page': page
        }
        return render(request, "booking_rooms_app/form.html", ctx)

    def post(self, request):
        form = RegistrationForm(request.POST)
        ctx = {
            "form": form,
        }
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            messages.success(request, f'New account created: {user.username}')
            return redirect('login')

        return render(request, 'booking_rooms_app/form.html', ctx)


class AboutView(View):
    def get(self, request):
        form = CommentForm()
        comments = Comment.objects.all()
        ctx = {
            'form': form,
            'comments': comments
        }
        return render(request, 'booking_rooms_app/About.html', ctx)


@method_decorator(login_required(login_url='login'), name='dispatch')
class AddCommentView(View):
    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            messages.success(request, f'Comment has been added')
            return redirect('about')
