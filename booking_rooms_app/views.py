import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse
from booking_rooms_app.form import RoomForm, ReservationForm, CommentForm, LoginForm, RegistrationForm, UserUpdateForm
from booking_rooms_app.models import Room, Reservation, Comment
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    return redirect('home')

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('booking_rooms_app/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


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
        room = get_object_or_404(Room, pk=id)
        form = RoomForm(request.POST, instance=room)
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

        form = ReservationForm(request.POST)
        form.instance.room = room
        reservations = room.reservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        date = datetime.date.today()
        context = {
            'room': room,
            'form': form,
            'reservations': reservations,
            'date': date
        }

        if form.is_valid():
            if Reservation.objects.filter(room=room, date=form.instance.date):
                messages.error(request, 'Reservation exist')
                return render(request, 'booking_rooms_app/Reservation.html', context)
            elif form.instance.date < datetime.date.today():
                messages.error(request, 'Date is from the past')
                return render(request, 'booking_rooms_app/Reservation.html', context)
            form.save()
            messages.success(request, f"Reservation has been made")
            return redirect(reverse('all-rooms'))
        messages.error(request, 'Something goes wrong. Please repeat reservation')

        return render(request, 'booking_rooms_app/Reservation.html', context)


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
        else:
            messages.error(request, "Wrong name/password or reCAPTCHA test!")
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
            user.is_active = False
            user.set_password(form.cleaned_data['password'])
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
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


@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfileView(View):
    def get(self, request, username):

        user = get_object_or_404(User, username=username)
        form = UserUpdateForm(instance=user)
        ctx = {
            'form': form,
            'username': username
        }
        return render(request, "booking_rooms_app/profile.html", ctx)

    def post(self, request, username):
        user = get_object_or_404(User, username=username)
        form = UserUpdateForm(request.POST, instance=user)
        ctx = {
            'form': form
        }
        if form.is_valid():
            form.save()
            messages.success(request, f"Your profile has been updated!")
            return redirect('profile', user.username)
        messages.error(request, "Something goes wrong")
        return render(request, 'booking_rooms_app/profile.html', ctx)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('home')