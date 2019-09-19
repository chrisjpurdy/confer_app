from django.db import models
from django.contrib.auth.models import User
from .validators import image_restriction

# Create your models here.

class Event(models.Model):
    event_id = models.CharField(max_length=10, unique=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date_opened = models.DateTimeField()
    image = models.ImageField(validators = [image_restriction], default = 'default.jpg', upload_to = 'event_pictures')

# adding an event :: q = Event(event_id="abcdefghij", username=*USER OBJECT*, name="Event number one", description="A small event for the boys", date_opened=timezone.now()*need to import timezone from django.utils*)

class OldEvent(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    date_opened = models.DateTimeField()
    date_closed = models.DateTimeField()

class Question(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    question = models.CharField(max_length=1000)
    time_asked = models.DateTimeField()
