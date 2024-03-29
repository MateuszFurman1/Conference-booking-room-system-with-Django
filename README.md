https://user-images.githubusercontent.com/106817902/221347567-afe711be-a6f5-498d-967e-c3fbab7c99a9.mp4


## Key Features

* Book conference room
* Add conference room if login
* Edit and delete room if login
* Login/logout
* Login with reCAPCHA and email confirmation
* Search for conference room by name, capacity and projector avalibility
* Add comment as feedback in about us section

App, which user can book conference room. User also can add text message to booking order, change profile, see available room and search for rooms. Registration system requires email approval to be an active user. Pytest covers all views with fixtures.
Tools & technologies used in project:
python, django framework, postgreSQL, pytest, Bootstrap, HTML, CSS, pycharm


## How to run
* clone repository
* go to Settings-> Project-> Python Interpreter-> add interpreter-> add local interpreter
* terminal: pip install -r requirements.txt
* create local_settings.py file like bellow in main directory:
   DATABASES = {
      'default': {
          'HOST': '127.0.0.1',
          'NAME': 'conferencebookingroom',
          'ENGINE': 'django.db.backends.postgresql',
          'USER': '#user name for ur database',
          'PASSWORD': '#password for ur database',
      }
  }
* open pgadmin and type create database conferenceBookingRoom
* terminal: python manage.py migrate v
* terminal: python manage.py seed_db- to create dummy data
* terminal: python manage.py runserver
* go to http://127.0.0.1:8000/home/


## Requirements
* asgiref==3.6.0
* Django==4.1.3
* django-crispy-forms==1.14.0
* django-factory-boy==1.0.0
* django-simple-captcha==0.5.17
* django_debug_toolbar==3.8.1
* factory-boy==3.2.1
* Faker==15.3.4
* Pillow==9.3.0
* psycopg2-binary==2.9.5
* py==1.11.0
* pytest==7.2.0
* pytest-django==4.5.2
* python-dateutil==2.8.2
* six==1.16.0
* sqlparse==0.4.3
* tzdata==2022.7
