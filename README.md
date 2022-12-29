
![image](https://user-images.githubusercontent.com/106817902/203418984-6230a506-5fe1-4e7e-a3df-d779f5eb943e.png)

## Key Features

* Book conference room
* Add conference room if login
* Edit and delete room if login
* Login/logout
* Login with reCAPCHA and email confirmation
* Search for conference room by name, capacity and projector avalibility
* Add comment as feedback in about us section


## How to run
* clone repository
* go to Settings-> Project-> Python Interprete-> add interpreter-> add local interpreter
* terminal: pip install -r requirements.txt
* create local_settings.py file like bellow in main directory:
   DATABASES = {
      'default': {
          'HOST': '127.0.0.1',
          'NAME': 'conferenceBookingRoom',
          'ENGINE': 'django.db.backends.postgresql',
          'USER': '#user name for ur database',
          'PASSWORD': '#password for ur database',
      }
  }
* open pgadmin and type create database conferenceBookingRoom


## Requirements

* asgiref==3.5.2
* Django==4.1.3
* django-crispy-forms==1.14.0
* django-recaptcha==3.0.0
* Pillow==9.3.0
* psycopg2-binary==2.9.5
* six==1.16.0
* sqlparse==0.4.3
* bootstrap
