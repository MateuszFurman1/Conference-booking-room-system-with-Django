"""booking_rooms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from booking_rooms_app.views import RoomView, CreateRoomView, AllRoomsView, DetailView, EditRoomView, DeleteRoomView, \
    ReservationView, SearchView, AddCommentView, LoginView, LogoutView, RegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^create-room/$', CreateRoomView.as_view(), name="create-room"),
    re_path(r'^home/$', RoomView.as_view(), name='home'),
    re_path(r'^all-rooms', AllRoomsView.as_view(), name='all-rooms'),
    re_path(r'^detail-room', DetailView.as_view(), name='detail-room'),
    re_path(r'^edit-room', EditRoomView.as_view(), name="edit-room"),
    re_path(r'^delete-room', DeleteRoomView.as_view(), name='delete-room'),
    re_path(r'^room-reserve', ReservationView.as_view(), name='room-reserve'),
    re_path(r'^search-room', SearchView.as_view(), name='search-room'),
    path('AddComment/<int:room_id>/', AddCommentView.as_view(), name='add-comment'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reistration/', RegistrationView.as_view(), name='registration')
]
