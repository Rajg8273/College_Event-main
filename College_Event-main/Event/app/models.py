from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Organizer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='organizer')
    is_organizer = models.BooleanField(default=True)
    organization_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    # Add more fields as needed

    def __str__(self):
        return self.organization_name

class Event(models.Model):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=100)
    venue = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    organizer_image = models.ImageField(upload_to='organizer_images/')

    # Add more fields as needed

    def __str__(self):
        return self.name

class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participants')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    registration_date = models.DateTimeField(default=timezone.now)
    # Add more fields as needed

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"


class Feedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedbacks')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    # Add more fields as needed

    def __str__(self):
        return f"{self.event.name} - {self.participant.user.username}"
